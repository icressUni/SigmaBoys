import React from "react";
import styles from "../styles/AlumnoCard.module.css";
import { Alumno } from "../types/alumno";
import { useLanguage } from "../lenguage/LenguageContext"; // ajusta ruta si hace falta

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
  registro: Registro[];
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
  const fotoAlumno = fotos.find((f) => f.alumno_id === alumno.id);
  const fotoURL = fotoAlumno?.foto_enviada || "/reconocimiento-facial.png";

  const asistenciaAlumno = asistencias?.find((a) => a.alumnos_id === alumno.id);

  const { translations } = useLanguage();

  return (
    <div className={styles.card}>
      <img
        src={fotoURL}
        alt={`${alumno.nombre} ${alumno.apellido}`}
        className={styles.image}
      />

      <div className={styles.info}>
        <h3>{alumno.nombre} {alumno.apellido}</h3>
        <p className={styles.email}>{alumno.correo}</p> {/* NUEVO */}
        <p className={styles.especialidad}>{alumno.especialidad}</p>
        {!isCompact && asistenciaAlumno && (
          <>
            <h4>{translations["Registro_de_ingreso:"] || "Registro de ingreso:"}</h4>
            <ul style={{ listStyle: "none", padding: 0 }}>
              {asistenciaAlumno.registro.map((r, i) => (
                <li key={i} style={{ marginBottom: "1em" }}>
                  <div><strong>{translations["Entrada"] || "Entrada"}</strong></div>
                  <div>{new Date(r.entrada).toLocaleString()}</div>
                  <div><strong>{translations["Salida"] || "Salida"}</strong></div>
                  <div>{new Date(r.salida).toLocaleString()}</div>
                  {i !== asistenciaAlumno.registro.length - 1 && (
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
