
import api from "./api";
import type { Signup } from "./types";

export const listSignups = async (): Promise<Signup[]> => {
  const { data } = await api.get("/api/signups/");
  return data;
};

export const createSignup = async (payload: Pick<Signup, "session"> & Partial<Signup>): Promise<Signup> => {
  const { data } = await api.post("/api/signups/", payload);
  return data;
};

export const updateSignup = async (id: number, payload: Partial<Signup>): Promise<Signup> => {
  const { data } = await api.patch(`/api/signups/${id}/`, payload);
  return data;
};

export const deleteSignup = async (id: number): Promise<void> => {
  await api.delete(`/api/signups/${id}/`);
};
