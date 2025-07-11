// src/data/getAsistencias.ts
import { Asistencia } from "../types/asistencia";

const API_URL = import.meta.env.VITE_API_URL || `http://${window.location.hostname}:8000`;

export async function getAsistencias(): Promise<Asistencia[]> {
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

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error al obtener asistencias:", error);
    throw error;
  }
}