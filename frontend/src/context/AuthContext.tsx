// src/context/AuthContext.tsx

import React, { createContext, useState, useEffect } from "react";
import type { User } from "../types";

interface AuthContextType {
  isAuthenticated: boolean;
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  loading: boolean;
}

export const AuthContext = createContext<AuthContextType | undefined>(
  undefined
);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check for existing auth token on mount
    const token = localStorage.getItem("token");
    const storedUser = localStorage.getItem("user");

    if (token && storedUser) {
      try {
        setIsAuthenticated(true);
        setUser(JSON.parse(storedUser));
      } catch (error) {
        console.error("Error parsing stored user data:", error);
        // Clear invalid data
        localStorage.removeItem("token");
        localStorage.removeItem("user");
      }
    }
    setLoading(false);
  }, []);

  const login = async (email: string, password: string) => {
    // Mock authentication - replace with actual API call
    // In production: await apiClient.post('/auth/login', { email, password })
    // read password to avoid unused parameter error
    void password;

    return new Promise<void>((resolve) => {
      setTimeout(() => {
        const mockToken = "mock-jwt-token-" + Date.now();
        const mockUser: User = {
          id: "mock-id",
          email,
          name: email.split("@")[0],
        };

        localStorage.setItem("token", mockToken);
        localStorage.setItem("user", JSON.stringify(mockUser));

        setIsAuthenticated(true);
        setUser(mockUser);
        resolve();
      }, 500);
    });
  };

  const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    setIsAuthenticated(false);
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{ isAuthenticated, user, login, logout, loading }}
    >
      {children}
    </AuthContext.Provider>
  );
};
