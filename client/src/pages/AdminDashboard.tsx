import { useState, useRef, useEffect } from "react";
import SearchBar from "../componentes/SearchBar";
import DropdownBar from "../componentes/DropdownBar";
import CardGrid from "../componentes/CardGrid";
import styles from "../styles/AdminDashboard.module.css";
import { useLanguage } from "../lenguage/LenguageContext";
import { getAlumnos } from "../data/getAlumnos";
import { getAsistencias } from "../data/getAsistencias";
import { Alumno } from "../types/alumno";
import { Asistencia } from "../types/asistencia";

const AdminDashboard = () => {
  const { translations } = useLanguage();

  const categories = [
    translations.category_Todos || "Todos",
    translations.category_Nombre || "Nombre",
    translations.category_Correo || "Correo",
    translations.category_Especialidad || "Especialidad",
  ];

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
            placeholder={translations.searchPlaceholder || "Buscar..."}
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
    </div>
  );
};

export default AdminDashboard;
