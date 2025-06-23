// api/routes/profesores.ts
import { getConnection } from "../db.ts";
import { bcrypt } from "../deps.ts";

export async function handleProfesoresRequest(req: Request): Promise<Response> {
  if (req.method === "POST") {
    try {
      const { correo, contrasena, rol } = await req.json();

      if (!correo || !contrasena || !rol) {
        return new Response("Faltan campos requeridos", { status: 400 });
      }

      const hashedPassword = await bcrypt.hash(contrasena);

      const client = await getConnection();
      await client.queryObject(
        `INSERT INTO profesores (email, password_hash, role) VALUES ($1, $2, $3)`,
        [correo, hashedPassword, rol]
      );

      client.release();
      return new Response("Profesor registrado con éxito", { status: 201 });
    } catch (err) {
      console.error("Error al registrar profesor:", err);
      return new Response("Error interno: " + (err instanceof Error ? err.message : String(err)), {
        status: 500,
      });
    }
  }

  return new Response("Método no permitido", { status: 405 });
}
