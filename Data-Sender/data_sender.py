import random
import time

import requests
from google.cloud import pubsub_v1

# Configura il publisher di Pub/Sub
project_id = "solarcaroncloud"
topic_id = "canbus-topic"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

# Lista dei valori possibili per X
x_values = [
    "050",
    "051",
    "052",
    "053",
    "054",
    "055",
    "056",
    "057",
    "058",
    "059",
    "05A",
    "05B",
    "05C",
    "05D",
    "151",
    "152",
    "153",
    "154",
    "161",
    "162",
    "163",
    "164",
    "171",
    "172",
    "173",
    "174",
    "181",
    "182",
    "183",
    "184",
    "521",
    "522",
    "526",
    "100",
    "101",
    "102",
    "103",
    "00B",
    "020",
    "523",
]

# Lista dei valori possibili per Y
y_values = [
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
]

while True:
    # Genera valori casuali per X e Y
    x = random.choice(x_values)
    y_hex = "".join([random.choice(y_values) for _ in range(16)])

    # Formatta il pacchetto simulato in formato CANbus
    packet = f"{x}#{y_hex}"
    print(f"Inviando pacchetto: {packet}")

    # Pubblica il pacchetto su Pub/Sub
    future = publisher.publish(topic_path, packet.encode("utf-8"))
    print(f"Pacchetto pubblicato: {future.result()}")

    # Attendere 200 ms prima di inviare il prossimo pacchetto
    time.sleep(0.2)
