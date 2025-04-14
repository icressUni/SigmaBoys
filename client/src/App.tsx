import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import CameraPage from "./pages/CameraPage";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/lab-tracker" element={<CameraPage />} />
      </Routes>
    </Router>
  );
}

export default App;
