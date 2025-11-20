import api from "./api";
import type { Session } from "./types";


export const listSessions = async (): Promise<Session[]> => {
  const url = "/api/sessions/";
  const { data } = await api.get(url);
  return data;
};


export const createSession = async (payload: Partial<Session>): Promise<Session> => {
  const { data } = await api.post("/api/sessions/", payload);
  return data;
};

export const updateSession = async (id: number, payload: Partial<Session>): Promise<Session> => {
  const { data } = await api.patch(`/api/sessions/${id}/`, payload);
  return data;
};

export const deleteSession = async (id: number): Promise<void> => {
  await api.delete(`/api/sessions/${id}/`);
};
