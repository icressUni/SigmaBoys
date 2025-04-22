import React, { useEffect, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Camera from '../componentes/Camara';
import { loadFaceModels, detectFaces } from '../componentes/faceRecognition';  // Importa las funciones

function CameraPage() {
  const [isLoading, setIsLoading] = useState(true);
  const [facesDetected, setFacesDetected] = useState(0);
  const navigate = useNavigate();
  const videoRef = useRef<HTMLVideoElement | null>(null);

  // Cargar modelos de face-api.js
  const loadModels = async () => {
    await loadFaceModels(); // Usar la función importada
    setIsLoading(false);
  };

  // Detectar caras en tiempo real
  const detectFacesInVideo = async () => {
    if (videoRef.current) {
      const detections = await detectFaces(videoRef.current);  // Usar la función importada
      setFacesDetected(detections.length);
      const canvas = faceapi.createCanvasFromMedia(videoRef.current);
      document.body.append(canvas);
      faceapi.matchDimensions(canvas, videoRef.current);
      canvas?.drawDetections(detections);
      canvas?.drawFaceLandmarks(detections);
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
      <h1>Reconocimiento Facial</h1>
      <Camera videoRef={videoRef} />
      {facesDetected > 0 && <div>¡Cara detectada!</div>}
      {facesDetected === 0 && <div>No se detectaron caras.</div>}
      <button className="login-button" onClick={() => navigate("/manual-login")}>
        Manual Login
      </button>
    </div>
  );
}

export default CameraPage;
