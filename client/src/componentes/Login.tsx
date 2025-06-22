import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import styles from "../styles/Login.module.css";
import { useLanguage } from "../lenguage/LenguageContext";
import Boton from "../componentes/Button"; // Asegúrate que este es el componente correcto

const Login: React.FC = () => {
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();
  const { translations } = useLanguage();

  const handleLogin = () => {
    setError(null);

    const validPassword = "123456"; // Contraseña válida hardcodeada

    if (password === validPassword) {
      navigate("/admin-dashboard"); // Navegar al dashboard si es correcta
    } else {
      setError(translations.loginError || "Contraseña incorrecta");
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
