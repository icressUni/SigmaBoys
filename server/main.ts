import { Application } from "@oak/oak";
import { config } from "./config/config.ts";
import { router } from "./routes/index.ts";
import { errorMiddleware } from "./middleware/errorMiddleware.ts";
import { logger } from "./middleware/loggerMiddleware.ts";
import { initializeDb } from "./config/db.ts";

// Initialize database
try {
  await initializeDb();
  console.log("Database initialized successfully");
} catch (error) {
  console.error("Error initializing database:", error);
  Deno.exit(1);
}

const app = new Application();

// Middleware
app.use(logger);
app.use(errorMiddleware);
app.use(router.routes());
app.use(router.allowedMethods());

console.log(`Server running on http://localhost:${config.PORT}`);

await app.listen({ port: config.PORT });
