// data/getAsistencias.ts
export const getAsistencias = async () => {
  try {
    const response = await fetch("http://localhost:8000/api/asistencias");
    if (!response.ok) throw new Error("Error al obtener asistencias");

    const data = await response.json();

    // Agrupar registros por alumno
    const agrupado: Record<number, { alumnos_id: number; registro: { entrada: string; salida: string }[] }> = {};

    for (const row of data) {
      const id = row.alumnos_id;
      if (!agrupado[id]) {
        agrupado[id] = {
          alumnos_id: id,
          registro: [],
        };
      }

      agrupado[id].registro.push({
        entrada: row.entrada,
        salida: row.salida,
      });
    }

    // Convertimos el objeto en array
    return Object.values(agrupado);
  } catch (error) {
    console.error(error);
    return [];
  }
};
