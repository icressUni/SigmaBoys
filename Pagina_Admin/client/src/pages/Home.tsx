import React, { useContext, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../App";
import Login from "../componentes/Login";

function Home() {
  const { isAuthenticated } = useContext(AuthContext);
  const navigate = useNavigate();

  useEffect(() => {
    if (isAuthenticated) {
      navigate("/admin-dashboard", { replace: true });
    }
  }, [isAuthenticated, navigate]);

  return (
    <main className="centered">
      <Login backgroundColor="#ffffff" mode="admin" />
    </main>
  );
}

export default Home;