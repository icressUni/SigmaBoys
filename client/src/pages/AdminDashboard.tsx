// pages/AdminDashboard.tsx
import { useState, useRef } from "react";
import alumnosData from "../data/alumnos.json";
import fotosData from "../data/fotos.json";
import asistenciasData from "../data/asistencias.json";

import SearchBar from "../componentes/SearchBar";
import DropdownBar from "../componentes/DropdownBar";
import CardGrid from "../componentes/CardGrid";
import styles from "../styles/AdminDashboard.module.css";
import { useLanguage } from "../lenguage/LenguageContext";

const AdminDashboard = () => {
  const { translations } = useLanguage();

  const categories = [
    translations.category_Todos || "Todos",
    translations.category_Nombre || "Nombre",
    translations.category_Correo || "Correo",
    translations.category_Especialidad || "Especialidad",
  ];

  const [searchResults, setSearchResults] = useState(alumnosData);
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState(categories[0]);

  const dropdownRef = useRef<HTMLDivElement>(null);

  const handleSearchResults = (results: typeof alumnosData) => {
    setSearchResults(results);
  };

  const handleSelectCategory = (category: string) => {
    setSelectedCategory(category);
    setIsDropdownOpen(false);
  };

  return (
    <div className={styles.container}>
      <h1 className={styles.header}>{translations.welcome}</h1>

      <div ref={dropdownRef} className={styles.controlsRow}>
        <div className={styles.dropdownWrapper}>
          <DropdownBar
            categories={categories}
            isOpen={isDropdownOpen}
            setIsOpen={setIsDropdownOpen}
            selectedCategory={selectedCategory}
            onSelectCategory={handleSelectCategory}
          />
        </div>

        <div className={styles.searchWrapper}>
          <SearchBar
            data={alumnosData}
            onSearchResults={handleSearchResults}
            selectedCategory={selectedCategory}
            placeholder={translations.searchPlaceholder || "Buscar..."}
          />
        </div>
      </div>

      <div className={styles.results}>
        {searchResults.length > 0 ? (
          <CardGrid
            data={searchResults}
            fotos={fotosData}
            asistencias={asistenciasData}
            columnCount={3}
            gridHeight="auto"
          />
        ) : (
          <p>{translations.noResults || "No se encontraron resultados."}</p>
        )}
      </div>
    </div>
  );
};

export default AdminDashboard;
