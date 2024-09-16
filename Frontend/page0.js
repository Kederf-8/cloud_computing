async function fetchBatteryData() {
  const url = "http://35.226.184.53:5000/temperatures";

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
      const batteryId = batteryName === "Battery0" ? "1" : "2";

      document.getElementById(`LT${batteryId}`).textContent = battery.min_temp.toFixed(2);
      document.getElementById(`HT${batteryId}`).textContent = battery.max_temp.toFixed(2);
      document.getElementById(`CIW${batteryId}`).textContent =
        battery.warning_count;
      document.getElementById(`CIC${batteryId}`).textContent =
        battery.critical_count;
      document.getElementById(`CIE${batteryId}`).textContent =
        battery.error_count;
      document.getElementById(`TA${batteryId}`).textContent = battery.avg_temp.toFixed(2);

      const ciwElement = document.getElementById(`CIW${batteryId}`);
      const cicElement = document.getElementById(`CIC${batteryId}`);
      const cieElement = document.getElementById(`CIE${batteryId}`);

      if (battery.warning_count >= 5) {
        ciwElement.style.color = "#F5B800";
        ciwElement.style.fontWeight = "bold";
      } else {
        ciwElement.style.color = "black";
        ciwElement.style.fontWeight = "normal";
      }

      if (battery.critical_count >= 2) {
        cicElement.style.color = "#FF8000";
        cicElement.style.fontWeight = "bold";
      } else {
        cicElement.style.color = "black";
        cicElement.style.fontWeight = "normal";
      }

      if (battery.error_count >= 1) {
        cieElement.style.color = "#FF0000";
        cieElement.style.fontWeight = "bold";
      } else {
        cieElement.style.color = "black";
        cieElement.style.fontWeight = "normal";
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
