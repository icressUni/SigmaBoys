import { djwt } from "../deps.ts";

const secret = Deno.env.get("JWT_SECRET") || "clave_secreta_segura";

export async function verifyToken(req: Request): Promise<{ correo: string; role: string } | null> {
  const authHeader = req.headers.get("Authorization");
  if (!authHeader || !authHeader.startsWith("Bearer ")) return null;

  const token = authHeader.slice(7);

  try {
    const key = await crypto.subtle.importKey(
      "raw",
      new TextEncoder().encode(secret),
      { name: "HMAC", hash: "SHA-256" },
      false,
      ["sign", "verify"]
    );

    const payload = await djwt.verify(token, key, "HS256");
    return payload as { correo: string; role: string };
  } catch (err) {
    console.error("Token inválido:", err);
    return null;
  }
}
