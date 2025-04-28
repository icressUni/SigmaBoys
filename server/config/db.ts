import { Pool } from "https://deno.land/x/postgres@v0.17.0/mod.ts";
import { config } from "./config.ts";

const POOL_CONNECTIONS = 20;
const pool = new Pool(config.DB, POOL_CONNECTIONS);

export async function getClient() {
  return await pool.connect();
}

// Initialize database with tables if not exists
export async function initializeDb() {
  const client = await getClient();
  
  try {
    // Create Alumno table
    await client.queryObject(`
      CREATE TABLE IF NOT EXISTS alumnos (
        id SERIAL PRIMARY KEY,
        nombres VARCHAR(255) NOT NULL,
        apellidos VARCHAR(255) NOT NULL,
        rut VARCHAR(13) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        admin BOOLEAN NOT NULL DEFAULT FALSE
      );
    `);

    // Create Asistencia table
    await client.queryObject(`
      CREATE TABLE IF NOT EXISTS asistencias (
        id SERIAL PRIMARY KEY,
        alumnos_id INTEGER NOT NULL,
        registro TIMESTAMP WITH TIME ZONE NOT NULL,
        CONSTRAINT fk_alumno FOREIGN KEY (alumnos_id) REFERENCES alumnos(id)
      );
    `);

    // Create Fotos table
    await client.queryObject(`
      CREATE TABLE IF NOT EXISTS fotos (
        id SERIAL PRIMARY KEY,
        alumnos_id INTEGER NOT NULL,
        url VARCHAR(255) NOT NULL,
        CONSTRAINT fk_alumno_foto FOREIGN KEY (alumnos_id) REFERENCES alumnos(id)
      );
    `);
    
    console.log("Database initialized successfully");
  } catch (error) {
    console.error("Error initializing database:", error);
    throw error;
  } finally {
    client.release();
  }
}
