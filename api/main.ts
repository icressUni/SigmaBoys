import { serve } from "https://deno.land/std@0.204.0/http/server.ts";
import { routes } from "./routes/index.ts";

const allowedOrigin = "http://localhost:3000"; // Asegúrate de que coincida con tu frontend

serve(async (req: Request) => {
  const url = new URL(req.url);
  const handler = routes[url.pathname];

  // Manejo de preflight (CORS OPTIONS)
  if (req.method === "OPTIONS") {
    return new Response(null, {
      status: 204,
      headers: {
        "Access-Control-Allow-Origin": allowedOrigin,
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Max-Age": "86400", // 1 día
      },
    });
  }

  if (handler) {
    try {
      const response = await handler(req);

      const headers = new Headers(response.headers);
      headers.set("Access-Control-Allow-Origin", allowedOrigin);
      headers.set("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
      headers.set("Access-Control-Allow-Headers", "Content-Type");

      return new Response(response.body, {
        status: response.status,
        statusText: response.statusText,
        headers,
      });
    } catch (err) {
      console.error("Error en el handler:", err);
      return new Response("Error interno del servidor", {
        status: 500,
        headers: {
          "Access-Control-Allow-Origin": allowedOrigin,
          "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
          "Access-Control-Allow-Headers": "Content-Type",
        },
      });
    }
  }

  // Ruta no encontrada
  return new Response("Ruta no encontrada", {
    status: 404,
    headers: {
      "Access-Control-Allow-Origin": allowedOrigin,
      "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    },
  });
});
