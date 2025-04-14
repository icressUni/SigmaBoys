import { useNavigate } from "react-router-dom";
import "../diseños/Camera.css"; // Reutilizamos el mismo CSS para estilos consistentes

function Home() {
  const navigate = useNavigate();

  return (
    <div className="container">
      <h1>Bienvenido</h1>
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
