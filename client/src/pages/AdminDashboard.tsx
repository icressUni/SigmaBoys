// src/pages/AdminDashboard.tsx
import { useState, useRef, useEffect, useMemo } from "react";
import SearchBar from "@components/SearchBar";
import DropdownBar from "@components/DropdownBar";
import CardGrid from "@components/CardGrid";
import AddUserButton from "@components/AddUserButton"; // <-- NUEVA LÍNEA
import styles from "../styles/AdminDashboard.module.css";
import { useLanguage } from "../lenguage/LenguageContext";
import { getAlumnos } from "../data/getAlumnos";
import { getAsistencias } from "../data/getAsistencias";
import { Alumno } from "../types/alumno";
import { Asistencia } from "../types/asistencia";

const AdminDashboard = () => {
  const { translations } = useLanguage();

  const categories = useMemo(() => [
    translations.category_Todos,
    translations.category_Nombre,
    translations.category_Correo,
    translations.category_Especialidad,
  ], [translations]);

  const [alumnosData, setAlumnosData] = useState<Alumno[]>([]);
  const [searchResults, setSearchResults] = useState<Alumno[]>([]);
  const [asistencias, setAsistencias] = useState<Asistencia[]>([]);
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState(categories[0]);
  const [error, setError] = useState<string | null>(null);

  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [alumnos, asistenciasData] = await Promise.all([
          getAlumnos(),
          getAsistencias(),
        ]);
        setAlumnosData(alumnos);
        setSearchResults(alumnos);
        setAsistencias(asistenciasData);
        setError(null);
      } catch (err) {
        setError("No se pudo cargar la información. Revisa la conexión con la API.");
        setAlumnosData([]);
        setSearchResults([]);
        setAsistencias([]);
      }
    };
    fetchData();
  }, []);

  const handleSearchResults = (results: Alumno[]) => {
    setSearchResults(results);
  };

  const handleSelectCategory = (category: string) => {
    setSelectedCategory(category);
    setIsDropdownOpen(false);
  };

  useEffect(() => {
    setSelectedCategory(categories[0]);
  }, [categories]);

  return (
    <div className={styles.container}>
      <h1 className={styles.header}>{translations.welcome}</h1>

      <div ref={dropdownRef} className={styles.controlsRow}>
        <div className={styles.dropdownWrapper}>
          <DropdownBar
            categories={categories}
            isOpen={isDropdownOpen}
            setIsOpen={setIsDropdownOpen}
            selectedCategory={selectedCategory}
            onSelectCategory={handleSelectCategory}
          />
        </div>

        <div className={styles.searchWrapper}>
          <SearchBar
            data={alumnosData}
            onSearchResults={handleSearchResults}
            selectedCategory={selectedCategory}
            placeholder={translations.searchPlaceholder}
          />
        </div>
      </div>

      {error ? (
        <p style={{ color: "red", marginTop: "1rem" }}>{error}</p>
      ) : (
        <div className={styles.results}>
          {searchResults.length > 0 ? (
            <CardGrid
              data={searchResults}
              fotos={[]} // Asegúrate de cargar y pasar las fotos si las tienes
              asistencias={asistencias}
              columnCount={3}
              gridHeight="auto"
            />
          ) : (
            <p>{translations.noResults || "No se encontraron resultados."}</p>
          )}
        </div>
      )}

      {/* BOTÓN DE AÑADIR USUARIO */}
      <div className={styles.floatingButtonWrapper}>
        <AddUserButton />
      </div>
    </div>
  );
};

export default AdminDashboard;
