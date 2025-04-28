// src/App.tsx
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "@pages/Home";
import CameraPage from "@pages/CameraPage";
import LoginPage from "@pages/LoginPage";
import AdminDashboard from "@pages/AdminDashboard";
import Header from "@components/Header";
import LoadingScreen from "@components/LoadingScreen";
import { useEffect, useState } from "react";
import "./styles/index.css";

function App() {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simula un pequeño tiempo de carga (ej: 1.5 segundos)
    const timer = setTimeout(() => {
      setLoading(false);
    }, 1500); // puedes ajustar el tiempo aquí si quieres

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
            <Route path="/admin-dashboard" element={<AdminDashboard />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
