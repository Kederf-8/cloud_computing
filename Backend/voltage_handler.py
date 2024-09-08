import struct

import can
from commons import battery_voltages, reverse_byte_order, voltage_data


def process_voltage_packet(message):
    packet_id = message.arbitration_id
    battery_name = None

    if 0x151 <= packet_id <= 0x154:
        battery_name = "Battery0"
        cell_index = (packet_id - 0x151) * 4
    elif 0x161 <= packet_id <= 0x164:
        battery_name = "Battery0"
        cell_index = (packet_id - 0x161) * 4 + 14
    elif 0x171 <= packet_id <= 0x174:
        battery_name = "Battery1"
        cell_index = (packet_id - 0x171) * 4
    elif 0x181 <= packet_id <= 0x184:
        battery_name = "Battery1"
        cell_index = (packet_id - 0x181) * 4 + 14

    if battery_name is not None:
        data = message.data

        if packet_id in [0x154, 0x164, 0x174, 0x184]:
            # Check if equalization is active (first 14 bits)
            voltage_data[battery_name]["equalization"] = any(
                val >= 0x04 for val in data[4:6]
            )
            # Use only the first 4 bytes for these packets
            data = data[:4]

        reversed_data = reverse_byte_order(data)
        for i in range(0, len(reversed_data), 2):
            voltage = int.from_bytes(reversed_data[i : i + 2], byteorder="big") / 1000.0
            battery_voltages[battery_name][str(cell_index)] = round(voltage, 2)
            cell_index += 1

    if packet_id == 0x521:
        data = message.data
        recieved_charge_rate = struct.unpack(">i", data[2:6])[0]
        charge_rate = round(recieved_charge_rate / 1000, 2)  # da mA a A
        voltage_data["charge_rate"] = charge_rate

    if packet_id == 0x522:
        data = message.data
        received_shunt_voltage = int.from_bytes(message.data[2:6], byteorder="big")
        shunt_voltage = round(received_shunt_voltage / 1000, 2)  # da mV a V
        voltage_data["shunt_voltage"] = shunt_voltage

    if packet_id == 0x526:
        data = message.data
        recieved_output_power = struct.unpack(">i", data[2:6])[0]
        output_power = round(recieved_output_power / 1000, 2)  # da W a kW
        voltage_data["output_power"] = output_power


def update_battery_voltages(message):
    try:
        if message is not None:
            process_voltage_packet(message)
    except can.CanError:
        pass
