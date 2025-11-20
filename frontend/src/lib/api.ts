
import axios from "axios";

const API_BASE = import.meta.env.VITE_API_BASE ?? "";
console.log(API_BASE)

let accessToken: string | null = null;
let refreshToken: string | null = null;

export const setTokens = (access: string, refresh: string) => {
  accessToken = access;
  refreshToken = refresh;
};

const api = axios.create({
  baseURL: API_BASE,
});

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
      original.headers.Authorization = `Bearer ${accessToken}`;
      return api(original);
    }
    return Promise.reject(err);
  }
);

export default api;
