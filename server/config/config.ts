import { load } from "https://deno.land/std@0.210.0/dotenv/mod.ts";

// Load environment variables
await load({ export: true });

export const config = {
  PORT: Number(Deno.env.get("PORT")) || 8000,
  DB: {
    host: Deno.env.get("DB_HOST") || "localhost",
    port: Number(Deno.env.get("DB_PORT")) || 5432,
    database: Deno.env.get("DB_NAME") || "sigmadatabase",
    user: Deno.env.get("DB_USER") || "postgres",
    password: Deno.env.get("DB_PASSWORD") || "postgres",
  },
  JWT_SECRET: Deno.env.get("JWT_SECRET") || "default_secret_key_change_this"
};
