// src/componentes/Login.tsx
import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/login.css";
import usuarios from "../data/users.json";

interface LoginProps {
  backgroundColor: string;
}

const Login: React.FC<LoginProps> = ({ backgroundColor }) => {
  const [username, setUsername] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const navigate = useNavigate();

  const handleLogin = () => {
    const user = usuarios.find(
      (u) => u.username === username && u.password === password
    );

    if (user) {
      if (user.role === "admin") {
        navigate("/admin-dashboard");
      } else {
        navigate("/lab-tracker");
      }
    } else {
      setErrorMessage("Usuario o contraseña incorrectos");
    }
  };

  return (
    <div className="login-container form-container" style={{ backgroundColor }}>
      <h2>Iniciar sesión</h2>
      <form onSubmit={(e) => e.preventDefault()}>
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
        <div className="form-group">
          <label htmlFor="password" className="form-label">Contraseña</label>
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
          Iniciar sesión
        </button>
      </form>
    </div>
  );
};

export default Login;
