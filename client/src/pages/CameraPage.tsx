import React, { useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import Camera from '../componentes/Camara';

function CameraPage() {
  const navigate = useNavigate();
  const videoRef = useRef<HTMLVideoElement | null>(null);

  return (
    <div className="camera-page">
      <div className="camera-content">
        <h1>Sistema de Reconocimiento Facial</h1>

        {/* Solo mostrar la cámara */}
        <div className="video-container">
          <Camera videoRef={videoRef} onError={(err) => console.error(err)} />
        </div>

        <button className="login-button" onClick={() => navigate("/manual-login")}>
          Iniciar sesión manualmente
        </button>
      </div>
    </div>
  );
}

export default CameraPage;
