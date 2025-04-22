// src/pages/ManualLoginPage.tsx
import React from "react";
import Login from "../componentes/Login";

function ManualLoginPage() {
  return (
    <div style={{
      backgroundColor: "#e3f2fd", // Azul claro de fondo
      minHeight: "100vh",
      display: "flex",
      alignItems: "center",
      justifyContent: "center"
    }}>
      <Login backgroundColor="#ffffff" />
    </div>
  );
}

export default ManualLoginPage;
