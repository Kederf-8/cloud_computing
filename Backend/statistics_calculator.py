from commons import (
    battery_temperatures,
    battery_voltages,
    min_temperatures,
    temperature_data,
    voltage_data,
)


def calculate_temperature_statistics(temperatures, battery_name):
    if not temperatures:
        return temperature_data

    avg_temp = round(sum(temperatures) / len(temperatures), 2)
    temperature_data[battery_name]["avg_temp"] = avg_temp

    max_temp = max(battery_temperatures[battery_name].values())
    temperature_data[battery_name]["max_temp"] = max_temp

    min_temp = min(battery_temperatures[battery_name].values())
    min_temperatures[battery_name] = min_temp

    if not temperature_data[battery_name]["min_temp"] == min_temperatures[battery_name]:
        temperature_data[battery_name]["min_temp"] = min_temperatures[battery_name]

    warning_count = sum(1 for temp in temperatures if temp > 35)
    temperature_data[battery_name]["warning_count"] = warning_count

    critical_count = sum(1 for temp in temperatures if temp > 45)
    temperature_data[battery_name]["critical_count"] = critical_count

    error_count = sum(1 for temp in temperatures if temp > 55)
    temperature_data[battery_name]["error_count"] = error_count

    return temperature_data


def calculate_voltage_statistics(voltages, battery_name):
    if not voltages:
        return voltage_data

    average_voltage = round(sum(voltages) / len(voltages), 2)
    voltage_data[battery_name]["average_voltage"] = average_voltage

    current_voltage = round(sum(voltages), 2)
    voltage_data[battery_name]["current_voltage"] = current_voltage

    min_voltage = min(battery_voltages[battery_name].values())
    voltage_data[battery_name]["min_voltage"] = min_voltage

    max_voltage = max(battery_voltages[battery_name].values())
    voltage_data[battery_name]["max_voltage"] = max_voltage

    max_delta = max_voltage - min_voltage
    voltage_data[battery_name]["max_delta"] = max_delta

    delta_between_batteries = abs(
        voltage_data["Battery0"]["max_delta"] - voltage_data["Battery1"]["max_delta"]
    )
    voltage_data["delta_between_batteries"] = delta_between_batteries

    return voltage_data
