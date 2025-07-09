import React, { useState, useEffect } from "react";
import styles from "../styles/SearchBar.module.css";

interface SearchBarProps {
  data: any[];
  onSearchResults: (results: any[]) => void;
  selectedCategory: string;
  placeholder: string;
}

const SearchBar: React.FC<SearchBarProps> = ({
  data,
  onSearchResults,
  selectedCategory,
  placeholder,
}) => {
  const [searchTerm, setSearchTerm] = useState("");

  useEffect(() => {
    let results = data;

    const search = searchTerm.trim().toLowerCase();
    const category = selectedCategory.toLowerCase();

    if (search !== "") {
      if (category === "todos") {
        results = data.filter((item) =>
          Object.values(item).some((value) =>
            String(value).toLowerCase().includes(search)
          )
        );
      } else if (category === "nombre") {
        results = data.filter((item) => {
          const nombre = item.nombre?.toLowerCase() || "";
          const apellido = item.apellido?.toLowerCase() || "";
          return nombre.includes(search) || apellido.includes(search);
        });
      } else {
        results = data.filter((item) =>
          String(item[category] || "")
            .toLowerCase()
            .includes(search)
        );
      }
    }

    onSearchResults(results);
  }, [searchTerm, selectedCategory, data]); // quitamos onSearchResults para evitar bucle

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value);
  };

  const handleResetSearch = () => {
    setSearchTerm("");
    onSearchResults(data); // Reset manual
  };

  return (
    <div className={styles.searchContainer}>
      <div className={styles.searchBarWrapper}>
        <div className={styles.searchBarInner}>
          <input
            type="text"
            placeholder={placeholder}
            value={searchTerm}
            onChange={handleInputChange}
            className={styles.searchInput}
            aria-label="Buscar"
          />
          <button
            className={styles.searchButton}
            onClick={handleResetSearch}
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
