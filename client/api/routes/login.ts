import { getConnection } from "../db.ts";
import { bcrypt } from "../deps.ts";

export async function handleLoginRequest(req: Request): Promise<Response> {
  if (req.method !== "POST") {
    return new Response("Método no permitido", { status: 405 });
  }

  try {
    const { correo, contrasena } = await req.json();

    if (!correo || !contrasena) {
      return new Response("Faltan campos requeridos", { status: 400 });
    }

    const client = await getConnection();

    // Buscar el profesor por correo
    const result = await client.queryObject<{ password_hash: string; role: string }>(
      "SELECT password_hash, role FROM profesores WHERE email = $1",
      [correo]
    );

    client.release();

    if (result.rows.length === 0) {
      return new Response("Usuario no encontrado", { status: 401 });
    }

    const { password_hash, role } = result.rows[0];

    // Verificar contraseña
    const passwordMatch = await bcrypt.compare(contrasena, password_hash);

    if (!passwordMatch) {
      return new Response("Contraseña incorrecta", { status: 401 });
    }

    // Aquí podrías generar un token JWT para mantener sesión, pero para simplicidad devolveremos info básica
    const responseBody = {
      correo,
      role,
      message: "Login exitoso",
    };

    return new Response(JSON.stringify(responseBody), {
      status: 200,
      headers: {
        "Content-Type": "application/json",
      },
    });
  } catch (err) {
    console.error("Error en login:", err);
    return new Response("Error interno", { status: 500 });
  }
}
