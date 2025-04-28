import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import * as path from "node:path";

export default defineConfig({
  root: "./client",  // Ajusta según la estructura de tu proyecto
  server: {
    port: 3000,
    proxy: {
      "/api": "http://localhost:8000",  // Proxy para redirigir las solicitudes a la API en Deno
    },
  },
  plugins: [
    react(),
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './client/src'),
      '@components': path.resolve(__dirname, './client/src/componentes'),
      '@pages': path.resolve(__dirname, './client/src/pages'),
    }
  },
  optimizeDeps: {
    include: ["face-api.js"],  // Incluye face-api.js en las dependencias si es necesario
  },
});
