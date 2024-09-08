async function fetchMpptData() {
  const url = "http://localhost:5000/mppts";

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

async function displayMpptData() {
  try {
    const data = await fetchMpptData();
    for (const mpptNumber in data) {
      const mppt = data[mpptNumber];

      if (
        mpptNumber == "mppt1" ||
        mpptNumber == "mppt2" ||
        mpptNumber == "mppt3"
      ) {
        document.getElementById(`CA${mpptNumber}`).textContent = mppt.current.toFixed(2);
        document.getElementById(`PW${mpptNumber}`).textContent = mppt.power.toFixed(2);
        var statusElement = document.getElementById(`STATUS${mpptNumber}`);
        if (mppt.status) {
          statusElement.classList.remove("cellItem-inverter-disabled");
          statusElement.classList.add("cellItem-inverter-enabled");
          statusElement.textContent = "ENABLED";
        } else {
          statusElement.classList.remove("cellItem-inverter-enabled");
          statusElement.classList.add("cellItem-inverter-disabled");
          statusElement.textContent = "DISABLED";
        }
      }
      if (mpptNumber == "power_tot") {
        document.getElementById(`PWTOT`).textContent = mppt.toFixed(2);
      }
      if (mpptNumber == "current_tot") {
        document.getElementById(`CTOT`).textContent = mppt.toFixed(2);
      }
      if (mpptNumber == "voltage") {
        document.getElementById(`VOLTAGE`).textContent = mppt.toFixed(2);
      }
    }
  } catch (error) {
    console.error("Errore durante il recupero dei dati:", error);
  }
}

setInterval(() => {
  setTimeout(() => {
    displayMpptData();
  }, 50);
}, 50);
