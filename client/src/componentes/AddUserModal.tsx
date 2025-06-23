// src/componentes/AddUserModal.tsx
import { useState } from "react";
import styles from "../styles/AddUserModal.module.css";
import { useLanguage } from "../lenguage/LenguageContext";

interface AddUserModalProps {
  onClose: () => void;
  onUserAdded: () => void;
}

interface FormData {
  email: string;
  password: string;
  confirmPassword: string;
  role: string;
}

const AddUserModal = ({ onClose, onUserAdded }: AddUserModalProps) => {
  const { translations } = useLanguage();
  const [formData, setFormData] = useState<FormData>({
    email: "",
    password: "",
    confirmPassword: "",
    role: "",
  });
  const [errors, setErrors] = useState<Partial<FormData>>({});
  const [isLoading, setIsLoading] = useState(false);
  const [apiError, setApiError] = useState<string>("");

  // Nuevo estado para mostrar toast fuera del modal
  const [showToast, setShowToast] = useState(false);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    if (errors[name as keyof FormData]) {
      setErrors(prev => ({ ...prev, [name]: "" }));
    }
  };

  const validateForm = (): boolean => {
    const newErrors: Partial<FormData> = {};

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

    if (!formData.role) {
      newErrors.role = translations.required || "Campo requerido";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validateForm()) return;

    setIsLoading(true);
    setApiError("");

    try {
      const response = await fetch("http://localhost:8000/api/profesores", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          correo: formData.email.trim(),
          contrasena: formData.password,
          rol: formData.role,
        }),
      });

      const message = await response.text();
      if (!response.ok) throw new Error(message || "Error al crear usuario");

      onUserAdded();
      onClose();

      // Mostrar toast luego de cerrar modal
      setShowToast(true);
      setTimeout(() => setShowToast(false), 3000);
    } catch (error) {
      setApiError(error instanceof Error ? error.message : "Error al crear usuario");
    } finally {
      setIsLoading(false);
    }
  };

  const handleBackdropClick = (e: React.MouseEvent) => {
    if (e.target === e.currentTarget) {
      setApiError("");
      onClose();
    }
  };

  return (
    <>
      <div className={styles.modalOverlay} onClick={handleBackdropClick}>
        <div className={styles.modalContent}>
          <div className={styles.modalHeader}>
            <h2>{translations.addUser || "Añadir Usuario"}</h2>
            {/* Botón "X" eliminado intencionalmente */}
          </div>

          <form onSubmit={handleSubmit} className={styles.form}>
            {apiError && <div className={styles.errorMessage}>{apiError}</div>}

            {/* ... resto del formulario igual ... */}

            <div className={styles.formGroup}>
              <label htmlFor="email" className={styles.label}>
                {translations.email || "Correo electrónico"}
              </label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleInputChange}
                className={`${styles.input} ${errors.email ? styles.inputError : ""}`}
                placeholder={translations.emailPlaceholder || "Ingresa el correo"}
                disabled={isLoading}
              />
              {errors.email && <span className={styles.fieldError}>{errors.email}</span>}
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
              {errors.password && <span className={styles.fieldError}>{errors.password}</span>}
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
              {errors.confirmPassword && <span className={styles.fieldError}>{errors.confirmPassword}</span>}
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
                className={`${styles.select} ${errors.role ? styles.inputError : ""}`}
                disabled={isLoading}
              >
                <option value="" disabled>
                  {translations.selectRole || "-- Selecciona un rol --"}
                </option>
                <option value="profesor">{translations.roleTeacher || "Profesor"}</option>
                <option value="ayudante">{translations.roleAssistant || "Ayudante"}</option>
              </select>
              {errors.role && <span className={styles.fieldError}>{errors.role}</span>}
            </div>

            <div className={styles.buttonGroup}>
              <button type="button" onClick={onClose} className={styles.cancelButton} disabled={isLoading}>
                {translations.cancel || "Cancelar"}
              </button>
              <button type="submit" className={styles.submitButton} disabled={isLoading}>
                {isLoading ? translations.creating || "Creando..." : translations.createUser || "Crear Usuario"}
              </button>
            </div>
          </form>
        </div>
      </div>

      {/* Toast flotante */}
      {showToast && (
        <div className={styles.toast}>
          {translations.userCreated || "Usuario creado exitosamente"}
        </div>
      )}
    </>
  );
};

export default AddUserModal;
