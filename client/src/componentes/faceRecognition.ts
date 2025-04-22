// src/utils/faceRecognition.ts

export const loadFaceModels = async () => {
    const MODEL_URL = '/models';
  
    await faceapi.nets.ssdMobilenetv1.loadFromUri(MODEL_URL);
    // No cargamos faceLandmark68Net ni faceRecognitionNet si solo queremos detección de caras
  };
  
  export const detectFaces = async (videoElement: HTMLVideoElement) => {
    const detections = await faceapi.detectAllFaces(
      videoElement,
      new faceapi.SsdMobilenetv1Options({ minConfidence: 0.5 })
    );
  
    return detections;
  };  