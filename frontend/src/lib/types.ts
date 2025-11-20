// src/lib/types.ts
export type Session = {
  id: number;
  date: string; // YYYY-MM-DD
  start_time?: string | null; // HH:MM:SS
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
};
