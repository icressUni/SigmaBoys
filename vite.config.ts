// vite.config.ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import * as path from "node:path";

export default defineConfig({
  root: "./client",
  build: {
    outDir: "../dist",
    emptyOutDir: true,
  },
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './client/src'),
      '@components': path.resolve(__dirname, './client/src/componentes'),
      '@pages': path.resolve(__dirname, './client/src/pages'),
    },
  },
  server: {
    port: 3000,           // Aquí fijas el puerto a 3000
    strictPort: true,     // Para que falle si 3000 está ocupado (en vez de cambiar automáticamente)
  },
});
