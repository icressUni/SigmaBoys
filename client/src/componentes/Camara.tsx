// src/componentes/Camara.tsx
import { useEffect, useRef } from "react";

interface CameraProps {
  onError: (err: string) => void;
}

const Camera: React.FC<CameraProps> = ({ onError }) => {
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const streamRef = useRef<MediaStream | null>(null); // Guardar el stream para detenerlo

  useEffect(() => {
    const getCamera = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
        streamRef.current = stream;
      } catch (err) {
        onError("Error al acceder a la cámara");
        console.error("Error al acceder a la cámara:", err);
      }
    };

    getCamera();

    // Limpieza: detener cámara al desmontar el componente
    return () => {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop());
      }
    };
  }, [onError]);

  return (
    <div className="video-container">
      <video ref={videoRef} autoPlay playsInline className="video-element flipped" />
    </div>
  );
};

export default Camera;
