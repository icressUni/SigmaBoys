import React, { useContext, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../App";
import Login from "../componentes/Login";

function Home() {
  const { isAuthenticated } = useContext(AuthContext);
  const navigate = useNavigate();

  useEffect(() => {
    // Solo redirigir si el usuario está autenticado
    // y evitar redirecciones múltiples
    if (isAuthenticated) {
      console.log("Usuario autenticado, redirigiendo al dashboard");
      navigate("/admin-dashboard", { replace: true });
    }
  }, [isAuthenticated, navigate]);

  // No mostrar el componente Login si el usuario ya está autenticado
  // para evitar parpadeos
  if (isAuthenticated) {
    return null; // O puedes retornar un LoadingScreen aquí
  }

  return (
    <main className="centered">
      <Login backgroundColor="#ffffff" mode="admin" />
    </main>
  );
}

export default Home;