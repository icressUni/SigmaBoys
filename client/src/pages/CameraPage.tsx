import { useEffect, useRef } from "react";
import "../diseños/Camera.css";

function CameraPage() {
  const videoRef = useRef<HTMLVideoElement | null>(null);

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
      <button className="login-button">Manual Login</button>
    </div>
  );
}

export default CameraPage;
