import axios from "axios";

const API_BASE = import.meta.env.VITE_API_BASE ?? "http://127.0.0.1:8000";

let accessToken: string | null = localStorage.getItem("access");
let refreshToken: string | null = localStorage.getItem("refresh");

export const setTokens = (access: string, refresh: string) => {
  accessToken = access;
  refreshToken = refresh;
  localStorage.setItem("access", access);
  localStorage.setItem("refresh", refresh);
};

export const clearTokens = () => {
  accessToken = null;
  refreshToken = null;
  localStorage.removeItem("access");
  localStorage.removeItem("refresh");
};

const api = axios.create({ baseURL: API_BASE });

api.interceptors.request.use((config) => {
  if (accessToken) {
    config.headers.Authorization = `Bearer ${accessToken}`;
  }
  return config;
});

api.interceptors.response.use(
  (res) => res,
  async (err) => {
    const original = err.config;
    if (err.response?.status === 401 && refreshToken && !original._retry) {
      original._retry = true;
      const { data } = await axios.post(`${API_BASE}/api/token/refresh/`, { refresh: refreshToken });
      accessToken = data.access;
      localStorage.setItem("access", accessToken as string);
      original.headers.Authorization = `Bearer ${accessToken}`;
      return api(original);
    }
    return Promise.reject(err);
  }
);

export default api;
