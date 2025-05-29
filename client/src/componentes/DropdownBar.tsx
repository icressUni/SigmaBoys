// componentes/DropdownBar.tsx
import React, { useEffect, useRef } from "react";
import styles from "../styles/DropdownBar.module.css";

interface DropdownBarProps {
  isOpen: boolean;
  setIsOpen: (open: boolean) => void;
  selectedCategory: string;
  onSelectCategory: (category: string) => void;
  categories: string[];
}

const DropdownBar: React.FC<DropdownBarProps> = ({
  isOpen,
  setIsOpen,
  selectedCategory,
  onSelectCategory,
  categories,
}) => {
  const dropdownRef = useRef<HTMLDivElement>(null);

  const handleClickOutside = (event: MouseEvent) => {
    if (
      dropdownRef.current &&
      !dropdownRef.current.contains(event.target as Node)
    ) {
      setIsOpen(false);
    }
  };

  useEffect(() => {
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <div className={styles.dropdownOutside} ref={dropdownRef}>
      <div
        className={styles.dropdownButton}
        onClick={() => setIsOpen(!isOpen)}
        aria-expanded={isOpen}
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
          className={isOpen ? styles.dropdownIconOpen : styles.dropdownIcon}
        >
          <path d="M6 9l6 6 6-6" />
        </svg>
      </div>

      {isOpen && (
        <div className={styles.dropdownContainer} role="listbox">
          {categories.map((cat) => (
            <div
              key={cat}
              className={`${styles.dropdownItem} ${
                selectedCategory === cat ? styles.selected : ""
              }`}
              onClick={() => {
                onSelectCategory(cat);
                setIsOpen(false);
              }}
              role="option"
              aria-selected={selectedCategory === cat}
            >
              {cat}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default DropdownBar;
