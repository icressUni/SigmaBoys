import React, { createContext, useContext, useState, ReactNode } from "react";

interface LanguageContextProps {
  language: string;
  setLanguage: (lang: string) => void;
  translations: { [key: string]: string };
}

const translationsMap: Record<string, Record<string, string>> = {
  es: {
    welcome: "Bienvenido al Panel de Administración",
    back: "Volver atrás",
    home: "Inicio",
    loginTitle: "Clave de administrador",
    loginPlaceholder: "Contraseña...",
    loginButton: "Entrar",
    loginError: "Contraseña incorrecta",
    searchPlaceholder: "Buscar...",
    noResults: "No se encontraron resultados.",

    // Dropdown categories
    category_Todos: "Todos",
    category_Nombre: "Nombre",
    category_Correo: "Correo",
    category_Especialidad: "Especialidad",

    // Card
    Registro_de_ingreso: "Registro de ingreso:",
    Entrada: "Entrada",
    Salida: "Salida",

    // AddUserModal
    addUser: "Añadir Usuario",
    email: "Correo electrónico",
    emailPlaceholder: "Ingresa el correo",
    password: "Contraseña",
    passwordPlaceholder: "Ingresa la contraseña",
    confirmPassword: "Confirmar Contraseña",
    confirmPasswordPlaceholder: "Confirma la contraseña",
    role: "Rol",
    selectRole: "-- Selecciona un rol --",
    roleTeacher: "Profesor",
    roleAssistant: "Ayudante",
    cancel: "Cancelar",
    createUser: "Crear Usuario",
    creating: "Creando...",
    required: "Campo requerido",
    invalidEmail: "Email inválido",
    passwordMinLength: "Mínimo 6 caracteres",
    passwordMismatch: "Las contraseñas no coinciden",
  },
  en: {
    welcome: "Welcome to the Admin Dashboard",
    back: "Go back",
    home: "Home",
    loginTitle: "Admin password",
    loginPlaceholder: "Password...",
    loginButton: "Login",
    loginError: "Incorrect password",
    searchPlaceholder: "Search...",
    noResults: "No results found.",

    // Dropdown categories
    category_Todos: "All",
    category_Nombre: "Name",
    category_Correo: "Email",
    category_Especialidad: "Specialty",

    // Card
    Registro_de_ingreso: "Entry record:",
    Entrada: "Entry",
    Salida: "Exit",

    // AddUserModal
    addUser: "Add User",
    email: "Email",
    emailPlaceholder: "Enter email",
    password: "Password",
    passwordPlaceholder: "Enter password",
    confirmPassword: "Confirm Password",
    confirmPasswordPlaceholder: "Confirm password",
    role: "Role",
    selectRole: "-- Select a role --",
    roleTeacher: "Teacher",
    roleAssistant: "Assistant",
    cancel: "Cancel",
    createUser: "Create User",
    creating: "Creating...",
    required: "This field is required",
    invalidEmail: "Invalid email",
    passwordMinLength: "Minimum 6 characters",
    passwordMismatch: "Passwords do not match",
  },
};

// Crear el contexto
const LanguageContext = createContext<LanguageContextProps | undefined>(undefined);

// Hook personalizado
export const useLanguage = () => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error("useLanguage debe usarse dentro de LanguageProvider");
  }
  return context;
};

// Proveedor del contexto
export const LanguageProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [language, setLanguage] = useState("es");
  const translations = translationsMap[language];

  return (
    <LanguageContext.Provider value={{ language, setLanguage, translations }}>
      {children}
    </LanguageContext.Provider>
  );
};
