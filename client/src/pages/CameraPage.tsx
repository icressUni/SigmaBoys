import React, { useEffect, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Camera from '../componentes/Camara';
import axios from 'axios';

function CameraPage() {
  const [isLoading, setIsLoading] = useState(true);
  const [facesDetected, setFacesDetected] = useState(0);
  const [recognitionResult, setRecognitionResult] = useState<string[]>([]); // Resultados del reconocimiento
  const navigate = useNavigate();
  const videoRef = useRef<HTMLVideoElement | null>(null);

  // Cargar modelos de face-api.js
  const loadModels = async () => {
    setIsLoading(false);
  };

  // Detectar caras en tiempo real y tomar foto cuando se detecta
  const detectFacesInVideo = async () => {
    if (videoRef.current) {
      const canvas = faceapi.createCanvasFromMedia(videoRef.current);
      document.body.append(canvas);
      faceapi.matchDimensions(canvas, videoRef.current);
      const detections = await faceapi.detectAllFaces(videoRef.current).withFaceLandmarks().withFaceDescriptors();
      canvas?.drawDetections(detections);

      setFacesDetected(detections.length);

      if (detections.length > 0) {
        captureImageForRecognition(detections);
      }
    }
  };

  // Función para capturar una imagen y enviarla al backend para reconocimiento
  const captureImageForRecognition = async (detections: any) => {
    if (videoRef.current) {
      const canvas = faceapi.createCanvasFromMedia(videoRef.current);
      const dataUrl = canvas.toDataURL(); // Convierte el canvas en una imagen base64

      try {
        const formData = new FormData();
        formData.append('imagen', dataUrl);

        const response = await axios.post('http://localhost:5000/api/reconocer', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });

        if (response.data.resultados) {
          setRecognitionResult(response.data.resultados);
        }
      } catch (error) {
        console.error("Error al reconocer la imagen:", error);
      }
    }
  };

  useEffect(() => {
    loadModels();
  }, []);

  useEffect(() => {
    if (!isLoading) {
      const interval = setInterval(() => {
        detectFacesInVideo();
      }, 100); // Detectar cada 100ms
      return () => clearInterval(interval);
    }
  }, [isLoading]);

  return (
    <div className="camera-page">
      <h1>Sistema de Reconocimiento Facial</h1>

      {/* Sección de estado del sistema */}
      <div className="section" id="status-section">
        <h2>Estado del Sistema</h2>
        <div id="status" className={`status ${isLoading ? 'error' : 'success'}`}>
          {isLoading ? 'Comprobando estado de la API...' : 'API conectada correctamente'}
        </div>
      </div>

      {/* Sección de cámara */}
      <div className="section">
        <h2>Reconocimiento en Tiempo Real</h2>
        <Camera videoRef={videoRef} onError={(err) => console.error(err)} />

        {/*{facesDetected > 0 && <div>¡Cara detectada!</div>}*/}
        {/*{facesDetected === 0 && <div>No se detectaron caras.</div>}*/}
      </div>

      {/* Sección de resultados */}
      {recognitionResult.length > 0 && (
        <div className="section" id="results">
          <h2>Resultados del Reconocimiento:</h2>
          <div className="result-container">
            <div className="result-info">
              <h3>Personas Identificadas</h3>
              {recognitionResult.map((name, index) => (
                <div key={index} className="person">
                  <strong>{name}</strong>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      <button className="login-button" onClick={() => navigate("/manual-login")}>
        Iniciar sesión manualmente
      </button>
    </div>
  );
}

export default CameraPage;
