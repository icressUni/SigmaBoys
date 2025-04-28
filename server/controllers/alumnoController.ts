import { Context, RouterContext, Status } from "@oak/oak";
import { AlumnoModel, CreateAlumnoDto, UpdateAlumnoDto } from "../models/alumnoModel.ts";

export class AlumnoController {
  static async getAlumnos(ctx: Context) {
    try {
      const alumnos = await AlumnoModel.findAll();
      ctx.response.body = { success: true, data: alumnos };
    } catch (error) {
      ctx.response.status = Status.InternalServerError;
      ctx.response.body = { success: false, error: (error instanceof Error) ? error.message : "Unknown error" };
    }
  }

  static async getAlumnoById(ctx: RouterContext<"/alumnos/:id", { id: string }>) {
    try {
      const id = parseInt(ctx.params.id);
      if (isNaN(id)) {
        ctx.response.status = Status.BadRequest;
        ctx.response.body = { success: false, error: "ID inválido" };
        return;
      }

      const alumno = await AlumnoModel.findById(id);
      if (!alumno) {
        ctx.response.status = Status.NotFound;
        ctx.response.body = { success: false, error: "Alumno no encontrado" };
        return;
      }

      ctx.response.body = { success: true, data: alumno };
    } catch (error) {
      ctx.response.status = Status.InternalServerError;
      ctx.response.body = { success: false, error: (error instanceof Error) ? error.message : "Unknown error"};
    }
  }

  static async createAlumno(ctx: Context) {
    try {
      const body = ctx.request.body;
      if (!body.type || body.type !== "json") {
        ctx.response.status = Status.BadRequest;
        ctx.response.body = { success: false, error: "Datos inválidos" };
        return;
      }
      
      const data = await body.value as CreateAlumnoDto;
      
      // Validate required fields
      if (!data.nombres || !data.apellidos || !data.rut || !data.password) {
        ctx.response.status = Status.BadRequest;
        ctx.response.body = { success: false, error: "Todos los campos son requeridos" };
        return;
      }
      
      // Check if RUT already exists
      const existingAlumno = await AlumnoModel.findByRut(data.rut);
      if (existingAlumno) {
        ctx.response.status = Status.Conflict;
        ctx.response.body = { success: false, error: "El RUT ya está registrado" };
        return;
      }
      
      const alumno = await AlumnoModel.create(data);
      ctx.response.status = Status.Created;
      ctx.response.body = { success: true, data: alumno };
    } catch (error) {
      ctx.response.status = Status.InternalServerError;
      ctx.response.body = { success: false, error: (error instanceof Error) ? error.message : "Unknown error" };
    }
  }

  static async updateAlumno(ctx: RouterContext<"/alumnos/:id", { id: string }>) {
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
      
      const data = await body.value as UpdateAlumnoDto;
      
      // Check if alumno exists
      const existingAlumno = await AlumnoModel.findById(id);
      if (!existingAlumno) {
        ctx.response.status = Status.NotFound;
        ctx.response.body = { success: false, error: "Alumno no encontrado" };
        return;
      }
      
      // If updating RUT, check if it's not already used
      if (data.rut && data.rut !== existingAlumno.rut) {
        const alumnoByRut = await AlumnoModel.findByRut(data.rut);
        if (alumnoByRut) {
          ctx.response.status = Status.Conflict;
          ctx.response.body = { success: false, error: "El RUT ya está registrado" };
          return;
        }
      }
      
      const updatedAlumno = await AlumnoModel.update(id, data);
      ctx.response.body = { success: true, data: updatedAlumno };
    } catch (error) {
      ctx.response.status = Status.InternalServerError;
      ctx.response.body = { success: false, error: (error instanceof Error) ? error.message : "Unknown error"};
    }
  }

  static async deleteAlumno(ctx: RouterContext<"/alumnos/:id", { id: string }>) {
    try {
      const id = parseInt(ctx.params.id);
      if (isNaN(id)) {
        ctx.response.status = Status.BadRequest;
        ctx.response.body = { success: false, error: "ID inválido" };
        return;
      }

      const success = await AlumnoModel.delete(id);
      if (!success) {
        ctx.response.status = Status.NotFound;
        ctx.response.body = { success: false, error: "Alumno no encontrado" };
        return;
      }

      ctx.response.body = { success: true, message: "Alumno eliminado correctamente" };
    } catch (error) {
      ctx.response.status = Status.InternalServerError;
      ctx.response.body = { success: false, error: (error instanceof Error) ? error.message : "Unknown error" };
    }
  }
  
  static async login(ctx: Context) {
    try {
      const body = ctx.request.body;
      if (!body.type || body.type !== "json") {
        ctx.response.status = Status.BadRequest;
        ctx.response.body = { success: false, error: "Datos inválidos" };
        return;
      }
      
      const { rut, password } = await body.value as { rut: string; password: string };
      
      if (!rut || !password) {
        ctx.response.status = Status.BadRequest;
        ctx.response.body = { success: false, error: "RUT y contraseña son requeridos" };
        return;
      }
      
      const isValid = await AlumnoModel.verifyPassword(rut, password);
      if (!isValid) {
        ctx.response.status = Status.Unauthorized;
        ctx.response.body = { success: false, error: "Credenciales inválidas" };
        return;
      }
      
      const alumno = await AlumnoModel.findByRut(rut);
      
      // Generate JWT token
      const token = await createToken({
        id: alumno!.id,
        rut: alumno!.rut,
        admin: alumno!.admin
      });
      
      ctx.response.body = { 
        success: true, 
        data: {
          id: alumno!.id,
          nombres: alumno!.nombres,
          apellidos: alumno!.apellidos,
          rut: alumno!.rut,
          admin: alumno!.admin,
          token: token
        }
      };
    } catch (error) {
      ctx.response.status = Status.InternalServerError;
      ctx.response.body = { success: false, error: (error instanceof Error) ? error.message : "Unknown error" };
    }
  }
}
