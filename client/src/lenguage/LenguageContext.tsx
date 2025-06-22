import React, { createContext, useContext, useState, ReactNode } from "react";

interface LanguageContextProps {
  language: string;
  setLanguage: (lang: string) => void;
  translations: { [key: string]: string };
}

const translationsMap: Record<string, Record<string, string>> = {
  es: {
    welcome: "Bienvenido al Panel de Administración", // preferí esta versión más completa
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

    //Card
    Registro_de_ingreso:"Registro de ingreso:",
    Entrada: "Entrada",
    Salida: "Salida",
  },
  en: {
    welcome: "Welcome to the Admin Dashboard", // preferí esta versión más descriptiva
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
    category_Correo: "Mail",
    category_Especialidad: "Specialty",
    //Card
    Registro_de_ingreso:"Entry record:",
    Entrada: "Entry",
    Salida: "Exit",
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
