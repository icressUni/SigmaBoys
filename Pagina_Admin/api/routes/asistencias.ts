// api/routes/asistencias.ts
import { getConnection } from "../db.ts";

export async function handleAsistenciasRequest(req: Request): Promise<Response> {
  try {
    const client = await getConnection();

    const result = await client.queryObject(
      `SELECT id, alumnos_id, entrada, salida FROM asistencias`
    );

    client.release();
    return Response.json(result.rows);
  } catch (err) {
    console.error("Error al obtener asistencias:", err);
    return new Response("Error interno", { status: 500 });
  }
}
