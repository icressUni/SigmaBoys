import React, { useState, useEffect } from "react";
import styles from "../styles/SearchBar.module.css";

interface SearchBarProps {
  data: any[];
  onSearchResults: (results: any[]) => void;
  selectedCategory: string;
  placeholder: string; // Texto del placeholder traducido
}

const SearchBar: React.FC<SearchBarProps> = ({
  data,
  onSearchResults,
  selectedCategory,
  placeholder,
}) => {
  const [searchTerm, setSearchTerm] = useState("");

  useEffect(() => {
    let results;

    if (searchTerm.trim() === "") {
      results = data;
    } else if (selectedCategory.toLowerCase() === "todos") {
      results = data.filter((item) =>
        Object.values(item).some((value) =>
          String(value)
            .toLowerCase()
            .includes(searchTerm.trim().toLowerCase())
        )
      );
    }

    // 🔧 Modificación específica para que el filtro "Nombre" busque en nombre y apellido
    else if (selectedCategory.toLowerCase() === "nombre") {
      results = data.filter((item) => {
        const nombre = item.nombre?.toLowerCase() || "";
        const apellido = item.apellido?.toLowerCase() || "";
        const search = searchTerm.trim().toLowerCase();
        return (
          nombre.includes(search) || apellido.includes(search)
        );
      });
    }

    // Resto de filtros por propiedad
    else {
      const key = selectedCategory.toLowerCase();
      results = data.filter((item) =>
        String(item[key])
          .toLowerCase()
          .includes(searchTerm.trim().toLowerCase())
      );
    }

    onSearchResults(results);
  }, [searchTerm, selectedCategory, data, onSearchResults]);

  return (
    <div className={styles.searchContainer}>
      <div className={styles.searchBarWrapper}>
        <div className={styles.searchBarInner}>
          <input
            type="text"
            placeholder={placeholder}
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className={styles.searchInput}
            aria-label="Buscar"
          />
          <button
            className={styles.searchButton}
            onClick={() => onSearchResults(data)} // Botón puede resetear búsqueda si quieres
            aria-label="Buscar"
            title="Buscar"
            type="button"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <circle cx="11" cy="11" r="8" />
              <line x1="21" y1="21" x2="16.65" y2="16.65" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
};

export default SearchBar;
