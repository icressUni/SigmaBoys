import { getClient } from "../config/db.ts";

export interface Asistencia {
  id: number;
  alumnos_id: number;
  registro: Date;
}

export type CreateAsistenciaDto = Omit<Asistencia, "id">;

export class AsistenciaModel {
  static async findAll(): Promise<Asistencia[]> {
    const client = await getClient();
    try {
      const result = await client.queryObject<Asistencia>(
        "SELECT id, alumnos_id, registro FROM asistencias;"
      );
      return result.rows;
    } finally {
      client.release();
    }
  }

  static async findById(id: number): Promise<Asistencia | null> {
    const client = await getClient();
    try {
      const result = await client.queryObject<Asistencia>(
        "SELECT id, alumnos_id, registro FROM asistencias WHERE id = $1;",
        [id]
      );
      return result.rows[0] || null;
    } finally {
      client.release();
    }
  }

  static async findByAlumnoId(alumnoId: number): Promise<Asistencia[]> {
    const client = await getClient();
    try {
      const result = await client.queryObject<Asistencia>(
        "SELECT id, alumnos_id, registro FROM asistencias WHERE alumnos_id = $1 ORDER BY registro DESC;",
        [alumnoId]
      );
      return result.rows;
    } finally {
      client.release();
    }
  }

  static async create(asistencia: CreateAsistenciaDto): Promise<Asistencia> {
    const client = await getClient();
    try {
      const result = await client.queryObject<Asistencia>(
        "INSERT INTO asistencias (alumnos_id, registro) VALUES ($1, $2) RETURNING *;",
        [asistencia.alumnos_id, asistencia.registro]
      );
      return result.rows[0];
    } finally {
      client.release();
    }
  }

  static async delete(id: number): Promise<boolean> {
    const client = await getClient();
    try {
      const result = await client.queryObject(
        "DELETE FROM asistencias WHERE id = $1 RETURNING id;",
        [id]
      );
      return result.rows.length > 0;
    } finally {
      client.release();
    }
  }
}
