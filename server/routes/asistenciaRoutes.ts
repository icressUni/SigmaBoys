import { Router } from "@oak/oak";
import { AsistenciaController } from "../controllers/asistenciaController.ts";
import { authMiddleware } from "../middleware/authMiddleware.ts";

export const asistenciaRouter = new Router();

// Todas las rutas de asistencia requieren autenticación
asistenciaRouter.get("/asistencias", authMiddleware, AsistenciaController.getAsistencias);
asistenciaRouter.get("/asistencias/:id", authMiddleware, AsistenciaController.getAsistenciaById);
asistenciaRouter.get("/alumnos/:id/asistencias", authMiddleware, AsistenciaController.getAsistenciasByAlumnoId);
asistenciaRouter.post("/asistencias", authMiddleware, AsistenciaController.createAsistencia);
asistenciaRouter.delete("/asistencias/:id", authMiddleware, AsistenciaController.deleteAsistencia);
