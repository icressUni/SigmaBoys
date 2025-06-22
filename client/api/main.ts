import { serve } from "https://deno.land/std@0.204.0/http/server.ts";
import { routes } from "./routes/index.ts";

const allowedOrigin = "http://localhost:3000";

serve(async (req: Request) => {
  const url = new URL(req.url);
  const handler = routes[url.pathname];

  if (req.method === "OPTIONS") {
    return new Response(null, {
      status: 204,
      headers: {
        "Access-Control-Allow-Origin": allowedOrigin,
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
      },
    });
  }

  if (handler) {
    const response = await handler(req);
    const newHeaders = new Headers(response.headers);
    newHeaders.set("Access-Control-Allow-Origin", allowedOrigin);

    return new Response(response.body, {
      status: response.status,
      statusText: response.statusText,
      headers: newHeaders,
    });
  }

  return new Response("Ruta no encontrada", { status: 404 });
});
