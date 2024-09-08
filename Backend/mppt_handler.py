import can
from commons import mppt_data


def process_mppt_packet(message):
    packet_id = message.arbitration_id

    if packet_id == 0x0B:
        # Process data from ID 0x0B to update MPPT status
        data = message.data[0]
        for i in range(3):
            if (data >> i + 1) & 0x01 == 1:
                mppt_data[f"mppt{3 - i}"]["status"] = True
            else:
                mppt_data[f"mppt{3 - i}"]["status"] = False

    elif packet_id == 0x20:
        # Process data from ID 0x20 to update MPPT currents and total power

        received_current_mppt1 = int.from_bytes(message.data[2:4], byteorder="big")
        received_current_mppt2 = int.from_bytes(message.data[4:6], byteorder="big")
        received_current_mppt3 = int.from_bytes(message.data[6:8], byteorder="big")

        current_mppt1 = round(
            ((received_current_mppt1 & 0xFFF) / 0xFFF) * 50 - 25, 2
        )  # da - 25 a + 25
        current_mppt2 = round(
            ((received_current_mppt2 & 0xFFF) / 0xFFF) * 50 - 25, 2
        )  # da - 25 a + 25
        current_mppt3 = round(
            ((received_current_mppt3 & 0xFFF) / 0xFFF) * 50 - 25, 2
        )  # da - 25 a + 25

        mppt_data["mppt1"]["current"] = current_mppt1
        mppt_data["mppt2"]["current"] = current_mppt2
        mppt_data["mppt3"]["current"] = current_mppt3

        power_1 = round(current_mppt1 * mppt_data["voltage"], 2)
        power_2 = round(current_mppt2 * mppt_data["voltage"], 2)
        power_3 = round(current_mppt3 * mppt_data["voltage"], 2)

        mppt_data["mppt1"]["power"] = power_1
        mppt_data["mppt2"]["power"] = power_2
        mppt_data["mppt3"]["power"] = power_3

        # Calculate total power
        total_power = round(power_1 + power_2 + power_3, 2)
        mppt_data["power_tot"] = total_power

        # Calculate total current
        total_current = round(current_mppt1 + current_mppt2 + current_mppt3, 2)
        mppt_data["current_tot"] = total_current

    elif packet_id == 0x523:
        received_voltage = int.from_bytes(message.data[2:6], byteorder="big")
        voltage = round(received_voltage / 1000, 2)  # da mV a V
        mppt_data["voltage"] = voltage


def update_mppt_data(message):
    try:
        if message is not None:
            process_mppt_packet(message)
    except can.CanError:
        pass
