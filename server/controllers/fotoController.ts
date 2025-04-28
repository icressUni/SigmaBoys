import { Context, RouterContext, Status } from "@oak/oak";
import { FotoModel, CreateFotoDto } from "../models/fotoModel.ts";
import { AlumnoModel } from "../models/alumnoModel.ts";

export class FotoController {
  static async getFotos(ctx: Context) {
    try {
      const fotos = await FotoModel.findAll();
      ctx.response.body = { success: true, data: fotos };
    } catch (error) {
      ctx.response.status = Status.InternalServerError;
      ctx.response.body = { success: false, error: (error instanceof Error) ? error.message : "Unknown error" };
    }
  }

  static async getFotoById(ctx: RouterContext<"/fotos/:id", { id: string }>) {
    try {
      const id = parseInt(ctx.params.id);
      if (isNaN(id)) {
        ctx.response.status = Status.BadRequest;
        ctx.response.body = { success: false, error: "ID inválido" };
        return;
      }

      const foto = await FotoModel.findById(id);
      if (!foto) {
        ctx.response.status = Status.NotFound;
        ctx.response.body = { success: false, error: "Foto no encontrada" };
        return;
      }

      ctx.response.body = { success: true, data: foto };
    } catch (error) {
      ctx.response.status = Status.InternalServerError;
      ctx.response.body = { success: false, error: (error instanceof Error) ? error.message : "Unknown error" };
    }
  }

  static async getFotosByAlumnoId(ctx: RouterContext<"/alumnos/:id/fotos", { id: string }>) {
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

      const fotos = await FotoModel.findByAlumnoId(alumnoId);
      ctx.response.body = { success: true, data: fotos };
    } catch (error) {
      ctx.response.status = Status.InternalServerError;
      ctx.response.body = { success: false, error: (error instanceof Error) ? error.message : "Unknown error" };
    }
  }

  static async createFoto(ctx: Context) {
    try {
      const body = ctx.request.body;
      if (!body.type || body.type !== "json") {
        ctx.response.status = Status.BadRequest;
        ctx.response.body = { success: false, error: "Datos inválidos" };
        return;
      }
      
      const data = await body.value as CreateFotoDto;
      
      // Validate required fields
      if (!data.alumnos_id || !data.url) {
        ctx.response.status = Status.BadRequest;
        ctx.response.body = { success: false, error: "ID de alumno y URL son requeridos" };
        return;
      }
      
      // Check if alumno exists
      const alumno = await AlumnoModel.findById(data.alumnos_id);
      if (!alumno) {
        ctx.response.status = Status.NotFound;
        ctx.response.body = { success: false, error: "Alumno no encontrado" };
        return;
      }
      
      const foto = await FotoModel.create(data);
      ctx.response.status = Status.Created;
      ctx.response.body = { success: true, data: foto };
    } catch (error) {
      ctx.response.status = Status.InternalServerError;
      ctx.response.body = { success: false, error: (error instanceof Error) ? error.message : "Unknown error" };
    }
  }

  static async updateFoto(ctx: RouterContext<"/fotos/:id", { id: string }>) {
    try {
      const id = parseInt(ctx.params.id);
      if (isNaN(id)) {
        ctx.response.status = Status.BadRequest;
        ctx.response.body = { success: false, error: "ID inválido" };
        return;
      }

      const body = ctx.request.body;
      if (!body.type || body.type !== "json") {
        ctx.response.status = Status.BadRequest;
        ctx.response.body = { success: false, error: "Datos inválidos" };
        return;
      }
      
      const data = await body.value as { url: string };
      
      if (!data.url) {
        ctx.response.status = Status.BadRequest;
        ctx.response.body = { success: false, error: "URL es requerida" };
        return;
      }

      const updatedFoto = await FotoModel.update(id, data.url);
      if (!updatedFoto) {
        ctx.response.status = Status.NotFound;
        ctx.response.body = { success: false, error: "Foto no encontrada" };
        return;
      }

      ctx.response.body = { success: true, data: updatedFoto };
    } catch (error) {
      ctx.response.status = Status.InternalServerError;
      ctx.response.body = { success: false, error: (error instanceof Error) ? error.message : "Unknown error" };
    }
  }

  static async deleteFoto(ctx: RouterContext<"/fotos/:id", { id: string }>) {
    try {
      const id = parseInt(ctx.params.id);
      if (isNaN(id)) {
        ctx.response.status = Status.BadRequest;
        ctx.response.body = { success: false, error: "ID inválido" };
        return;
      }

      const success = await FotoModel.delete(id);
      if (!success) {
        ctx.response.status = Status.NotFound;
        ctx.response.body = { success: false, error: "Foto no encontrada" };
        return;
      }

      ctx.response.body = { success: true, message: "Foto eliminada correctamente" };
    } catch (error) {
      ctx.response.status = Status.InternalServerError;
      ctx.response.body = { success: false, error: (error instanceof Error) ? error.message : "Unknown error" };
    }
  }
}
