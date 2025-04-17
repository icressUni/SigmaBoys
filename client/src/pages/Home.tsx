import { useNavigate } from "react-router-dom";
import "../diseños/Camera.css"; // Reutilizamos el mismo CSS para estilos consistentes

function Home() {
  const navigate = useNavigate();

  return (
    <div className="container">
      <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
        <h1>Bienvenido</h1>
        <button onClick={() => navigate("/test_DB")}>Nuevo Botón</button>
      </div>
      <div className="button-group">
        <button className="login-button" onClick={() => alert("Sección Admin no implementada aún")}>
          Admin
        </button>
        <button className="login-button" onClick={() => navigate("/lab-tracker")}>
          Lab Tracker
        </button>
      </div>
    </div>
  );
}

export default Home;
