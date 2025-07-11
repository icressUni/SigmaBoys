import React, { useState } from "react";
import styles from "../styles/CardGrid.module.css";
import AlumnoCard from "../componentes/AlumnoCard";
import { Alumno } from "../types/alumno";
import { AsistenciaAgrupada } from "../types/asistencia";

interface Foto {
  id: number;
  alumno_id: number;
  url: string[];
}

interface CardGridProps {
  data: Alumno[];
  fotos: Foto[];
  asistencias: AsistenciaAgrupada[];
  gridHeight?: string;
  gridWidth?: string;
  columnCount?: number;
}

const CardGrid = ({
  data,
  fotos,
  asistencias,
  gridHeight = "500px",
  gridWidth = "100%",
}: CardGridProps) => {
  const [expandedId, setExpandedId] = useState<number | null>(null);

  const handleOpen = (id: number) => {
    setExpandedId(id);
  };

  const handleClose = () => {
    setExpandedId(null);
  };

  return (
    <>
      <div
        className={styles.listContainer}
        style={{
          height: gridHeight,
          width: gridWidth,
          overflowY: "auto",
          padding: "1rem",
        }}
      >
        <ul className={styles.nameList}>
          {data.map((alumno) => (
            <li
              key={alumno.id}
              className={styles.nameCard}
              onClick={() => handleOpen(alumno.id)}
            >
              <div className={styles.nameText}>{alumno.nombre} {alumno.apellido}</div>
              <div className={styles.email}>{alumno.correo}</div>
              <div className={styles.especialidad}>{alumno.especialidad}</div>
            </li>
          ))}
        </ul>
      </div>

      {expandedId !== null && (
        <div
          className={styles.modalOverlay}
          onClick={handleClose}
          aria-modal="true"
          role="dialog"
        >
          <div
            className={styles.modalContent}
            onClick={(e) => e.stopPropagation()}
          >
            {(() => {
              const alumno = data.find((a) => a.id === expandedId);
              if (!alumno) return null;
              
              const alumnoFotos = fotos.filter((f) => f.alumno_id === alumno.id);
              // Las asistencias ya están agrupadas por alumno
              const alumnoAsistencias = asistencias.filter(
                (a) => a.alumnos_id === alumno.id
              );
              
              return (
                <AlumnoCard
                  alumno={alumno}
                  fotos={alumnoFotos}
                  asistencias={alumnoAsistencias}
                  isCompact={false}
                />
              );
            })()}
          </div>
        </div>
      )}
    </>
  );
};

export default CardGrid;