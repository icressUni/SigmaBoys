// src/componentes/LoadingScreen.tsx
import React from "react";
import "../styles/loading.css"; // Asegúrate de importar tu nuevo CSS acá

const LoadingScreen: React.FC = () => {
  return (
    <div className="loading-screen">
      <div className="hourglass"></div>
      <p className="loading-text">Cargando...</p>
    </div>
  );
};

export default LoadingScreen;
