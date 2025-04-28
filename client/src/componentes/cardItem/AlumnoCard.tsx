import React, { ReactNode } from 'react';
import './AlumnoCard.css';

interface Alumno {
  id: number;
  nombres: string;
  apellidos: string;
  rut: string;
  admin: boolean;
}

interface AlumnoCardProps {
  alumno: Alumno;
  scrollableContent?: ReactNode;
}

const AlumnoCard: React.FC<AlumnoCardProps> = ({ alumno, scrollableContent }) => {
  return (
    <div className="alumno-card">
      <div className="alumno-card-header">
        <h3>{alumno.nombres} {alumno.apellidos}</h3>
        <span className="alumno-card-id">ID: {alumno.id}</span>
      </div>
      
      <div className="alumno-card-info">
        <p><strong>RUT:</strong> {alumno.rut}</p>
        <p><strong>Tipo:</strong> {alumno.admin ? 'Administrador' : 'Estudiante'}</p>
      </div>
      
      {scrollableContent && (
        <div className="alumno-card-scrollable">
          {scrollableContent}
        </div>
      )}
    </div>
  );
};

export default AlumnoCard;
