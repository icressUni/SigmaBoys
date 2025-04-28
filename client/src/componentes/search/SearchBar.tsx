import React, { useState } from "react";
import Boton from "../Boton.tsx";
import "./SearchBar.css";

interface SearchBarProps {
  data: any[];
  onSearchResults: (results: any[]) => void;
}

const SearchBar: React.FC<SearchBarProps> = ({ data, onSearchResults }) => {
  const [searchTerm, setSearchTerm] = useState("");

  const handleSearch = () => {
    const results = data.filter((item) =>
      Object.values(item).some((value) =>
        String(value).toLowerCase().includes(searchTerm.toLowerCase())
      )
    );
    onSearchResults(results);
  };

  // Added key press handler for better UX
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      handleSearch();
    }
  };

  return (
    <div className="search-container">
      <div className="search-bar">
        <input
          type="text"
          placeholder="Buscar..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          onKeyPress={handleKeyPress}
          className="search-input"
        />
        <Boton texto="Buscar" onClick={handleSearch} />
      </div>
    </div>
  );
};

export default SearchBar;
