export type Session = {
  id: number;
  date: string;
  start_time?: string | null;
  end_time?: string | null;
  capacity?: number;
  is_active?: boolean;
  signup_count: number;
};

export type Signup = {
  id: number;
  session: number;
  lc_level?: "easy" | "medium" | "hard" | "none" | null;
  discord_username?: string | null;
  status?: "active" | "canceled";
  created_at: string;
};

export type TokenPair = {
  access: string;
  refresh: string;
  // optional: backend can include role info
  is_admin?: boolean;
};



// src/lib/types.ts
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

export type User = {
  id: number;
  username: string;
  fullname: string;
  email: string;
  discord_id: string;
  isAdmin: boolean;
};
