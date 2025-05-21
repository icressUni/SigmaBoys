import React, { useState, useEffect } from "react";

const API_URL = "http://localhost:5000/api";

function RegistroRostro() {
  const [statusMessage, setStatusMessage] = useState("Comprobando estado de la API...");
  const [statusClass, setStatusClass] = useState("status");
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [resultData, setResultData] = useState(null);

  // Función para chequear el estado de la API
  const checkStatus = async () => {
    setStatusMessage("Comprobando estado de la API...");
    setStatusClass("status");

    try {
      const response = await fetch(`${API_URL}/status`);
      const data = await response.json();

      if (response.ok) {
        setStatusMessage(`API conectada correctamente: ${data.message}`);
        setStatusClass("status success");
      } else {
        setStatusMessage(`Error al conectar con la API: ${data.error}`);
        setStatusClass("status error");
      }
    } catch (error) {
      setStatusMessage(`Error al conectar con la API: ${error.message}`);
      setStatusClass("status error");
      console.error("Error:", error);
    }
  };

  // Reconocer rostros en la imagen
  const recognizeFaces = async () => {
    if (!file) {
      alert("Por favor selecciona una imagen");
      return;
    }

    setLoading(true);
    setResultData(null);

    const formData = new FormData();
    formData.append("imagen", file);

    try {
      const response = await fetch(`${API_URL}/reconocer`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        setResultData(data);
      } else {
        alert(`Error: ${data.error}`);
      }
    } catch (error) {
      alert(`Error al procesar la imagen: ${error.message}`);
      console.error("Error:", error);
    } finally {
      setLoading(false);
    }
  };

  // Se ejecuta al cargar el componente
  useEffect(() => {
    checkStatus();
  }, []);

  return (
    <div className="container">
      <h1>Sistema de Reconocimiento Facial</h1>

      <div className="section" id="status-section">
        <h2>Estado del Sistema</h2>
        <div id="status" className={statusClass}>
          {statusMessage}
        </div>
        <button onClick={checkStatus}>Comprobar estado</button>
      </div>

      <div className="section">
        <h2>Reconocimiento de Imagen</h2>
        <p>Sube una imagen para identificar rostros:</p>
        <input
          type="file"
          id="image-upload"
          accept="image/*"
          onChange={(e) => setFile(e.target.files[0])}
        />
        <button onClick={recognizeFaces}>Reconocer rostros</button>

        {loading && (
          <div id="loading" style={{ marginTop: 10 }}>
            Procesando imagen... Por favor espere.
          </div>
        )}

        {resultData && (
          <div
            id="results"
            className="result-container"
            style={{ marginTop: 20, display: "flex" }}
          >
            <div id="result-image-container">
              <h3>Imagen Procesada</h3>
              <img
                id="result-image"
                className="result-image"
                src={`data:image/jpeg;base64,${resultData.imagen_procesada}`}
                alt="Imagen procesada"
              />
            </div>

            <div className="result-info">
              <h3>Personas Identificadas</h3>
              <div id="persons-list">
                {resultData.resultados.length === 0 ? (
                  <p>No se encontraron rostros en la imagen.</p>
                ) : (
                  resultData.resultados.map((persona, index) => {
                    const confianza = persona.confianza.toFixed(2);
                    const colorStyle =
                      persona.nombre === "Desconocido"
                        ? { color: "red" }
                        : { color: "green" };

                    return (
                      <div key={index} className="person">
                        <strong style={colorStyle}>
                          Persona {index + 1}: {persona.nombre}
                        </strong>
                        <div>Confianza: {confianza}%</div>
                      </div>
                    );
                  })
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default RegistroRostro;
