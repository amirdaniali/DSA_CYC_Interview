/**
 * Authentication helpers for login and signup.
 * These functions talk directly to your Django backend.
 */

import api from "./api";

// Response returned by login/signup endpoints
export type AuthResponse = {
  access: string;
  refresh: string;
  id: number;
  username: string;
  email: string;
  full_name: string;
  discord_username: string;
  role: "admin" | "user";
};

// Payload for signup
export type SignupPayload = {
  username: string;
  email: string;
  full_name: string;
  discord_username: string;
  password: string;
};

/**
 * Login user with username + password.
 * Calls Django /accounts/token/ endpoint.
 */
export async function login(username: string, password: string): Promise<AuthResponse> {
  const { data } = await api.post("/accounts/token/", { username, password });
  return data;
}

/**
 * Signup user with required fields.
 * Calls Django /accounts/signup/ endpoint.
 */
export async function signup(payload: SignupPayload): Promise<AuthResponse> {
  const { data } = await api.post("/accounts/signup/", payload);
  return data;
}

/**
 * Logout helper (optional).
 * If you have a backend logout endpoint, call it here.
 * Otherwise just clear localStorage in AuthContext.
 */
export function logout() {
  // placeholder
}
