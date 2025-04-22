// src/App.tsx
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "@pages/Home";
import CameraPage from "@pages/CameraPage";
import LoginPage from "@pages/LoginPage";
import AdminDashboard from "@pages/AdminDashboard";
import Header from "@components/Header";
import "./styles/index.css";

function App() {
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
