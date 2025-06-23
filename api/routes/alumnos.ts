// api/routes/alumnos.ts
import { getConnection } from "../db.ts";

export async function handleAlumnosRequest(req: Request): Promise<Response> {
  try {
    const client = await getConnection();

    const result = await client.queryObject(
      `SELECT id, nombre, apellido, correo, especialidad FROM alumnos`
    );

    client.release();
    return Response.json(result.rows);
  } catch (err) {
    console.error("Error al obtener alumnos:", err);
    return new Response("Error interno", { status: 500 });
  }
}
