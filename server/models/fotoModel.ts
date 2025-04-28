import { getClient } from "../config/db.ts";

export interface Foto {
  id: number;
  alumnos_id: number;
  url: string;
}

export type CreateFotoDto = Omit<Foto, "id">;

export class FotoModel {
  static async findAll(): Promise<Foto[]> {
    const client = await getClient();
    try {
      const result = await client.queryObject<Foto>(
        "SELECT id, alumnos_id, url FROM fotos;"
      );
      return result.rows;
    } finally {
      client.release();
    }
  }

  static async findById(id: number): Promise<Foto | null> {
    const client = await getClient();
    try {
      const result = await client.queryObject<Foto>(
        "SELECT id, alumnos_id, url FROM fotos WHERE id = $1;",
        [id]
      );
      return result.rows[0] || null;
    } finally {
      client.release();
    }
  }

  static async findByAlumnoId(alumnoId: number): Promise<Foto[]> {
    const client = await getClient();
    try {
      const result = await client.queryObject<Foto>(
        "SELECT id, alumnos_id, url FROM fotos WHERE alumnos_id = $1;",
        [alumnoId]
      );
      return result.rows;
    } finally {
      client.release();
    }
  }

  static async create(foto: CreateFotoDto): Promise<Foto> {
    const client = await getClient();
    try {
      const result = await client.queryObject<Foto>(
        "INSERT INTO fotos (alumnos_id, url) VALUES ($1, $2) RETURNING *;",
        [foto.alumnos_id, foto.url]
      );
      return result.rows[0];
    } finally {
      client.release();
    }
  }

  static async update(id: number, url: string): Promise<Foto | null> {
    const client = await getClient();
    try {
      const result = await client.queryObject<Foto>(
        "UPDATE fotos SET url = $1 WHERE id = $2 RETURNING *;",
        [url, id]
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
        "DELETE FROM fotos WHERE id = $1 RETURNING id;",
        [id]
      );
      return result.rows.length > 0;
    } finally {
      client.release();
    }
  }
}
