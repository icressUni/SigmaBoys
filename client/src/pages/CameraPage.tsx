import { useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import "../diseños/Camera.css";

function CameraPage() {
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const getCamera = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      } catch (err) {
        console.error("Error al acceder a la cámara:", err);
      }
    };

    getCamera();
  }, []);

  return (
    <div className="container">
      <h1>Reconocimiento Facial</h1>
      <div className="video-container">
        <video ref={videoRef} autoPlay playsInline className="video-element" />
      </div>
      <button className="login-button" onClick={() => navigate("/manual-login")}>
        Manual Login
      </button>
    </div>
  );
}

export default CameraPage;
