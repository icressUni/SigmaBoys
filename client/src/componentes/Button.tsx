// src/componentes/Boton.tsx
import React from "react";
import { useNavigate } from "react-router-dom";
import styles from "../styles/Button.module.css"; // Asegúrate de que el nombre coincida exactamente

interface BotonProps {
  texto?: string;
  destino?: string;
  onClick?: () => void;
}

const Boton: React.FC<BotonProps> = ({
  texto = "Minijuego",
  destino = "/minijuego",
  onClick,
}) => {
  const navigate = useNavigate();

  const handleClick = () => {
    if (onClick) {
      onClick();
    } else if (destino) {
      navigate(destino);
    }
  };

  return (
    <button onClick={handleClick} className={styles.btn}>
      {texto}
    </button>
  );
};

export default Boton;
