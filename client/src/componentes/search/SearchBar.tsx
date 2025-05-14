import React, { useState, useRef, useEffect } from "react";
import "./SearchBar.css";

interface SearchBarProps {
  data: any[];
  onSearchResults: (results: any[]) => void;
  categories?: string[];
  isDropdownOpen: boolean;
  setIsDropdownOpen: (isOpen: boolean) => void;
  selectedCategory: string;
}

const SearchBar: React.FC<SearchBarProps> = ({ 
  data, 
  onSearchResults,
  isDropdownOpen,
  setIsDropdownOpen,
  selectedCategory
}) => {
  const [searchTerm, setSearchTerm] = useState("");
  const dropdownRef = useRef<HTMLDivElement>(null);

  /*useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsDropdownOpen(false);
      }
    };
    
    if (isDropdownOpen) {
      document.addEventListener("mousedown", handleClickOutside);
    }
    
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [isDropdownOpen, setIsDropdownOpen]);*/

  const handleSearch = () => {
    let results;
    
    if (selectedCategory === "Todos") {
      results = data.filter((item) =>
        Object.values(item).some((value) =>
          String(value).toLowerCase().includes(searchTerm.toLowerCase())
        )
      );
    } else {
      const property = selectedCategory.toLowerCase();
      
      results = data.filter((item) =>
        String(item[property]).toLowerCase().includes(searchTerm.toLowerCase())
      );
    }
    
    onSearchResults(results);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      handleSearch();
    }
  };

  const toggleDropdown = (e: React.MouseEvent) => {
    e.stopPropagation();
    setIsDropdownOpen(!isDropdownOpen);
  };

  return (
    <div className="search-container">
      <div className="search-bar-wrapper">
        <div className="search-bar-inner" ref={dropdownRef}>
          <div 
            className="dropdown-button" 
            onClick={toggleDropdown}
            aria-expanded={isDropdownOpen}
            role="button"
            aria-haspopup="listbox"
          >
            <span>{selectedCategory}</span>
            <svg 
              xmlns="http://www.w3.org/2000/svg" 
              width="16" 
              height="16" 
              viewBox="0 0 24 24" 
              fill="none" 
              stroke="currentColor" 
              strokeWidth="2"
              className={isDropdownOpen ? "dropdown-icon-open" : "dropdown-icon"}
            >
              <path d="M6 9l6 6 6-6" />
            </svg>
          </div>
          
          <input
            type="text"
            placeholder="Buscar..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            onKeyPress={handleKeyPress}
            className="search-input-embedded"
          />
          
          <button className="search-button" onClick={handleSearch}>
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="11" cy="11" r="8" />
              <path d="M21 21l-4.35-4.35" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
};

export default SearchBar;