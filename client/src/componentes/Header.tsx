// src/componentes/Header.tsx
import { useNavigate, useLocation } from "react-router-dom";

const Header: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const handleGoBack = () => navigate(-1);
  const handleGoHome = () => navigate("/");

  return (
    <header className="bg-blue-600 text-white py-2 px-4 flex justify-between items-center fixed top-0 left-0 w-full">
      {/* Zona izquierda - Navegación */}
      <div className="flex items-center space-x-3">
        {location.pathname !== "/" && (
          <button
            onClick={handleGoBack}
            className="hover:bg-blue-700 p-1 rounded transition-colors"
            aria-label="Volver atrás"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M19 12H5M12 19l-7-7 7-7" />
            </svg>
          </button>
        )}
        
        <button
          onClick={handleGoHome}
          disabled={location.pathname === "/"}
          className={`hover:bg-blue-700 p-1 rounded transition-colors ${
            location.pathname === "/" ? "opacity-50 cursor-not-allowed" : ""
          }`}
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
            <polyline points="9 22 9 12 15 12 15 22" />
          </svg>
        </button>
      </div>
    </header>
  );
};

export default Header;
