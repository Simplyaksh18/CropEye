import axios from "axios";

const defaultBaseUrl = process.env.REACT_APP_API_BASE
  ? process.env.REACT_APP_API_BASE
  : process.env.NODE_ENV === "development"
  ? "http://localhost:5000/api"
  : "/api";

const api = axios.create({
  baseURL: defaultBaseUrl,
  timeout: 20000,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (resp) => resp,
  (error) => {
    if (error.response && error.response.status === 401) {
      // optional: trigger logout
    }
    return Promise.reject(error);
  }
);

export default api;
