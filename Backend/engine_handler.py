import can
from commons import ROLLING, engine_data, reverse_byte_order


def process_engine_packet(message):
    packet_id = message.arbitration_id

    if packet_id == 0x0100 or packet_id == 0x0101:
        data = message.data
        reversed_data = reverse_byte_order(data)
        received_rpm = int.from_bytes(reversed_data[0:2], byteorder="big")
        received_current = int.from_bytes(reversed_data[2:4], byteorder="big")
        received_voltage = int.from_bytes(reversed_data[4:6], byteorder="big")

        rpm = round(received_rpm * 6000 / 0xFFFF, 2)  # da 0 a 6000

        """Calcolo con la divisione sul valore ricevuto"""
        # current = round((received_current / 10) * 4000 / 0x1999, 2)  # da 0 a 4000
        # voltage = round((received_voltage / 10) * 1800 / 0x1999, 2)  # da 0 a 1800

        """Calcolo con i range divisi per 10"""
        current = round(received_current * 400 / 0xFFFF, 2)  # da 0 a 400
        voltage = round(received_voltage * 180 / 0xFFFF, 2)  # da 0 a 180

        """Calcolo con l'hard cut del valore ricevuto"""
        # current = round(received_current, 2)  # da 0 a 4000
        # if current > 4000:
        #     current = 4000
        # voltage = round(received_voltage, 2)  # da 0 a 1800
        # if voltage > 1800:
        #     voltage = 1800

        power = round(current * voltage, 2)

        if packet_id == 0x0100:
            engine_data["MotoreSX"]["rpm"] = rpm
            engine_data["MotoreSX"]["current_used"] = current
            engine_data["MotoreSX"]["controller_voltage"] = voltage
            engine_data["MotoreSX"]["power_used"] = power
        elif packet_id == 0x0101:
            engine_data["MotoreDX"]["rpm"] = rpm
            engine_data["MotoreDX"]["current_used"] = current
            engine_data["MotoreDX"]["controller_voltage"] = voltage
            engine_data["MotoreDX"]["power_used"] = power

        if not engine_data["MotoreDX"]["rpm"] + engine_data["MotoreSX"]["rpm"] == 0:
            avg_rpm = (
                engine_data["MotoreDX"]["rpm"] + engine_data["MotoreSX"]["rpm"]
            ) / 2

            engine_data["speed"] = int(convert_rpm2km(avg_rpm))
        else:
            engine_data["speed"] = 0

    if packet_id == 0x0102 or packet_id == 0x0103:
        received_controller_temp = message.data[1]
        received_engine_temp = message.data[2]
        contoller_temp = received_controller_temp - 40  # offset 40°
        engine_temp = received_engine_temp - 30  # offset 30°
        if packet_id == 0x0102:
            engine_data["MotoreSX"]["controller_temp"] = contoller_temp
            engine_data["MotoreSX"]["engine_temp"] = engine_temp
        elif packet_id == 0x0103:
            engine_data["MotoreDX"]["controller_temp"] = contoller_temp
            engine_data["MotoreDX"]["engine_temp"] = engine_temp


def convert_rpm2km(rpm):
    meters = ROLLING / 1000
    meters_x_minute = meters * rpm
    km_x_minute = meters_x_minute / 1000
    km_x_h = km_x_minute * 60
    return km_x_h


def update_engine_data(message):
    try:
        if message is not None:
            process_engine_packet(message)
    except can.CanError:
        pass
