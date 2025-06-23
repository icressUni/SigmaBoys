import { getConnection } from "../db.ts";
import { bcrypt, djwt } from "../deps.ts";

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
    const result = await client.queryObject<{ password_hash: string; role: string }>(
      "SELECT password_hash, role FROM profesores WHERE email = $1",
      [correo]
    );
    client.release();

    if (result.rows.length === 0) {
      return new Response("Usuario no encontrado", { status: 401 });
    }

    const { password_hash, role } = result.rows[0];
    const passwordMatch = await bcrypt.compare(contrasena, password_hash);

    if (!passwordMatch) {
      return new Response("Contraseña incorrecta", { status: 401 });
    }

    // ✅ Generar clave secreta en formato CryptoKey
    const key = await crypto.subtle.importKey(
      "raw",
      new TextEncoder().encode("clave_secreta_segura"), // tu clave secreta
      { name: "HMAC", hash: "SHA-256" },
      false,
      ["sign", "verify"]
    );

    // ✅ Crear JWT con djwt
    const jwt = await djwt.create(
      { alg: "HS256", typ: "JWT" },
      { correo, role },
      key
    );

    return new Response(JSON.stringify({ token: jwt }), {
      status: 200,
      headers: { "Content-Type": "application/json" },
    });
  } catch (err) {
    console.error("Error en login:", err);
    return new Response("Error interno", { status: 500 });
  }
}
