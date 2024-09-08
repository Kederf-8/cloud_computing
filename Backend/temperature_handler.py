import can
from commons import battery_temperatures, reverse_byte_order


def process_can_packet(message):
    packet_id = message.arbitration_id  # CAN packet ID
    data = message.data  # CAN packet data

    if 0x50 <= packet_id <= 0x56:
        # Process temperature data from battery packet 0
        battery_name = "Battery0"
        cell_group = (packet_id - 0x50) * 4
    elif 0x57 <= packet_id <= 0x5D:
        # Process temperature data from battery packet 1
        battery_name = "Battery1"
        cell_group = (packet_id - 0x57) * 4

    reversed_data = reverse_byte_order(data)
    for i in range(0, len(reversed_data), 2):
        if i + 1 < len(reversed_data):
            cell_number = cell_group + i // 2
            cell_temp_raw = reversed_data[i] << 8 | reversed_data[i + 1]
            cell_temp = cell_temp_raw / 128.0
            battery_temperatures[battery_name][str(cell_number)] = round(cell_temp, 2)


def update_battery_temperatures(message):
    try:
        if message is not None:
            process_can_packet(message)
    except can.CanError:
        pass
