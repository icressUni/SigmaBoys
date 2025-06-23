import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import styles from "../styles/Login.module.css";
import { useLanguage } from "../lenguage/LenguageContext";
import Boton from "../componentes/Button";

const Login: React.FC = () => {
  const [correo, setCorreo] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();
  const { translations } = useLanguage();

  // ✅ Redirigir automáticamente si ya hay token
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      navigate("/admin-dashboard");
    }
  }, [navigate]);

  const handleLogin = async () => {
    setError(null);

    try {
      const res = await fetch("http://localhost:8000/api/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ correo, contrasena: password }),
      });

      if (res.status === 200) {
        const data = await res.json();
        localStorage.setItem("token", data.token);
        navigate("/admin-dashboard");
      } else if (res.status === 401) {
        setError(translations.loginError || "Correo o contraseña incorrectos");
      } else {
        setError("Error en el servidor, intente más tarde");
      }
    } catch (error) {
      setError("Error de conexión");
      console.error(error);
    }
  };

  return (
    <div className={`${styles.loginContainer} ${styles.formContainer}`}>
      <h2>{translations.loginTitle || "Iniciar Sesión"}</h2>
      <form
        onSubmit={(e) => {
          e.preventDefault();
          handleLogin();
        }}
      >
        <div className={styles.formGroup}>
          <input
            type="email"
            value={correo}
            onChange={(e) => setCorreo(e.target.value)}
            className={styles.formControl}
            placeholder={translations.emailPlaceholder || "Correo electrónico"}
            required
            autoComplete="username"
          />
        </div>

        <div className={styles.formGroup}>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className={styles.formControl}
            placeholder={translations.loginPlaceholder || "Contraseña"}
            required
            autoComplete="current-password"
          />
        </div>

        {error && <div className={styles.alert}>{error}</div>}
        <Boton texto={translations.loginButton || "Entrar"} type="submit" />
      </form>
    </div>
  );
};

export default Login;
