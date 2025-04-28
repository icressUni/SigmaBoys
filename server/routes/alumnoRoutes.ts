import { Router } from "@oak/oak";
import { AlumnoController } from "../controllers/alumnoController.ts";
import { authMiddleware } from "../middleware/authMiddleware.ts";

export const alumnoRouter = new Router();

// Rutas públicas
alumnoRouter.post("/login", AlumnoController.login);

// Rutas protegidas que requieren autenticación
alumnoRouter.get("/alumnos", authMiddleware, AlumnoController.getAlumnos);
alumnoRouter.get("/alumnos/:id", authMiddleware, AlumnoController.getAlumnoById);
alumnoRouter.post("/alumnos", authMiddleware, AlumnoController.createAlumno);
alumnoRouter.put("/alumnos/:id", authMiddleware, AlumnoController.updateAlumno);
alumnoRouter.delete("/alumnos/:id", authMiddleware, AlumnoController.deleteAlumno);
