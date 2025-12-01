import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      "/api/ndvi": {
        target: "http://localhost:5001",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api\/ndvi/, ""),
      },
      "/api/soil": {
        target: "http://localhost:5000",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api\/soil/, "/api"),
      },
      "/api/weather": {
        target: "http://localhost:5003",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api\/weather/, "/api/weather"),
      },
      "/api/crops": {
        target: "http://localhost:5004",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api\/crops/, ""),
      },
      "/api/water": {
        target: "http://localhost:5005",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api\/water/, "/api"),
      },
      "/api/pests": {
        target: "http://localhost:5006",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api\/pests/, "/api"),
      },
    },
  },
});
