// src/contexts/AuthContext.tsx
/* eslint-disable react-refresh/only-export-components */
// Authentication context compatible with your backend API

import React, { createContext, useState, useContext, useEffect } from "react";
import type { ReactNode } from "react";
import { jwtDecode } from "jwt-decode";
import api from "../api/api-client";

interface User {
  id: string | null;
  email: string | null;
  firstName: string | null;
  lastName: string | null;
  farmName: string | null;
  location: string | null;
  createdAt: string | null;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  loading: boolean;
  claims: unknown | null;
  isAuthenticated: boolean;
  login: (
    email: string,
    password: string
  ) => Promise<{ success: boolean; error?: string }>;
  register: (
    userData: unknown
  ) => Promise<{ success: boolean; error?: string }>;
  logout: () => Promise<void>;
  getAuthHeader: () => { Authorization?: string };
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(
    localStorage.getItem("token")
  );
  const [loading, setLoading] = useState(true);
  const [claims, setClaims] = useState<unknown | null>(null);

  const extractUserProfile = (decoded: unknown): User | null => {
    if (!decoded || typeof decoded !== "object") {
      return null;
    }
    // decoded is unknown but may be a token payload object
    const d = decoded as Record<string, unknown>;

    if (d.user && typeof d.user === "object") {
      return d.user as User;
    }

    const getString = (k: string) =>
      typeof d[k] === "string" ? (d[k] as string) : null;

    return {
      id: getString("sub") ?? getString("id"),
      email: getString("email"),
      firstName: getString("firstName"),
      lastName: getString("lastName"),
      farmName: getString("farmName"),
      location: getString("location"),
      createdAt: getString("createdAt"),
    };
  };

  useEffect(() => {
    if (token) {
      try {
        const decoded = jwtDecode<unknown>(token as string);

        // cast to record for checks
        const d = decoded as Record<string, unknown>;

        // Check for legacy token shape
        if (d.sub && typeof d.sub === "object") {
          localStorage.removeItem("token");
          setToken(null);
          setClaims(null);
          setUser(null);
          setLoading(false);
          return;
        }

        // Check token expiration
        const exp = typeof d.exp === "number" ? d.exp : undefined;
        if (!exp || exp * 1000 > Date.now()) {
          setClaims(decoded);
          setUser(extractUserProfile(decoded));
        } else {
          localStorage.removeItem("token");
          setToken(null);
          setClaims(null);
          setUser(null);
        }
      } catch (err) {
        console.error(err);
        localStorage.removeItem("token");
        setToken(null);
        setClaims(null);
        setUser(null);
      }
    } else {
      setClaims(null);
      setUser(null);
    }

    setLoading(false);
  }, [token]);

  const login = async (email: string, password: string) => {
    try {
      const { data } = await api.post("/login", { email, password });

      if (data?.token) {
        localStorage.setItem("token", data.token);
        setToken(data.token);
        return { success: true };
      }

      return { success: false, error: data?.message || "Login failed" };
    } catch (err) {
      const e = err as {
        response?: { data?: { message?: string } };
        message?: string;
      };
      const msg = e.response?.data?.message || e.message || "Login failed";
      return { success: false, error: msg };
    }
  };

  const register = async (userData: unknown) => {
    try {
      const { data } = await api.post("/register", userData);

      if (data?.token) {
        localStorage.setItem("token", data.token);
        setToken(data.token);
        return { success: true };
      }

      return { success: false, error: data?.message || "Registration failed" };
    } catch (err) {
      const e = err as {
        response?: { data?: { message?: string } };
        message?: string;
      };
      const msg =
        e.response?.data?.message || e.message || "Registration failed";
      return { success: false, error: msg };
    }
  };

  const logout = async () => {
    try {
      await api.post("/logout");
    } catch (err) {
      console.error(err);
      // Ignore network errors on logout
    }

    localStorage.removeItem("token");
    setToken(null);
    setUser(null);
    setClaims(null);
  };

  const getAuthHeader = () => {
    return token ? { Authorization: `Bearer ${token}` } : {};
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        loading,
        claims,
        isAuthenticated: !!token && !!user,
        login,
        register,
        logout,
        getAuthHeader,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};
