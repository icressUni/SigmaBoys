// src/componentes/Login.tsx
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import styles from "../styles/Login.module.css";
import Boton from "./Button";
import { useLanguage } from "../lenguage/LenguageContext";

const Login: React.FC = () => {
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();
  const { translations } = useLanguage();

  const handleLogin = () => {
    if (password === "1234") {
      navigate("/admin-dashboard"); // o el destino que tú quieras
    } else {
      setError(translations.loginError);
    }
  };

  return (
    <div className={`${styles.loginContainer} ${styles.formContainer}`}>
      <h2>{translations.loginTitle}</h2>
      <form onSubmit={(e) => e.preventDefault()}>
        <div className={styles.formGroup}>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className={styles.formControl}
            placeholder={translations.loginPlaceholder}
            required
            autoComplete="current-password"
          />
        </div>
        {error && <div className={styles.alert}>{error}</div>}
        <Boton texto={translations.loginButton} onClick={handleLogin} />
      </form>
    </div>
  );
};

export default Login;
