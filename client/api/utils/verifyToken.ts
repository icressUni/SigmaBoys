import { djwt } from "../deps.ts";

const key = "clave_secreta_segura"; // Debe ser igual al del login

export async function verifyToken(req: Request): Promise<{ correo: string; role: string } | null> {
  const authHeader = req.headers.get("Authorization");
  if (!authHeader || !authHeader.startsWith("Bearer ")) return null;

  const token = authHeader.slice(7);

  try {
    const payload = await djwt.verify(token, key, "HS256");
    return payload as { correo: string; role: string };
  } catch (err) {
    console.error("Token inválido:", err);
    return null;
  }
}
