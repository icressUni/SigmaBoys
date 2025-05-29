import React from "react";
import { useNavigate, useLocation } from "react-router-dom";
import styles from "../styles/Header.module.css";
import LanguageSelector from "./LenguageSelector";
import { useLanguage } from "../lenguage/LenguageContext";

const Header: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { translations } = useLanguage();

  const handleGoBack = () => navigate(-1);
  const handleGoHome = () => navigate("/");

  return (
    <header className={styles.header}>
      {/* Zona izquierda: solo botones */}
      <div className={styles.left}>
        {location.pathname !== "/" && (
          <button
            onClick={handleGoBack}
            className={styles.iconButton}
            aria-label={translations.back}
          >
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M19 12H5M12 19l-7-7 7-7" />
            </svg>
          </button>
        )}

        <button
          onClick={handleGoHome}
          disabled={location.pathname === "/"}
          className={`${styles.iconButton} ${location.pathname === "/" ? styles.disabled : ""}`}
          aria-label={translations.home}
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
            <polyline points="9 22 9 12 15 12 15 22" />
          </svg>
        </button>
      </div>

      {/* Centro */}
      <div className={styles.center}>
        {translations.welcome}
      </div>

      {/* Derecha: Language Selector */}
      <div className={styles.right}>
        <div className={styles.languageSelectorWrapper}>
          <LanguageSelector />
        </div>
      </div>
    </header>
  );
};

export default Header;
