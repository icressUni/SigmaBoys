import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import CameraPage from "./pages/CameraPage";
import LoginManual from "./pages/LoginManual";
import "./index.css";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/lab-tracker" element={<CameraPage />} />
        <Route path="/manual-login" element={<LoginManual />} />
      </Routes>
    </Router>
  );
}

export default App;
