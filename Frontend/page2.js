async function fetchEngineData() {
  const url = "http://localhost:5000/engines";

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

async function displayEngineData() {
  try {
    const data = await fetchEngineData();
    for (const engineName in data) {
      const engine = data[engineName];
      const engineId = engineName === "MotoreDX" ? "DX" : "SX";

      if (engineName == "MotoreDX" || engineName == "MotoreSX") {
        document.getElementById(`ET${engineId}`).textContent =
          engine.engine_temp.toFixed(2);
        document.getElementById(`CT${engineId}`).textContent =
          engine.controller_temp.toFixed(2);
        document.getElementById(`CV${engineId}`).textContent =
          engine.controller_voltage.toFixed(2);
        document.getElementById(`CR${engineId}`).textContent =
          engine.current_requested.toFixed(2);
        document.getElementById(`CU${engineId}`).textContent =
          engine.current_used.toFixed(2);
        document.getElementById(`PW${engineId}`).textContent =
          engine.power_used.toFixed(2);
        document.getElementById(`RPM${engineId}`).textContent =
          engine.rpm.toFixed(2);
      }

      if (engineName == "speed") {
        document.getElementById(`SPEED`).textContent = engine;
      }

      if (engineName == "log_error") {
        const log_error_formattato = engine.replace(/;/g, "<br>");
        const limitatore = 7;
        const primiSetteBr = log_error_formattato
          .split("<br>", limitatore)
          .join("<br>");
        document.getElementById(`LOG`).innerHTML = primiSetteBr;
      }
    }
  } catch (error) {
    console.error("Errore durante il recupero dei dati dei motori:", error);
  }
}
displayEngineData();

setInterval(() => {
  setTimeout(() => {
    displayEngineData();
  }, 50);
}, 50);
