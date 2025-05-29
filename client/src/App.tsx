// src/App.tsx
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Home from "@pages/Home";
import AdminDashboard from "@pages/AdminDashboard";
import Header from "@components/Header";
import LoadingScreen from "@components/LoadingScreen";
import { useEffect, useState } from "react";
import { LanguageProvider } from "./lenguage/LenguageContext"; // ✅ Importar el contexto de idioma
import "./styles/index.css"; // Importar estilos globales

function App() {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setLoading(false);
    }, 1500);
    return () => clearTimeout(timer);
  }, []);

  if (loading) {
    return <LoadingScreen />;
  }

  return (
    <LanguageProvider> {/* ✅ Proveedor del contexto de idioma envuelve toda la app */}
      <Router>
        <div className="flex flex-col min-h-screen">
          <Header />
          <main className="flex-grow pt-16"> {/* pt-16 para no tapar con el header fijo */}
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/admin" element={<Navigate to="/" replace />} />
              <Route path="/admin-dashboard" element={<AdminDashboard />} />
            </Routes>
          </main>
        </div>
      </Router>
    </LanguageProvider>
  );
}

export default App;
