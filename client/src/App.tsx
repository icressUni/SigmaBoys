// src/App.tsx
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "@pages/Home";
import CameraPage from "@pages/CameraPage";
import LoginPage from "@pages/LoginPage";
import AdminDashboard from "@pages/AdminDashboard";
import AdminAccessPage from "@pages/AdminAccessPage";
import RegistroRostro from "@pages/RegistroRostro";  // <-- Importa la página RegistroRostro
import Header from "@components/Header";
import LoadingScreen from "@components/LoadingScreen";
import { useEffect, useState } from "react";
import "./styles/index.css";

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
    <Router>
      <div className="flex flex-col min-h-screen">
        <Header />
        <main className="flex-grow">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/lab-tracker" element={<CameraPage />} />
            <Route path="/manual-login" element={<LoginPage />} />
            <Route path="/admin" element={<AdminAccessPage />} />
            <Route path="/admin-dashboard" element={<AdminDashboard />} />
            <Route path="/registro-rostro" element={<RegistroRostro />} /> {/* Aquí agregas la ruta */}
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
