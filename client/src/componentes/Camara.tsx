import { useEffect, useRef } from "react";

interface CameraProps {
  videoRef?: React.RefObject<HTMLVideoElement>;
  onError: (err: string) => void;
}

const Camera: React.FC<CameraProps> = ({ videoRef, onError }) => {
  const internalVideoRef = useRef<HTMLVideoElement | null>(null);
  const streamRef = useRef<MediaStream | null>(null);

  // Usamos el videoRef externo si existe, sino el interno
  const videoElementRef = videoRef || internalVideoRef;

  useEffect(() => {
    const getCamera = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        if (videoElementRef.current) {
          videoElementRef.current.srcObject = stream;
        }
        streamRef.current = stream;
      } catch (err) {
        onError("Error al acceder a la cámara");
        console.error("Error al acceder a la cámara:", err);
      }
    };

    getCamera();

    return () => {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop());
      }
    };
  }, [onError, videoElementRef]);

  return (
    <video ref={videoElementRef} autoPlay playsInline className="video-element flipped" />
  );
};

export default Camera;
