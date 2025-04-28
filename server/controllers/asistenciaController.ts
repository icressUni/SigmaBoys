import { Context, RouterContext, Status } from "@oak/oak";
import { AsistenciaModel, CreateAsistenciaDto } from "../models/asistenciaModel.ts";
import { AlumnoModel } from "../models/alumnoModel.ts";

export class AsistenciaController {
  static async getAsistencias(ctx: Context) {
    try {
      const asistencias = await AsistenciaModel.findAll();
      ctx.response.body = { success: true, data: asistencias };
    } catch (error) {
      ctx.response.status = Status.InternalServerError;
      ctx.response.body = { success: false, error: (error instanceof Error) ? error.message : "Unknown error" };
    }
  }

  static async getAsistenciaById(ctx: RouterContext<"/asistencias/:id", { id: string }>) {
    try {
      const id = parseInt(ctx.params.id);
      if (isNaN(id)) {
        ctx.response.status = Status.BadRequest;
        ctx.response.body = { success: false, error: "ID inválido" };
        return;
      }

      const asistencia = await AsistenciaModel.findById(id);
      if (!asistencia) {
        ctx.response.status = Status.NotFound;
        ctx.response.body = { success: false, error: "Asistencia no encontrada" };
        return;
      }

      ctx.response.body = { success: true, data: asistencia };
    } catch (error) {
      ctx.response.status = Status.InternalServerError;
      ctx.response.body = { success: false, error: (error instanceof Error) ? error.message : "Unknown error" };
    }
  }

  static async getAsistenciasByAlumnoId(ctx: RouterContext<"/alumnos/:id/asistencias", { id: string }>) {
    try {
      const alumnoId = parseInt(ctx.params.id);
      if (isNaN(alumnoId)) {
        ctx.response.status = Status.BadRequest;
        ctx.response.body = { success: false, error: "ID de alumno inválido" };
        return;
      }

      // Verificar que el alumno exista
      const alumno = await AlumnoModel.findById(alumnoId);
      if (!alumno) {
        ctx.response.status = Status.NotFound;
        ctx.response.body = { success: false, error: "Alumno no encontrado" };
        return;
      }

      const asistencias = await AsistenciaModel.findByAlumnoId(alumnoId);
      ctx.response.body = { success: true, data: asistencias };
    } catch (error) {
      ctx.response.status = Status.InternalServerError;
      ctx.response.body = { success: false, error: (error instanceof Error) ? error.message : "Unknown error" };
    }
  }

  static async createAsistencia(ctx: Context) {
    try {
      const body = ctx.request.body;
      if (!body.type || body.type !== "json") {
        ctx.response.status = Status.BadRequest;
        ctx.response.body = { success: false, error: "Datos inválidos" };
        return;
      }
      
      const data = await body.value as CreateAsistenciaDto;
      
      // Validate required fields
      if (!data.alumnos_id) {
        ctx.response.status = Status.BadRequest;
        ctx.response.body = { success: false, error: "ID de alumno es requerido" };
        return;
      }
      
      // Set registro to current date if not provided
      if (!data.registro) {
        data.registro = new Date();
      }
      
      // Check if alumno exists
      const alumno = await AlumnoModel.findById(data.alumnos_id);
      if (!alumno) {
        ctx.response.status = Status.NotFound;
        ctx.response.body = { success: false, error: "Alumno no encontrado" };
        return;
      }
      
      const asistencia = await AsistenciaModel.create(data);
      ctx.response.status = Status.Created;
      ctx.response.body = { success: true, data: asistencia };
    } catch (error) {
      ctx.response.status = Status.InternalServerError;
      ctx.response.body = { success: false, error: (error instanceof Error) ? error.message : "Unknown error" };
    }
  }

  static async deleteAsistencia(ctx: RouterContext<"/asistencias/:id", { id: string }>) {
    try {
      const id = parseInt(ctx.params.id);
      if (isNaN(id)) {
        ctx.response.status = Status.BadRequest;
        ctx.response.body = { success: false, error: "ID inválido" };
        return;
      }

      const success = await AsistenciaModel.delete(id);
      if (!success) {
        ctx.response.status = Status.NotFound;
        ctx.response.body = { success: false, error: "Asistencia no encontrada" };
        return;
      }

      ctx.response.body = { success: true, message: "Asistencia eliminada correctamente" };
    } catch (error) {
      ctx.response.status = Status.InternalServerError;
      ctx.response.body = { success: false, error: (error instanceof Error) ? error.message : "Unknown error" };
    }
  }
}
