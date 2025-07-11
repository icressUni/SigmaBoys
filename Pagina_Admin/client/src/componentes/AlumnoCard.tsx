import React from "react";
import styles from "../styles/AlumnoCard.module.css";
import { Alumno } from "../types/alumno";
import { AsistenciaAgrupada } from "../types/asistencia";
import { useLanguage } from "../lenguage/LenguageContext";

interface Foto {
  alumno_id: number;
  foto_enviada: string;
  url: string[];
}

interface AlumnoCardProps {
  alumno: Alumno;
  fotos: Foto[];
  asistencias?: AsistenciaAgrupada[];
  isCompact?: boolean;
  scrollableContent?: React.ReactNode;
}

const AlumnoCard = ({
  alumno,
  fotos,
  asistencias,
  isCompact = false,
}: AlumnoCardProps) => {
  // Buscar asistencias del alumno específico
  const asistenciaAlumno = asistencias?.find(a => a.alumnos_id === alumno.id);
  const { translations } = useLanguage();

  return (
    <div className={styles.card}>
      <div className={styles.info}>
        <div className={styles.headerRow}>
          <h3 className={styles.nombre}>{alumno.nombre} {alumno.apellido}</h3>
          <p className={styles.email}>{alumno.correo}</p>
        </div>
        <p className={styles.especialidad}>{alumno.especialidad}</p>

        {!isCompact && asistenciaAlumno && asistenciaAlumno.registro && asistenciaAlumno.registro.length > 0 && (
          <>
            <h4>{translations["Registro_de_ingreso:"] || "Registro de ingreso:"}</h4>
            <ul style={{ listStyle: "none", padding: 0 }}>
              {asistenciaAlumno.registro.map((r, i) => (
                <li key={i} style={{ marginBottom: "1em" }}>
                  <div><strong>{translations["Entrada"] || "Entrada"}</strong></div>
                  <div>{r.entrada ? new Date(r.entrada).toLocaleString() : "-"}</div>
                  <div><strong>{translations["Salida"] || "Salida"}</strong></div>
                  <div>{r.salida ? new Date(r.salida).toLocaleString() : "-"}</div>
                  {i !== asistenciaAlumno.registro.length - 1 && (
                    <hr style={{ marginTop: "0.5em", borderColor: "#ccc" }} />
                  )}
                </li>
              ))}
            </ul>
          </>
        )}
        
        {!isCompact && (!asistenciaAlumno || !asistenciaAlumno.registro || asistenciaAlumno.registro.length === 0) && (
          <div style={{ marginTop: "1rem", color: "#666", fontStyle: "italic" }}>
            {translations["Sin_registros_de_asistencia"] || "Sin registros de asistencia"}
          </div>
        )}
      </div>
    </div>
  );
};

export default AlumnoCard;