// src/componentes/AddUserButton.tsx
import { useState } from "react";
import styles from "../styles/AddUserButton.module.css";
import { useLanguage } from "../lenguage/LenguageContext";
import AddUserModal from "./AddUserModal";

interface AddUserButtonProps {
  onUserAdded?: () => void;
}

const AddUserButton = ({ onUserAdded }: AddUserButtonProps) => {
  const { translations } = useLanguage();
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleOpenModal = () => {
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
  };

  const handleUserAdded = () => {
    setIsModalOpen(false);
    if (onUserAdded) {
      onUserAdded();
    }
  };

  return (
    <>
      <button 
        className={styles.addButton}
        onClick={handleOpenModal}
        title={translations.addUser || "Añadir Usuario"}
      >
        <svg 
          width="24" 
          height="24" 
          viewBox="0 0 24 24" 
          fill="none" 
          xmlns="http://www.w3.org/2000/svg"
        >
          <path 
            d="M12 5V19M5 12H19" 
            stroke="currentColor" 
            strokeWidth="2" 
            strokeLinecap="round" 
            strokeLinejoin="round"
          />
        </svg>
      </button>

      {isModalOpen && (
        <AddUserModal 
          onClose={handleCloseModal}
          onUserAdded={handleUserAdded}
        />
      )}
    </>
  );
};

export default AddUserButton;