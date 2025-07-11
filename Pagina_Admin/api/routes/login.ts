import { getConnection } from "../db.ts";
import { bcrypt, djwt } from "../deps.ts";

export async function handleLoginRequest(req: Request): Promise<Response> {
  if (req.method !== "POST") {
    return new Response(JSON.stringify({ error: "Método no permitido" }), { 
      status: 405,
      headers: { "Content-Type": "application/json" }
    });
  }

  try {
    const { correo, contrasena } = await req.json();

    console.log("Intento de login para:", correo);

    if (!correo || !contrasena) {
      return new Response(JSON.stringify({ error: "Faltan campos requeridos" }), { 
        status: 400,
        headers: { "Content-Type": "application/json" }
      });
    }

    const client = await getConnection();
    
    try {
      const result = await client.queryObject<{ password_hash: string; role: string }>(
        "SELECT password_hash, role FROM profesores WHERE email = $1",
        [correo]
      );

      if (result.rows.length === 0) {
        console.log("Usuario no encontrado:", correo);
        return new Response(JSON.stringify({ error: "Usuario no encontrado" }), { 
          status: 401,
          headers: { "Content-Type": "application/json" }
        });
      }

      const { password_hash, role } = result.rows[0];
      const passwordMatch = await bcrypt.compare(contrasena, password_hash);

      if (!passwordMatch) {
        console.log("Contraseña incorrecta para:", correo);
        return new Response(JSON.stringify({ error: "Contraseña incorrecta" }), { 
          status: 401,
          headers: { "Content-Type": "application/json" }
        });
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

      console.log("Login exitoso para:", correo);

      return new Response(JSON.stringify({ 
        token: jwt,
        user: { correo, role },
        message: "Login exitoso" 
      }), {
        status: 200,
        headers: { "Content-Type": "application/json" },
      });

    } finally {
      client.release();
    }

  } catch (err) {
    console.error("Error en login:", err);
    return new Response(JSON.stringify({ error: "Error interno del servidor" }), { 
      status: 500,
      headers: { "Content-Type": "application/json" }
    });
  }
}