import { Context, Status } from "@oak/oak";
import { create, verify } from "https://deno.land/x/djwt@v2.8/mod.ts";
import { config } from "../config/config.ts";

const encoder = new TextEncoder();
const jwtSecret = encoder.encode(config.JWT_SECRET);

export async function createToken(payload: Record<string, unknown>) {
  return await create({ alg: "HS256", typ: "JWT" }, { ...payload, exp: Date.now() + 60 * 60 * 1000 }, jwtSecret);
}

export async function authMiddleware(ctx: Context, next: () => Promise<unknown>) {
  try {
    const authHeader = ctx.request.headers.get("Authorization");
    if (!authHeader || !authHeader.startsWith("Bearer ")) {
      ctx.response.status = Status.Unauthorized;
      ctx.response.body = { success: false, error: "Token no proporcionado" };
      return;
    }

    const token = authHeader.split(" ")[1];
    
    try {
      const payload = await verify(token, jwtSecret);
      // Set user info on context for use in controllers
      ctx.state.user = payload;
      await next();
    } catch (error) {
      ctx.response.status = Status.Unauthorized;
      ctx.response.body = { success: false, error: "Token inválido" };
    }
  } catch (error) {
    ctx.response.status = Status.Unauthorized;
    ctx.response.body = { success: false, error: "Error de autenticación" };
  }
}
