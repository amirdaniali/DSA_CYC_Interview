// src/lib/auth.ts
import api from "./api";
import { setTokens } from "./api";
import type { TokenPair } from "./types";

export const login = async (username: string, password: string): Promise<void> => {
  const { data } = await api.post<TokenPair>("/api/token/", { username, password });
  setTokens(data.access, data.refresh);
};
