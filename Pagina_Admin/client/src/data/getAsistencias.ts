// src/data/getAsistencias.ts
import { Asistencia, AsistenciaAgrupada } from "../types/asistencia";

const API_URL = import.meta.env.VITE_API_URL || `http://${window.location.hostname}:8000`;

export async function getAsistencias(): Promise<AsistenciaAgrupada[]> {
  try {
    // Obtener token del localStorage
    const token = localStorage.getItem("token");
    
    if (!token) {
      throw new Error("No hay token de autenticación");
    }

    const response = await fetch(`${API_URL}/api/asistencias`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      if (response.status === 401) {
        // Token inválido, limpiar localStorage
        localStorage.removeItem("token");
        window.location.href = "/";
        throw new Error("Sesión expirada");
      }
      throw new Error(`Error ${response.status}: ${response.statusText}`);
    }

    const data: Asistencia[] = await response.json();
    
    // Agrupar asistencias por alumno
    const asistenciasAgrupadas = data.reduce((acc, asistencia) => {
      const alumnoId = asistencia.alumnos_id;
      
      if (!acc[alumnoId]) {
        acc[alumnoId] = {
          id: asistencia.id,
          alumnos_id: alumnoId,
          registro: []
        };
      }
      
      acc[alumnoId].registro.push({
        entrada: asistencia.entrada,
        salida: asistencia.salida
      });
      
      return acc;
    }, {} as Record<number, AsistenciaAgrupada>);
    
    return Object.values(asistenciasAgrupadas);
  } catch (error) {
    console.error("Error al obtener asistencias:", error);
    throw error;
  }
}