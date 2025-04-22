import React from "react";
import { useNavigate } from "react-router-dom";
import Boton from "../componentes/Boton";

function Home() {
  const navigate = useNavigate();

  const handleAdminClick = () => {
    navigate("/manual-login"); // Redirige al login
  };

  return (
    <main className="centered">
      <div className="container">
        <h1>Bienvenido</h1>
        <div className="button-group">
          <Boton texto="Admin" onClick={handleAdminClick} />
          <Boton texto="Lab Tracker" destino="/lab-tracker" />
        </div>
      </div>
    </main>
  );
}

export default Home;
