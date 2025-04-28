// src/pages/AdminDashboard.tsx
import { useState } from 'react';
import AlumnoCard from '../componentes/cardItem/AlumnoCard.tsx';
import SearchBar from "../componentes/search/SearchBar.tsx";
import CardGrid from "../componentes/grid/CardGrid.tsx";
import alumnos from "../data/alumnos.json" with { type: "json" };
import asistencias from "../data/asistencias.json" with { type: "json" };

interface Asistencia {
  id: number;
  alumnos_id: number;
  registro: string[];
}

const AdminDashboard = () => {
  const [searchResults, setSearchResults] = useState(alumnos);

  const handleSearchResults = (results: typeof alumnos) => {
    setSearchResults(results);
  };

  // Create scrollable content for each alumno card
  const getScrollableContent = (alumnoId: number) => {
    const alumnoAsistencias = asistencias.filter(
      (asistencia: Asistencia) => asistencia.alumnos_id === alumnoId
    );

    return (
      <div>
        <h4>Asistencia Reciente</h4>
        <ul>
          {alumnoAsistencias.flatMap((asistencia: Asistencia) => 
            asistencia.registro.map((fecha, idx) => (
              <li key={`${asistencia.id}-${idx}`}>
                {new Date(fecha).toLocaleDateString('es-ES')} - Presente
              </li>
            ))
          )}
          
        </ul>
      </div>
    );
  };

  return (
    <div className="p-8 text-center">
      <h1 className="text-3xl font-bold text-green-700">Bienvenido al Panel de Administración</h1>
      <p className="mt-4 text-lg">Aquí puedes gestionar tus recursos administrativos.</p>
      
      <div className="mt-6 mb-8 w-full">
        <h2 className="text-2xl font-semibold mb-4">Buscar Alumnos</h2>
        <SearchBar data={alumnos} onSearchResults={handleSearchResults} />
      </div>
      
      <div className="mt-8">
        <div className="mt-4">
          <CardGrid
            data={searchResults}
            gridHeight="600px"
            columnCount={3}
            renderItem={(alumno) => (
              <AlumnoCard
                alumno={alumno}
                scrollableContent={getScrollableContent(alumno.id)}
              />
            )}
          />
        </div>
      </div>
    </div>
  );
  };


export default AdminDashboard;
