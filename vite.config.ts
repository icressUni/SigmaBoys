import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import * as path from "node:path";

export default defineConfig({
  root: "./client",  // Ajusta según la estructura de tu proyecto
  server: {
    port: 3000,
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
    include: ["face-api.js"],  // Incluye face-api.js en las dependencias
  },
});
