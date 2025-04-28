import { getClient } from "../config/db.ts";
import { hash, compare } from "https://deno.land/x/bcrypt@v0.4.1/mod.ts";

export interface Alumno {
  id: number;
  nombres: string;
  apellidos: string;
  rut: string;
  password: string;
  admin: boolean;
}

export type CreateAlumnoDto = Omit<Alumno, "id">;
export type UpdateAlumnoDto = Partial<Omit<Alumno, "id">>;

export class AlumnoModel {
  static async findAll(): Promise<Alumno[]> {
    const client = await getClient();
    try {
      const result = await client.queryObject<Alumno>(
        "SELECT id, nombres, apellidos, rut, password, admin FROM alumnos;"
      );
      return result.rows;
    } finally {
      client.release();
    }
  }

  static async findById(id: number): Promise<Alumno | null> {
    const client = await getClient();
    try {
      const result = await client.queryObject<Alumno>(
        "SELECT id, nombres, apellidos, rut, password, admin FROM alumnos WHERE id = $1;",
        [id]
      );
      return result.rows[0] || null;
    } finally {
      client.release();
    }
  }

  static async findByRut(rut: string): Promise<Alumno | null> {
    const client = await getClient();
    try {
      const result = await client.queryObject<Alumno>(
        "SELECT id, nombres, apellidos, rut, password, admin FROM alumnos WHERE rut = $1;",
        [rut]
      );
      return result.rows[0] || null;
    } finally {
      client.release();
    }
  }

  static async create(alumno: CreateAlumnoDto): Promise<Alumno> {
    // Hash password before storing
    const hashedPassword = await hash(alumno.password);
    
    const client = await getClient();
    try {
      const result = await client.queryObject<Alumno>(
        "INSERT INTO alumnos (nombres, apellidos, rut, password, admin) VALUES ($1, $2, $3, $4, $5) RETURNING *;",
        [alumno.nombres, alumno.apellidos, alumno.rut, hashedPassword, alumno.admin]
      );
      return result.rows[0];
    } finally {
      client.release();
    }
  }

  static async update(id: number, alumno: UpdateAlumnoDto): Promise<Alumno | null> {
    const client = await getClient();
    
    try {
      // Get current data to only update provided fields
      const current = await this.findById(id);
      if (!current) return null;

      // If password is being updated, hash it
      let password = current.password;
      if (alumno.password) {
        password = await hash(alumno.password);
      }

      const result = await client.queryObject<Alumno>(
        `UPDATE alumnos SET 
          nombres = $1, 
          apellidos = $2, 
          rut = $3, 
          password = $4, 
          admin = $5 
        WHERE id = $6 RETURNING *;`,
        [
          alumno.nombres || current.nombres,
          alumno.apellidos || current.apellidos,
          alumno.rut || current.rut,
          password,
          alumno.admin !== undefined ? alumno.admin : current.admin,
          id
        ]
      );
      
      return result.rows[0] || null;
    } finally {
      client.release();
    }
  }

  static async delete(id: number): Promise<boolean> {
    const client = await getClient();
    try {
      const result = await client.queryObject(
        "DELETE FROM alumnos WHERE id = $1 RETURNING id;",
        [id]
      );
      return result.rows.length > 0;
    } finally {
      client.release();
    }
  }

  static async verifyPassword(rut: string, password: string): Promise<boolean> {
    const alumno = await this.findByRut(rut);
    if (!alumno) return false;
    
    return await compare(password, alumno.password);
  }
}
