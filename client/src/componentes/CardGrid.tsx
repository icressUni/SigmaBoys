import React, { useState } from "react";
import styles from "../styles/CardGrid.module.css";
import AlumnoCard from "../componentes/AlumnoCard";
import { Alumno } from "../types/alumno";

interface Foto {
  id: number;
  alumno_id: number;
  url: string[];
}

interface Registro {
  entrada: string;
  salida: string;
}

interface Asistencia {
  id: number;
  alumnos_id: number;
  registro: Registro[];
}

interface CardGridProps {
  data: Alumno[];
  fotos: Foto[];
  asistencias: Asistencia[];
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
  columnCount = 3,
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
        className={styles.container}
        style={{
          height: gridHeight,
          width: gridWidth,
        }}
      >
        <div
          className={styles.grid}
          style={{
            gridTemplateColumns: `repeat(${columnCount}, 1fr)`,
          }}
        >
          {data.map((alumno) => {
            const alumnoFotos = fotos.filter((f) => f.alumno_id === alumno.id);
            const alumnoAsistencias = asistencias.filter(
              (a) => a.alumnos_id === alumno.id
            );

            return (
              <div key={alumno.id} className={styles.item}>
                <div
                  onClick={() => handleOpen(alumno.id)}
                  style={{ cursor: "pointer", width: "100%" }}
                >
                  <AlumnoCard
                    alumno={alumno}
                    fotos={alumnoFotos}
                    asistencias={alumnoAsistencias}
                    isCompact={true}
                  />
                </div>
              </div>
            );
          })}
        </div>
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
