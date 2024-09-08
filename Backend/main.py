import datetime
import logging
import threading
import time
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
from mppt_handler import update_mppt_data
from statistics_calculator import (
    calculate_temperature_statistics,
    calculate_voltage_statistics,
)
from temperature_handler import update_battery_temperatures
from voltage_handler import update_battery_voltages

app = Flask(__name__)

# Configura il middleware CORS per consentire le richieste da http://localhost:8000
CORS(app, origins="http://localhost:8000")

# Genera il file di log, con la data e l'ora attuale nel nome
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

# Ignora i log delle chiamate GET
log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)


# Classe che simula il messaggio CAN
class SimulatedCANMessage:
    def __init__(self, arbitration_id, data):
        self.arbitration_id = arbitration_id
        self.data = data


# Simula la ricezione dei pacchetti tramite POST
@app.route("/canbus", methods=["POST"])
def receive_canbus_packet():
    data = request.get_json()
    packet = data.get("packet")

    # Simula la ricezione del pacchetto CANbus
    if packet:
        print(f"Pacchetto ricevuto: {packet}")
        try:
            packet_id_str, packet_data_str = packet.split("#")
            packet_id = int(packet_id_str, 16)
            packet_data = bytes.fromhex(packet_data_str)
        except ValueError:
            logging.error("Invalid message format: %s", packet)
            return jsonify({"status": "error", "message": "Invalid packet format"}), 400

        # Crea un oggetto SimulatedCANMessage
        simulated_message = SimulatedCANMessage(packet_id, packet_data)

        date = datetime.datetime.now().strftime("%H:%M:%S")

        # Processa il pacchetto in base al suo ID
        if packet_id in FIRST_PAGE_IDS:
            try:
                update_battery_temperatures(simulated_message)
                logging.info("Temperature data updated successfully (%s).", date)
                logging.info("Temperatures: %s", battery_temperatures)
            except Exception as e:
                logging.error("Error updating temperature data: %s", e)
        if packet_id in SECOND_PAGE_IDS:
            try:
                update_battery_voltages(simulated_message)
                logging.info("Voltage data updated successfully (%s).", date)
                logging.info("Voltages: %s", battery_voltages)
            except Exception as e:
                logging.error("Error updating voltage data: %s", e)
        if packet_id in THIRD_PAGE_IDS:
            try:
                update_engine_data(simulated_message)
                logging.info("Engine data updated successfully (%s).", date)
            except Exception as e:
                logging.error("Error updating engine data: %s", e)
        if packet_id in FOURTH_PAGE_IDS:
            try:
                update_mppt_data(simulated_message)
                logging.info("MPPT data updated successfully (%s).", date)
            except Exception as e:
                logging.error("Error updating MPPT data: %s", e)

        return jsonify({"status": "success"}), 200
    return jsonify({"status": "error", "message": "Invalid packet"}), 400


# Gli endpoint del frontend rimangono invariati
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
    app.run(host="0.0.0.0", port=5000)
