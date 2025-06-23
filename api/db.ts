// api/db.ts
import { Pool } from "./deps.ts";

const DATABASE_URL =
  "postgresql://alumnos_db_owner:npg_S7BvNrnaRLy5@ep-rapid-glitter-aaxbrr0d-pooler.westus3.azure.neon.tech/alumnos_db?sslmode=require";

const pool = new Pool(DATABASE_URL, 3, true);

export async function getConnection() {
  const client = await pool.connect();
  return client;
}
