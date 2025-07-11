import React, { useState, useEffect, useContext } from "react";
import { useNavigate } from "react-router-dom";
import styles from "../styles/Login.module.css";
import { useLanguage } from "../lenguage/LenguageContext";
import { AuthContext } from "../App";
import Boton from "../componentes/Button";

interface LoginProps {
  backgroundColor?: string;
  mode?: string;
}

const Login: React.FC<LoginProps> = ({ backgroundColor, mode }) => {
  const [correo, setCorreo] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();
  const { translations } = useLanguage();
  const { isAuthenticated, login } = useContext(AuthContext);

  useEffect(() => {
    if (isAuthenticated) {
      navigate("/admin-dashboard", { replace: true });
    }
  }, [isAuthenticated, navigate]);

  const handleLogin = async () => {
    if (isLoading) return;
    
    setError(null);
    setIsLoading(true);

    // Validación básica
    if (!correo.trim() || !password.trim()) {
      setError("Por favor, complete todos los campos");
      setIsLoading(false);
      return;
    }

    // Validación de email básica
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(correo)) {
      setError("Por favor, ingrese un correo electrónico válido");
      setIsLoading(false);
      return;
    }

    // ✅ CORREGIDO: Usar import.meta.env en lugar de process.env
    const API_URL = import.meta.env.VITE_API_URL || `http://${window.location.hostname}:8000`;

    console.log("Intentando login con:", { correo, API_URL });

    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 15000);

      const res = await fetch(`${API_URL}/api/login`, {
        method: "POST",
        headers: { 
          "Content-Type": "application/json",
          "Accept": "application/json"
        },
        body: JSON.stringify({ correo, contrasena: password }),
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      console.log("Respuesta del servidor:", res.status, res.statusText);

      // Verificar si la respuesta es JSON válida
      const contentType = res.headers.get("content-type");
      if (!contentType || !contentType.includes("application/json")) {
        const textResponse = await res.text();
        console.error("Respuesta no JSON:", textResponse);
        throw new Error("Respuesta del servidor no válida");
      }

      if (res.status === 200) {
        const data = await res.json();
        console.log("Datos recibidos:", data);
        
        if (data.token) {
          console.log("Token recibido, iniciando sesión");
          login(data.token);
          // Dar tiempo al contexto para actualizar
          setTimeout(() => {
            navigate("/admin-dashboard", { replace: true });
          }, 100);
        } else {
          setError("Error en la respuesta del servidor: token no encontrado");
        }
      } else if (res.status === 401) {
        const errorData = await res.json().catch(() => ({}));
        setError(errorData.message || translations.loginError || "Correo o contraseña incorrectos");
      } else if (res.status === 500) {
        const errorData = await res.json().catch(() => ({}));
        setError(errorData.message || "Error interno del servidor. Intente más tarde.");
      } else {
        const errorData = await res.json().catch(() => ({}));
        setError(errorData.message || `Error del servidor (${res.status}). Intente más tarde.`);
      }
    } catch (error: any) {
      console.error('Login error:', error);
      
      if (error.name === 'AbortError') {
        setError("Tiempo de espera agotado. Verifique su conexión a internet.");
      } else if (error.message.includes('Failed to fetch')) {
        setError("No se pudo conectar al servidor. Verifique su conexión a internet.");
      } else if (error.message.includes('JSON')) {
        setError("Error en la comunicación con el servidor. Intente nuevamente.");
      } else {
        setError("Error de conexión. Verifique su red e intente nuevamente.");
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !isLoading) {
      handleLogin();
    }
  };

  return (
    <div 
      className={`${styles.loginContainer} ${styles.formContainer}`}
      style={{ backgroundColor: backgroundColor || "#ffffff" }}
    >
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
            onKeyPress={handleKeyPress}
            className={styles.formControl}
            placeholder={translations.emailPlaceholder || "Correo electrónico"}
            required
            autoComplete="username"
            disabled={isLoading}
            aria-describedby="email-error"
            aria-label="Correo electrónico"
            inputMode="email"
          />
        </div>

        <div className={styles.formGroup}>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            onKeyPress={handleKeyPress}
            className={styles.formControl}
            placeholder={translations.loginPlaceholder || "Contraseña"}
            required
            autoComplete="current-password"
            disabled={isLoading}
            aria-describedby="password-error"
            aria-label="Contraseña"
          />
        </div>

        {error && (
          <div className={styles.alert} role="alert" id="login-error">
            {error}
          </div>
        )}
        
        <Boton 
          texto={isLoading ? "Cargando..." : (translations.loginButton || "Entrar")} 
          type="submit"
          disabled={isLoading}
          aria-label={isLoading ? "Cargando" : "Iniciar sesión"}
        />
      </form>
    </div>
  );
};

export default Login;