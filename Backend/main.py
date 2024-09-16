import datetime
import logging
from pathlib import Path

from commons import (
    FIRST_PAGE_IDS,
    FOURTH_PAGE_IDS,
    SECOND_PAGE_IDS,
    THIRD_PAGE_IDS,
    battery_temperatures,
    battery_voltages,
    engine_data,
    mppt_data,
)
from engine_handler import update_engine_data
from flask import Flask, jsonify, request
from flask_cors import CORS
from google.cloud import pubsub_v1, storage
from mppt_handler import update_mppt_data
from statistics_calculator import (
    calculate_temperature_statistics,
    calculate_voltage_statistics,
)
from temperature_handler import update_battery_temperatures
from voltage_handler import update_battery_voltages

# Configura Flask e CORS
app = Flask(__name__)
CORS(app)

# Configura il logging
now = datetime.datetime.now()
formatted_date = now.strftime("%d-%m-%y-%H:%M")
if not Path("logs").exists():
    Path("logs").mkdir()
file_name = f"logs/log{formatted_date}.txt"

logging.basicConfig(
    filename=file_name,
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

# Configura Google Cloud Pub/Sub e Google Cloud Storage
project_id = "solarcaroncloud"
subscription_id = "canbus-topic-sub"
bucket_name = "solarcar-bucket"

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)
storage_client = storage.Client()


# Classe che simula il messaggio CAN
class SimulatedCANMessage:
    def __init__(self, arbitration_id, data):
        self.arbitration_id = arbitration_id
        self.data = data


# Funzione per salvare i dati su Google Cloud Storage
def save_to_gcs(data, filename):
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(filename)
    blob.upload_from_string(data)
    logging.info(f"Dati salvati in {filename} su GCS.")


# Callback per elaborare i messaggi Pub/Sub
def callback(message):
    packet = message.data.decode("utf-8")
    print(f"Pacchetto ricevuto: {packet}")
    try:
        packet_id_str, packet_data_str = packet.split("#")
        packet_id = int(packet_id_str, 16)
        packet_data = bytes.fromhex(packet_data_str)
    except ValueError:
        logging.error("Invalid message format: %s", packet)
        message.nack()  # Non conferma il messaggio
        return

    # Crea un oggetto SimulatedCANMessage
    simulated_message = SimulatedCANMessage(packet_id, packet_data)

    date = datetime.datetime.now().strftime("%H:%M:%S")

    # Processa il pacchetto in base al suo ID
    if packet_id in FIRST_PAGE_IDS:
        try:
            update_battery_temperatures(simulated_message)
            logging.info("Temperature data updated successfully (%s).", date)
            logging.info("Temperatures: %s", battery_temperatures)
            save_to_gcs(
                str(battery_temperatures), f"temperatures_{formatted_date}.json"
            )
        except Exception as e:
            logging.error("Error updating temperature data: %s", e)
    elif packet_id in SECOND_PAGE_IDS:
        try:
            update_battery_voltages(simulated_message)
            logging.info("Voltage data updated successfully (%s).", date)
            logging.info("Voltages: %s", battery_voltages)
            save_to_gcs(str(battery_voltages), f"voltages_{formatted_date}.json")
        except Exception as e:
            logging.error("Error updating voltage data: %s", e)
    elif packet_id in THIRD_PAGE_IDS:
        try:
            update_engine_data(simulated_message)
            logging.info("Engine data updated successfully (%s).", date)
            save_to_gcs(str(engine_data), f"engine_{formatted_date}.json")
        except Exception as e:
            logging.error("Error updating engine data: %s", e)
    elif packet_id in FOURTH_PAGE_IDS:
        try:
            update_mppt_data(simulated_message)
            logging.info("MPPT data updated successfully (%s).", date)
            save_to_gcs(str(mppt_data), f"mppt_{formatted_date}.json")
        except Exception as e:
            logging.error("Error updating MPPT data: %s", e)

    message.ack()  # Conferma il messaggio


# Avvia la sottoscrizione a Pub/Sub
streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
logging.info(f"Ascoltando i messaggi per {subscription_path}...")


# Endpoint per recuperare i dati del frontend
@app.route("/temperatures")
def get_battery_temperatures():
    response_data = {}
    for battery_name, cell_temperatures in battery_temperatures.items():
        temperatures = list(cell_temperatures.values())
        response_data = calculate_temperature_statistics(temperatures, battery_name)
    return jsonify(response_data)


@app.route("/voltages")
def get_battery_voltages():
    response_data = {}
    for battery_name, cell_voltages in battery_voltages.items():
        voltages = list(cell_voltages.values())
        response_data = calculate_voltage_statistics(voltages, battery_name)
    return jsonify(response_data)


@app.route("/engines")
def get_engine_endpoint():
    return jsonify(engine_data)


@app.route("/mppts")
def get_mppt_endpoint():
    return jsonify(mppt_data)


if __name__ == "__main__":
    # Esegui il backend e avvia l'ascolto dei messaggi
    try:
        app.run(host="0.0.0.0", port=5000)
        streaming_pull_future.result()
    except KeyboardInterrupt:
        streaming_pull_future.cancel()
        logging.info("Arresto del backend...")
