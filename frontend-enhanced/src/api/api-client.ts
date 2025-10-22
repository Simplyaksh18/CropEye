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

export default api;
