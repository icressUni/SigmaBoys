import { Router } from "@oak/oak";
import { FotoController } from "../controllers/fotoController.ts";
import { authMiddleware } from "../middleware/authMiddleware.ts";

export const fotoRouter = new Router();

// Todas las rutas de fotos requieren autenticación
fotoRouter.get("/fotos", authMiddleware, FotoController.getFotos);
fotoRouter.get("/fotos/:id", authMiddleware, FotoController.getFotoById);
fotoRouter.get("/alumnos/:id/fotos", authMiddleware, FotoController.getFotosByAlumnoId);
fotoRouter.post("/fotos", authMiddleware, FotoController.createFoto);
fotoRouter.put("/fotos/:id", authMiddleware, FotoController.updateFoto);
fotoRouter.delete("/fotos/:id", authMiddleware, FotoController.deleteFoto);
