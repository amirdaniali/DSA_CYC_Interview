import { createContext, useContext, useState, useEffect } from "react";
import type { User, AuthResponse } from "@/lib/types";
import { login as apiLogin, logout as apiLogout } from "@/lib/auth";

type AuthContextType = {
    user: User | null;
    loginUser: (username: string, password: string) => Promise<void>;
    logoutUser: () => void;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
    const [user, setUser] = useState<User | null>(null);

    // Restore user from localStorage on mount
    useEffect(() => {
        const storedUser = localStorage.getItem("user");
        if (storedUser) {
            const parsed = JSON.parse(storedUser);
            console.log("[AuthContext] Loaded user from localStorage:", parsed);
            setUser(parsed);
        }
    }, []);

    // --- loginUser updates context + localStorage ---
    const loginUser = async (username: string, password: string) => {
        const data: AuthResponse = await apiLogin(username, password);
        console.log("[AuthContext] Login API response:", data);

        const u: User = {
            id: data.id,
            username: data.username,
            fullname: data.full_name,
            email: data.email,
            discord_id: data.discord_username,
            isAdmin: data.role === "admin",
        };

        localStorage.setItem("access", data.access);
        localStorage.setItem("refresh", data.refresh);
        localStorage.setItem("user", JSON.stringify(u));

        setUser(u);
        console.log("[AuthContext] User set in context:", u);
    };

    const logoutUser = () => {
        apiLogout();
        localStorage.removeItem("access");
        localStorage.removeItem("refresh");
        localStorage.removeItem("user");
        setUser(null);
        console.log("[AuthContext] User logged out, context cleared");
    };

    return (
        <AuthContext.Provider value={{ user, loginUser, logoutUser }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const ctx = useContext(AuthContext);
    if (!ctx) throw new Error("useAuth must be used within AuthProvider");
    return ctx;
};
