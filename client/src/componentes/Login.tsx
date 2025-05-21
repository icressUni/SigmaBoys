import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/login.css";
import data from "../data/users.json"; // contiene users y adminPassword

interface LoginProps {
  backgroundColor: string;
  mode?: "admin" | "user"; // puede ser login normal o solo contraseña
}

const Login: React.FC<LoginProps> = ({ backgroundColor, mode = "user" }) => {
  const [username, setUsername] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const navigate = useNavigate();

  const handleLogin = () => {
    if (mode === "admin") {
      if (password === data.adminPassword) {
        navigate("/admin-dashboard");
      } else {
        setErrorMessage("Clave incorrecta");
      }
      return;
    }

    const user = data.users.find(
      (u) => u.username === username && u.password === password
    );

    if (user) {
      navigate("/lab-tracker");
    } else {
      setErrorMessage("Usuario o contraseña incorrectos");
    }
  };

  return (
    <div className="login-container form-container" style={{ backgroundColor }}>
      <h2>{mode === "admin" ? "Clave de Administrador" : "Iniciar sesión"}</h2>
      <form onSubmit={(e) => e.preventDefault()}>
        {mode !== "admin" && (
          <div className="form-group">
            <label htmlFor="username" className="form-label">Usuario</label>
            <input
              type="text"
              id="username"
              className="form-control"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
        )}
        <div className="form-group">
          <label htmlFor="password" className="form-label">
            {mode === "admin" ? "Clave" : "Contraseña"}
          </label>
          <input
            type="password"
            id="password"
            className="form-control"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        {errorMessage && <div className="alert">{errorMessage}</div>}
        <button type="button" className="btn" onClick={handleLogin}>
          {mode === "admin" ? "Ingresar al Panel" : "Iniciar sesión"}
        </button>
      </form>
    </div>
  );
};

export default Login;
