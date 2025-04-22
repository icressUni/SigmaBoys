import { useNavigate } from "react-router-dom";
import React from "react";

interface BotonProps {
  texto?: string;
  destino?: string;
  onClick?: () => void;
}

const Boton: React.FC<BotonProps> = ({ texto = "Minijuego", destino = "/minijuego", onClick }) => {
  const navigate = useNavigate();

  const handleClick = () => {
    if (onClick) {
      onClick(); // ejecuta onClick personalizado si está definido
    } else if (destino) {
      navigate(destino); // o navega al destino
    }
  };

  return (
    <button
      onClick={handleClick}
      className="btn" // Usamos la clase 'btn' para los estilos globales
    >
      {texto}
    </button>
  );
};

export default Boton;
