import api, { setTokens, clearTokens } from "./api";
import type { TokenPair } from "./types";

export const login = async (username: string, password: string): Promise<TokenPair> => {
  const { data } = await api.post<TokenPair>("/api/token/", { username, password });
  return data;
};

export const logout = () => {
  clearTokens();
};

export const refreshToken = async (refresh: string): Promise<TokenPair> => {
  const { data } = await api.post<TokenPair>("/api/token/refresh/", { refresh });
  setTokens(data.access, refresh);
  return { access: data.access, refresh };
};
