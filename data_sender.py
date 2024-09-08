import random
import time

import requests

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

# Indirizzo del backend locale
backend_url = "http://localhost:5000/canbus"

while True:
    # Genera valori casuali per X e Y
    x = random.choice(x_values)
    y_hex = "".join([random.choice(y_values) for _ in range(16)])

    # Formatta il pacchetto simulato in formato CANbus
    packet = "{}#{}".format(x, y_hex)
    print("Inviando pacchetto: {}".format(packet))

    # Invia il pacchetto al backend tramite una richiesta POST
    try:
        response = requests.post(backend_url, json={"packet": packet})
        print("Risposta dal server: {}".format(response.status_code))
    except Exception as e:
        print("Errore durante l'invio del pacchetto: {}".format(e))

    # Attendere 200 ms prima di inviare il prossimo pacchetto
    time.sleep(0.2)
