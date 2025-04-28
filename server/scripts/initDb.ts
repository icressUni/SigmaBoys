import { initializeDb } from "../config/db.ts";

try {
  console.log("Initializing database...");
  await initializeDb();
  console.log("Database initialization complete.");
} catch (error) {
  console.error("Failed to initialize database:", error);
  Deno.exit(1);
}
