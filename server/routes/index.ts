import { Router } from "@oak/oak";
import { alumnoRouter } from "./alumnoRoutes.ts";
import { asistenciaRouter } from "./asistenciaRoutes.ts";
import { fotoRouter } from "./fotoRoutes.ts";

export const router = new Router();

// Health check endpoint
router.get("/api/health", (ctx) => {
  ctx.response.body = { status: "ok", timestamp: new Date().toISOString() };
});

// Apply all routes
router.use("/api", alumnoRouter.routes(), alumnoRouter.allowedMethods());
router.use("/api", asistenciaRouter.routes(), asistenciaRouter.allowedMethods());
router.use("/api", fotoRouter.routes(), fotoRouter.allowedMethods());

// 404 handler for API routes
router.all("/api/(.*)", (ctx) => {
  ctx.response.status = 404;
  ctx.response.body = { success: false, error: "Endpoint no encontrado" };
});
