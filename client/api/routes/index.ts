// api/routes/index.ts
import { handleAlumnosRequest } from "./alumnos.ts";
import { handleAsistenciasRequest } from "./asistencias.ts";
import { getConnection } from "../db.ts"; // ← esto faltaba

// Ruta combinada: /api
export async function handleCombinedRequest(req: Request): Promise<Response> {
  try {
    const client = await getConnection();

    const result = await client.queryObject(`
      SELECT 
        a.id AS asistencia_id,
        a.entrada,
        a.salida,
        al.id AS alumno_id,
        al.nombre,
        al.apellido,
        al.correo,
        al.especialidad
      FROM asistencias a
      INNER JOIN alumnos al ON a.alumnos_id = al.id
    `);

    client.release();
    return Response.json(result.rows);
  } catch (err) {
    console.error("Error al obtener datos combinados:", err);
    return new Response("Error interno", { status: 500 });
  }
}

// Exporta todas las rutas correctamente
export const routes: Record<string, (req: Request) => Promise<Response>> = {
  "/api": handleCombinedRequest,
  "/api/alumnos": handleAlumnosRequest,
  "/api/asistencias": handleAsistenciasRequest,
};
