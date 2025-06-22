// src/App.tsx
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Home from "@pages/Home";
import AdminDashboard from "@pages/AdminDashboard";
import Header from "@components/Header";
import LoadingScreen from "@components/LoadingScreen";
import { useEffect, useState } from "react";
import { LanguageProvider } from "./lenguage/LenguageContext";
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
    <LanguageProvider>
      <Router>
        <div className="flex flex-col min-h-screen">
          <Header />
          <main className="flex-grow pt-16">
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
