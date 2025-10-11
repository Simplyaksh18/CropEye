import React, { createContext, useState, useContext, useEffect } from "react";
import { jwtDecode } from "jwt-decode";
import api from "../api/client";

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [loading, setLoading] = useState(true);
  const [claims, setClaims] = useState(null);

  const extractUserProfile = (decoded) => {
    if (!decoded || typeof decoded !== "object") {
      return null;
    }
    if (decoded.user && typeof decoded.user === "object") {
      return decoded.user;
    }
    return {
      id: decoded.sub ?? decoded.id ?? null,
      email: decoded.email ?? null,
      firstName: decoded.firstName ?? null,
      lastName: decoded.lastName ?? null,
      farmName: decoded.farmName ?? null,
      location: decoded.location ?? null,
      createdAt: decoded.createdAt ?? null,
    };
  };

  useEffect(() => {
    if (token) {
      try {
        const decoded = jwtDecode(token);
        if (decoded.sub && typeof decoded.sub === "object") {
          // Legacy token shape with object identity - force refresh to avoid backend errors
          localStorage.removeItem("token");
          setToken(null);
          setClaims(null);
          setUser(null);
          setLoading(false);
          return;
        }

        if (!decoded.exp || decoded.exp * 1000 > Date.now()) {
          setClaims(decoded);
          setUser(extractUserProfile(decoded));
        } else {
          localStorage.removeItem("token");
          setToken(null);
          setClaims(null);
          setUser(null);
        }
      } catch (error) {
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

  const login = async (email, password) => {
    try {
      const { data } = await api.post("/login", { email, password });
      if (data?.token) {
        localStorage.setItem("token", data.token);
        setToken(data.token);
        return { success: true };
      }
      return { success: false, error: data?.message || "Login failed" };
    } catch (err) {
      const msg = err.response?.data?.message || err.message || "Login failed";
      return { success: false, error: msg };
    }
  };

  const register = async (userData) => {
    try {
      const { data } = await api.post("/register", userData);
      if (data?.token) {
        localStorage.setItem("token", data.token);
        setToken(data.token);
        return { success: true };
      }
      return { success: false, error: data?.message || "Registration failed" };
    } catch (err) {
      const msg =
        err.response?.data?.message || err.message || "Registration failed";
      return { success: false, error: msg };
    }
  };

  const logout = async () => {
    try {
      await api.post("/logout");
    } catch (error) {
      // ignore network errors on logout
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
        login,
        register,
        logout,
        getAuthHeader,
        isAuthenticated: !!user,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};
