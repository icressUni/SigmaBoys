// api/deps.ts
export {
  serve,
  Server,
} from "https://deno.land/std@0.203.0/http/server.ts";

export { Pool } from "https://deno.land/x/postgres@v0.17.0/mod.ts";
export * as bcrypt from "https://deno.land/x/bcrypt@v0.4.1/mod.ts"; // versión compatible con Deno
