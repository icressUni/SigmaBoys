// src/componentes/Boton.tsx
import React from "react";
import styles from "../styles/Button.module.css";

interface BotonProps {
  texto: string;
  onClick?: () => void;
  type?: "button" | "submit" | "reset"; // Permitir definir el tipo de botón
}

const Boton = ({ texto, onClick, type = "button" }: BotonProps) => {
  return (
    <button onClick={onClick} type={type} className={styles.boton}>
      {texto}
    </button>
  );
};

export default Boton;
