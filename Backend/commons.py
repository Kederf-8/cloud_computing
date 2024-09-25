FIRST_PAGE_IDS = [
    0x50,
    0x51,
    0x52,
    0x53,
    0x54,
    0x55,
    0x56,
    0x57,
    0x58,
    0x59,
    0x5A,
    0x5B,
    0x5C,
    0x5D,
]
SECOND_PAGE_IDS = [
    0x151,
    0x152,
    0x153,
    0x154,
    0x161,
    0x162,
    0x163,
    0x164,
    0x171,
    0x172,
    0x173,
    0x174,
    0x181,
    0x182,
    0x183,
    0x184,
    0x521,
    0x522,
    0x526,
]
THIRD_PAGE_IDS = [0x100, 0x101, 0x102, 0x103]
FOURTH_PAGE_IDS = [0x0B, 0x20, 0x523]

temperature_data = {
    "Battery0": {
        "avg_temp": 0,
        "critical_count": 0,
        "error_count": 0,
        "max_temp": 0,
        "min_temp": 0,
        "warning_count": 0,
    },
    "Battery1": {
        "avg_temp": 0,
        "critical_count": 0,
        "error_count": 0,
        "max_temp": 0,
        "min_temp": 0,
        "warning_count": 0,
    },
}
""" Struttura della response della prima pagina. Usata come struct per conservare i dati"""

battery_temperatures = {
    "Battery0": {
        "0": 0,
        "1": 0,
        "2": 0,
        "3": 0,
        "4": 0,
        "5": 0,
        "6": 0,
        "7": 0,
        "8": 0,
        "9": 0,
        "10": 0,
        "11": 0,
        "12": 0,
        "13": 0,
        "14": 0,
        "15": 0,
        "16": 0,
        "17": 0,
        "18": 0,
        "19": 0,
        "20": 0,
        "21": 0,
        "22": 0,
        "23": 0,
        "24": 0,
        "25": 0,
        "26": 0,
        "27": 0,
    },
    "Battery1": {
        "0": 0,
        "1": 0,
        "2": 0,
        "3": 0,
        "4": 0,
        "5": 0,
        "6": 0,
        "7": 0,
        "8": 0,
        "9": 0,
        "10": 0,
        "11": 0,
        "12": 0,
        "13": 0,
        "14": 0,
        "15": 0,
        "16": 0,
        "17": 0,
        "18": 0,
        "19": 0,
        "20": 0,
        "21": 0,
        "22": 0,
        "23": 0,
        "24": 0,
        "25": 0,
        "26": 0,
        "27": 0,
    },
}
"""Dizionario per conservare i dati delle temperature delle celle"""

min_temperatures = {"Battery0": float("inf"), "Battery1": float("inf")}
"""Lista per tenere traccia delle min_temperatures"""

voltage_data = {
    "Battery0": {
        "average_voltage": 0,
        "current_voltage": 0,
        "equalization": False,
        "max_delta": 0,
        "max_voltage": 0,
        "min_voltage": 0,
    },
    "Battery1": {
        "average_voltage": 0,
        "current_voltage": 0,
        "equalization": False,
        "max_delta": 0,
        "max_voltage": 0,
        "min_voltage": 0,
    },
    "shunt_voltage": 0,
    "output_power": 0,
    "charge_rate": 0,
    "delta_between_batteries": 0,
}
""" Struttura della response della seconda pagina. Usata come struct per conservare i dati"""

battery_voltages = {
    "Battery0": {
        "0": 0,
        "1": 0,
        "2": 0,
        "3": 0,
        "4": 0,
        "5": 0,
        "6": 0,
        "7": 0,
        "8": 0,
        "9": 0,
        "10": 0,
        "11": 0,
        "12": 0,
        "13": 0,
        "14": 0,
        "15": 0,
        "16": 0,
        "17": 0,
        "18": 0,
        "19": 0,
        "20": 0,
        "21": 0,
        "22": 0,
        "23": 0,
        "24": 0,
        "25": 0,
        "26": 0,
        "27": 0,
    },
    "Battery1": {
        "0": 0,
        "1": 0,
        "2": 0,
        "3": 0,
        "4": 0,
        "5": 0,
        "6": 0,
        "7": 0,
        "8": 0,
        "9": 0,
        "10": 0,
        "11": 0,
        "12": 0,
        "13": 0,
        "14": 0,
        "15": 0,
        "16": 0,
        "17": 0,
        "18": 0,
        "19": 0,
        "20": 0,
        "21": 0,
        "22": 0,
        "23": 0,
        "24": 0,
        "25": 0,
        "26": 0,
        "27": 0,
    },
}
"""Dizionario per conservare i dati delle tensioni delle celle"""

min_voltages = {"Battery0": float("inf"), "Battery1": float("inf")}
"""Lista per tenere traccia dei min_voltages"""

engine_data = {
    "MotoreDX": {
        "engine_temp": 0,
        "controller_temp": 0,
        "controller_voltage": 0,
        "current_requested": 0,  # costante
        "current_used": 0,
        "power_used": 0,
        "rpm": 0,
    },
    "MotoreSX": {
        "engine_temp": 0,
        "controller_temp": 0,
        "controller_voltage": 0,
        "current_requested": 0,  # costante
        "current_used": 0,
        "power_used": 0,
        "rpm": 0,
    },
    "speed": 0,
    "log_error": "Questo log dimostra che la ci/cd funziona;Over Temperature Engine Left 12.31;Internal volts fault Engine Left 12.29;Throttle error at power-up Engine Right 12.15; Over Temperature engine 0 12.13;Warning cell in engine 1 12.12;Warning cell in engine 1 12.11;Warning cell in engine 1 12.09; Errore batteria destra cella 2 12.19; Errore batteria sinistra cella 3 12.20;",
}
""" Struttura della response della terza pagina. Usata come struct per conservare i dati"""

ROLLING = 1810
"""Costante di rotolamento calcolata in base alle ruote ed agli pneumatici"""

mppt_data = {
    "mppt1": {"current": 0, "status": False, "power": 0},
    "mppt2": {"current": 0, "status": False, "power": 0},
    "mppt3": {"current": 0, "status": False, "power": 0},
    "power_tot": 0,
    "voltage": 0,
    "current_tot": 0,
}
""" Struttura della response della quarta pagina. Usata come struct per conservare i dati"""


def reverse_byte_order(data):
    """Inverti l'ordine di LSB ed MSB"""
    reversed_data = bytearray(len(data))
    for i in range(0, len(data), 2):
        reversed_data[i] = data[i + 1]
        reversed_data[i + 1] = data[i]
    return reversed_data
