// src/componentes/AddUserModal.tsx
import { useState } from "react";
import styles from "../styles/AddUserModal.module.css";
import { useLanguage } from "../lenguage/LenguageContext";
import { createUser } from "../services/userService";

interface AddUserModalProps {
  onClose: () => void;
  onUserAdded: () => void;
}

interface FormData {
  username: string;
  email: string;
  password: string;
  confirmPassword: string;
  role: string;
}

const AddUserModal = ({ onClose, onUserAdded }: AddUserModalProps) => {
  const { translations } = useLanguage();
  const [formData, setFormData] = useState<FormData>({
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
    role: "user"
  });
  const [errors, setErrors] = useState<Partial<FormData>>({});
  const [isLoading, setIsLoading] = useState(false);
  const [apiError, setApiError] = useState<string>("");

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
    // Limpiar error del campo cuando el usuario empieza a escribir
    if (errors[name as keyof FormData]) {
      setErrors(prev => ({
        ...prev,
        [name]: ""
      }));
    }
  };

  const validateForm = (): boolean => {
    const newErrors: Partial<FormData> = {};

    if (!formData.username.trim()) {
      newErrors.username = translations.required || "Campo requerido";
    } else if (formData.username.length < 3) {
      newErrors.username = translations.usernameMinLength || "Mínimo 3 caracteres";
    }

    if (!formData.email.trim()) {
      newErrors.email = translations.required || "Campo requerido";
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = translations.invalidEmail || "Email inválido";
    }

    if (!formData.password) {
      newErrors.password = translations.required || "Campo requerido";
    } else if (formData.password.length < 6) {
      newErrors.password = translations.passwordMinLength || "Mínimo 6 caracteres";
    }

    if (!formData.confirmPassword) {
      newErrors.confirmPassword = translations.required || "Campo requerido";
    } else if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = translations.passwordMismatch || "Las contraseñas no coinciden";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    setIsLoading(true);
    setApiError("");

    try {
      await createUser({
        username: formData.username.trim(),
        email: formData.email.trim(),
        password: formData.password,
        role: formData.role
      });

      onUserAdded();
    } catch (error) {
      setApiError(error instanceof Error ? error.message : "Error al crear usuario");
    } finally {
      setIsLoading(false);
    }
  };

  const handleBackdropClick = (e: React.MouseEvent) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  return (
    <div className={styles.modalOverlay} onClick={handleBackdropClick}>
      <div className={styles.modalContent}>
        <div className={styles.modalHeader}>
          <h2>{translations.addUser || "Añadir Usuario"}</h2>
          <button 
            className={styles.closeButton}
            onClick={onClose}
            type="button"
          >
            ×
          </button>
        </div>

        <form onSubmit={handleSubmit} className={styles.form}>
          {apiError && (
            <div className={styles.errorMessage}>
              {apiError}
            </div>
          )}

          <div className={styles.formGroup}>
            <label htmlFor="username" className={styles.label}>
              {translations.username || "Nombre de Usuario"}
            </label>
            <input
              type="text"
              id="username"
              name="username"
              value={formData.username}
              onChange={handleInputChange}
              className={`${styles.input} ${errors.username ? styles.inputError : ""}`}
              placeholder={translations.usernamePlaceholder || "Ingresa el nombre de usuario"}
              disabled={isLoading}
            />
            {errors.username && (
              <span className={styles.fieldError}>{errors.username}</span>
            )}
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="email" className={styles.label}>
              {translations.email || "Email"}
            </label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleInputChange}
              className={`${styles.input} ${errors.email ? styles.inputError : ""}`}
              placeholder={translations.emailPlaceholder || "Ingresa el email"}
              disabled={isLoading}
            />
            {errors.email && (
              <span className={styles.fieldError}>{errors.email}</span>
            )}
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="password" className={styles.label}>
              {translations.password || "Contraseña"}
            </label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleInputChange}
              className={`${styles.input} ${errors.password ? styles.inputError : ""}`}
              placeholder={translations.passwordPlaceholder || "Ingresa la contraseña"}
              disabled={isLoading}
            />
            {errors.password && (
              <span className={styles.fieldError}>{errors.password}</span>
            )}
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="confirmPassword" className={styles.label}>
              {translations.confirmPassword || "Confirmar Contraseña"}
            </label>
            <input
              type="password"
              id="confirmPassword"
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleInputChange}
              className={`${styles.input} ${errors.confirmPassword ? styles.inputError : ""}`}
              placeholder={translations.confirmPasswordPlaceholder || "Confirma la contraseña"}
              disabled={isLoading}
            />
            {errors.confirmPassword && (
              <span className={styles.fieldError}>{errors.confirmPassword}</span>
            )}
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="role" className={styles.label}>
              {translations.role || "Rol"}
            </label>
            <select
              id="role"
              name="role"
              value={formData.role}
              onChange={handleInputChange}
              className={styles.select}
              disabled={isLoading}
            >
              <option value="user">{translations.roleUser || "Usuario"}</option>
              <option value="admin">{translations.roleAdmin || "Administrador"}</option>
              <option value="moderator">{translations.roleModerator || "Moderador"}</option>
            </select>
          </div>

          <div className={styles.buttonGroup}>
            <button
              type="button"
              onClick={onClose}
              className={styles.cancelButton}
              disabled={isLoading}
            >
              {translations.cancel || "Cancelar"}
            </button>
            <button
              type="submit"
              className={styles.submitButton}
              disabled={isLoading}
            >
              {isLoading 
                ? (translations.creating || "Creando...") 
                : (translations.createUser || "Crear Usuario")
              }
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AddUserModal;