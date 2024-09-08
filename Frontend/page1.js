async function fetchBatteryData() {
  const url = "http://localhost:5000/voltages";

  try {
    const response = await fetch(url);

    if (!response.ok) {
      throw new Error("Errore nella richiesta");
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Errore:", error);
    throw error;
  }
}

async function displayBatteryData() {
  try {
    const data = await fetchBatteryData();
    for (const batteryName in data) {
      const battery = data[batteryName];
      if (batteryName == "Battery0" || batteryName == "Battery1") {
        const batteryId = batteryName === "Battery0" ? "1" : "2";

        document.getElementById(`LV${batteryId}`).textContent =
          battery.min_voltage.toFixed(2);
        document.getElementById(`HV${batteryId}`).textContent =
          battery.max_voltage.toFixed(2);
        document.getElementById(`MD${batteryId}`).textContent =
          battery.max_delta.toFixed(2);
        document.getElementById(`AD${batteryId}`).textContent =
          battery.average_voltage.toFixed(2);
        document.getElementById(`V${batteryId}`).textContent =
          battery.current_voltage.toFixed(2);
        document.getElementById(`EQ${batteryId}`).checked =
          battery.equalization;
      }

      if (batteryName == "shunt_voltage") {
        document.getElementById(`SV`).textContent = battery.toFixed(2);
      }

      if (batteryName == "output_power") {
        if (battery > 0) {
          document.getElementById(`OP`).textContent = "+" + battery.toFixed(2);
          document.getElementById(`OP`).style.color = "#32CD32";
        } else {
          document.getElementById(`OP`).textContent = battery.toFixed(2);
          document.getElementById(`OP`).style.color = "#FF0000";
        }
      }

      if (batteryName == "delta_between_batteries") {
        document.getElementById(`DBB`).textContent = battery.toFixed(2);
      }

      if (batteryName == "charge_rate") {
        if (battery > 0) {
          document.getElementById(`DCR`).textContent = "+" + battery.toFixed(2);
          document.getElementById(`DCR`).style.color = "#32CD32";
        } else {
          document.getElementById(`DCR`).textContent = battery.toFixed(2);
          document.getElementById(`DCR`).style.color = "#FF0000";
        }
      }
    }
  } catch (error) {
    console.error("Errore durante il recupero dei dati della batteria:", error);
  }
}
displayBatteryData();

setInterval(() => {
  setTimeout(() => {
    displayBatteryData();
  }, 50);
}, 50);
