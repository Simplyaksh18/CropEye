/// <reference types="vitest" />
import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react() as any],
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          // Split large dependencies into separate chunks
          vendor: ["react", "react-dom", "react-router-dom"],
          ui: [
            "lucide-react",
            "@radix-ui/react-dialog",
            "@radix-ui/react-dropdown-menu",
          ],
          charts: ["recharts"],
          utils: ["axios", "date-fns", "clsx", "tailwind-merge"],
        },
      },
    },
    // Increase chunk size warning limit since we're optimizing
    chunkSizeWarningLimit: 1000,
  },
  server: {
    // Proxy API calls to the backend dev server to avoid CORS and matching /api paths
    proxy: {
      "/api": {
        target: "http://localhost:5000",
        changeOrigin: true,
        secure: false,
        // no rewrite needed: requests to /api/* will be forwarded to the same path on the target
      },
    },
  },
  test: {
    globals: true,
    environment: "jsdom",
    // point to the actual setup file included at project root
    setupFiles: ["./setup.ts"],
    // you might want to disable it, if you don't want to mock CSS imports
    css: true,
  },
});
