import React from "react";
import styles from "../styles/AlumnoCard.module.css";
import { Alumno } from "../types/alumno";
import { useLanguage } from "../lenguage/LenguageContext";

interface Foto {
  alumno_id: number;
  foto_enviada: string;
  url: string[];
}

interface Registro {
  entrada: string;
  salida: string;
}

interface Asistencia {
  alumnos_id: number;
  registro?: Registro[];
}

interface AlumnoCardProps {
  alumno: Alumno;
  fotos: Foto[];
  asistencias?: Asistencia[];
  isCompact?: boolean;
  scrollableContent?: React.ReactNode;
}

const AlumnoCard = ({
  alumno,
  fotos,
  asistencias,
  isCompact = false,
}: AlumnoCardProps) => {
  const asistenciaAlumno = asistencias?.[0];
  const { translations } = useLanguage();

  return (
    <div className={styles.card}>
      <div className={styles.info}>
        <div className={styles.headerRow}>
          <h3 className={styles.nombre}>{alumno.nombre} {alumno.apellido}</h3>
          <p className={styles.email}>{alumno.correo}</p>
        </div>
        <p className={styles.especialidad}>{alumno.especialidad}</p>

        {!isCompact && asistenciaAlumno && (
          <>
            <h4>{translations["Registro_de_ingreso:"] || "Registro de ingreso:"}</h4>
            <ul style={{ listStyle: "none", padding: 0 }}>
              {(asistenciaAlumno.registro ?? []).map((r, i) => (
                <li key={i} style={{ marginBottom: "1em" }}>
                  <div><strong>{translations["Entrada"] || "Entrada"}</strong></div>
                  <div>{r.entrada ? new Date(r.entrada).toLocaleString() : "-"}</div>
                  <div><strong>{translations["Salida"] || "Salida"}</strong></div>
                  <div>{r.salida ? new Date(r.salida).toLocaleString() : "-"}</div>
                  {i !== (asistenciaAlumno.registro?.length ?? 0) - 1 && (
                    <hr style={{ marginTop: "0.5em", borderColor: "#ccc" }} />
                  )}
                </li>
              ))}
            </ul>
          </>
        )}
      </div>
    </div>
  );
};

export default AlumnoCard;
