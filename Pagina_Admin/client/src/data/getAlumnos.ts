// data/getAlumnos.ts
export const getAlumnos = async () => {
  try {
    const response = await fetch("http://localhost:8000/api/alumnos");
    if (!response.ok) throw new Error("Error al obtener alumnos");
    const data = await response.json();
    return data; // asumiendo que data ya es un array de alumnos
  } catch (error) {
    console.error(error);
    return [];
  }
};
