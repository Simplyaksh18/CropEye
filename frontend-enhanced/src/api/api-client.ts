// src/api/client.ts
// Axios client configured for your backend

import axios from "axios";

// Use Vite environment variables (import.meta.env). Vite exposes VITE_* vars.
type ViteMeta = {
  env?: { VITE_API_BASE?: string; DEV?: boolean };
} & ImportMeta;
const meta = import.meta as ViteMeta;
const envBase = meta.env?.VITE_API_BASE;
const isDev = !!meta.env?.DEV;
const defaultBaseUrl = envBase
  ? envBase
  : isDev
  ? "http://localhost:5000/api"
  : "/api";

const api = axios.create({
  baseURL: defaultBaseUrl,
  timeout: 20000,
});

// Request interceptor - auto-attach token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    // headers may be undefined or a plain object; merge safely
    config.headers = {
      ...(config.headers || {}),
      Authorization: `Bearer ${token}`,
    } as typeof config.headers;
  }
  return config;
});

// Response interceptor - handle auth errors
api.interceptors.response.use(
  (resp) => resp,
  (error) => {
    if (error.response && error.response.status === 401) {
      // Optional: trigger logout or redirect to login
      localStorage.removeItem("token");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

// Development-friendly logging: print request/response info to console when running in dev
if (meta.env?.DEV) {
  api.interceptors.request.use(
    (config) => {
      try {
        const fullUrl = `${config.baseURL ?? ""}${config.url ?? ""}`;

        console.debug(
          "[API REQUEST]",
          (config.method || "GET").toUpperCase(),
          fullUrl,
          {
            headers: config.headers,
            data: config.data,
          }
        );
      } catch {
        /* ignore */
      }
      return config;
    },
    (err) => Promise.reject(err)
  );

  api.interceptors.response.use(
    (resp) => {
      try {
        const cfg = resp.config || {};

        console.debug(
          "[API RESPONSE]",
          (cfg.method || "GET").toUpperCase(),
          `${cfg.baseURL ?? ""}${cfg.url ?? ""}`,
          resp.status,
          resp.data
        );
      } catch {
        /* ignore */
      }
      return resp;
    },
    (err) => {
      try {
        const cfg = err.config || {};
        console.debug(
          "[API ERROR]",
          (cfg.method || "?").toUpperCase(),
          `${cfg.baseURL ?? ""}${cfg.url ?? ""}`,
          err.response?.status,
          err.response?.data || err.message
        );
      } catch {
        /* ignore */
      }
      return Promise.reject(err);
    }
  );
}

export default api;
