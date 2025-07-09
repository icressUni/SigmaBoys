import React from "react";
import { useLanguage } from "../lenguage/LenguageContext";
import styles from "../styles/LenguageSelector.module.css";

const LanguageSelector: React.FC = () => {
  const { language, setLanguage } = useLanguage();

  const handleLanguageChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setLanguage(e.target.value);
  };

  return (
    <select
      value={language}
      onChange={handleLanguageChange}
      className={styles.selector}
    >
      <option value="es">🇪🇸 Español</option>
      <option value="en">🇬🇧 English</option>
    </select>
  );
};

export default LanguageSelector;
