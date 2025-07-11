import React, { useContext } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import styles from "../styles/Header.module.css";
import LanguageSelector from "./LenguageSelector";
import { useLanguage } from "../lenguage/LenguageContext";
import { AuthContext } from "../App";

const Header: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { translations } = useLanguage();
  const { isAuthenticated, logout } = useContext(AuthContext);

  const handleLogout = () => {
    // Usar la función logout del contexto en lugar de manipular localStorage directamente
    logout();
    // Navegación inmediata sin esperar
    navigate("/", { replace: true });
  };

  const handleGoBack = () => navigate(-1);

  return (
    <header className={styles.header}>
      {/* Zona izquierda: Logout o Volver */}
      <div className={styles.left}>
        {isAuthenticated ? (
          <button
            onClick={handleLogout}
            className={styles.iconButton}
            aria-label={translations.logout || "Cerrar sesión"}
            title={translations.logout || "Cerrar sesión"}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="22"
              height="22"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
              <polyline points="16 17 21 12 16 7" />
              <line x1="21" y1="12" x2="9" y2="12" />
            </svg>
          </button>
        ) : (
          location.pathname !== "/" && (
            <button
              onClick={handleGoBack}
              className={styles.iconButton}
              aria-label={translations.back}
              title={translations.back}
            >
              <svg
                width="22"
                height="22"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
              >
                <path d="M19 12H5M12 19l-7-7 7-7" />
              </svg>
            </button>
          )
        )}
      </div>

      {/* Centro */}
      <div className={styles.center}>{translations.welcome}</div>

      {/* Derecha */}
      <div className={styles.right}>
        <div className={styles.languageSelectorWrapper}>
          <LanguageSelector />
        </div>
      </div>
    </header>
  );
};

export default Header;