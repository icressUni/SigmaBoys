import { serve } from "https://deno.land/std@0.204.0/http/server.ts";
import { routes } from "./routes/index.ts";

// Permitir múltiples orígenes para desarrollo
const allowedOrigins = [
  "http://localhost:3000",
  "http://localhost:5173", // Vite dev server
  "http://127.0.0.1:3000",
  "http://127.0.0.1:5173",
];

function getAllowedOrigin(requestOrigin: string | null): string {
  if (!requestOrigin) return allowedOrigins[0];
  
  if (allowedOrigins.includes(requestOrigin)) {
    return requestOrigin;
  }
  
  return allowedOrigins[0];
}

serve(async (req: Request) => {
  const url = new URL(req.url);
  const handler = routes[url.pathname];
  const origin = req.headers.get("origin");
  const allowedOrigin = getAllowedOrigin(origin);

  console.log(`${req.method} ${url.pathname} - Origin: ${origin}`);

  // Configuración CORS
  const corsHeaders = {
    "Access-Control-Allow-Origin": allowedOrigin,
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
    "Access-Control-Max-Age": "86400",
  };

  // Manejo de preflight (CORS OPTIONS)
  if (req.method === "OPTIONS") {
    return new Response(null, {
      status: 204,
      headers: corsHeaders,
    });
  }

  if (handler) {
    try {
      const response = await handler(req);

      // Agregar headers CORS a la respuesta
      const headers = new Headers(response.headers);
      Object.entries(corsHeaders).forEach(([key, value]) => {
        headers.set(key, value);
      });

      return new Response(response.body, {
        status: response.status,
        statusText: response.statusText,
        headers,
      });
    } catch (err) {
      console.error("Error en el handler:", err);
      return new Response(JSON.stringify({ error: "Error interno del servidor" }), {
        status: 500,
        headers: {
          "Content-Type": "application/json",
          ...corsHeaders,
        },
      });
    }
  }

  // Ruta no encontrada
  return new Response(JSON.stringify({ error: "Ruta no encontrada" }), {
    status: 404,
    headers: {
      "Content-Type": "application/json",
      ...corsHeaders,
    },
  });
});

console.log("Servidor corriendo en http://localhost:8000");
console.log("Orígenes permitidos:", allowedOrigins);