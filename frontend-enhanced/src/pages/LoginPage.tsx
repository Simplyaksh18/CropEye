// src/pages/LoginPage.tsx
// Enhanced Login Page with Agriculture Theme & Magic Bento Animations

import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { Mail, Lock, LogIn, Leaf } from "lucide-react";
import { useAuth } from "../context/AuthContext";
import { MagicAuthCard } from "../components/ui/MagicAuthCard";
import { AgricultureFacts } from "../components/ui/AgricultureFacts";
import logo from "../assets/cropeye-logo.svg";
import { LiquidChrome } from "../components/animations/LiquidChrome";

const LoginPage: React.FC = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  // Demo credentials (display only) — click Use demo to autofill
  const DEMO = { email: "demo@cropeye.test", password: "demo1234" };

  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    const result = await login(email, password);

    if (result.success) {
      navigate("/");
    } else {
      setError(result.error || "Login failed");
    }

    setLoading(false);
  };

  return (
    <div className="relative min-h-screen bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50 dark:from-gray-900 dark:via-green-900/20 dark:to-gray-900">
      {/* Decorative animated background */}
      <LiquidChrome className="opacity-60" interactive={false} />
      {/* Animated Background Pattern */}
      <div className="absolute inset-0 opacity-10">
        <div
          className="absolute inset-0"
          style={{
            backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%2310b981' fill-opacity='0.4'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
          }}
        />
      </div>

      <div className="relative z-10 min-h-screen flex items-center justify-center p-6">
        <div className="w-full max-w-6xl grid grid-cols-1 lg:grid-cols-2 gap-8 items-start">
          {/* Left Side - Expanded Content */}
          <div className="space-y-6 px-4 lg:px-0 relative">
            <AgricultureFacts />
            <div className="grid grid-cols-2 gap-4 mt-4">
              <div className="bg-white/5 p-4 rounded-xl">
                <h4 className="text-white font-semibold">NDVI Analysis</h4>
                <p className="text-sm text-gray-200/80">
                  In-depth satellite-derived crop health.
                </p>
              </div>
              <div className="bg-white/5 p-4 rounded-xl">
                <h4 className="text-white font-semibold">Weather & Alerts</h4>
                <p className="text-sm text-gray-200/80">
                  Localized forecasts and pest alerts.
                </p>
              </div>
            </div>
          </div>

          {/* Right Side - Login Card */}
          <div className="flex items-start justify-center">
            <MagicAuthCard className="w-full max-w-lg mx-auto">
              {/* Logo */}
              <div className="flex justify-center mb-6">
                <div className="relative">
                  <div className="w-24 h-24 rounded-full overflow-hidden border-4 border-green-500 shadow-lg">
                    <img
                      src={logo}
                      alt="CropEye Logo"
                      className="w-full h-full object-cover"
                    />
                  </div>
                  <div className="absolute -bottom-2 -right-2 w-10 h-10 bg-green-500 rounded-full flex items-center justify-center shadow-lg">
                    <Leaf className="w-6 h-6 text-white" />
                  </div>
                </div>
              </div>

              {/* Title */}
              <div className="text-center mb-8">
                <h1 className="text-3xl font-bold text-gray-800 dark:text-white mb-2">
                  Welcome Back
                </h1>
                <p className="text-gray-600 dark:text-gray-400">
                  Sign in to your CropEye dashboard
                </p>
              </div>

              {/* Demo credentials (dev) */}
              <div className="mb-4 text-sm text-gray-700 dark:text-gray-300">
                <div className="flex items-center justify-between bg-white/5 dark:bg-gray-800/60 rounded-md p-3 border border-gray-800">
                  <div>
                    <div className="font-semibold">Demo account</div>
                    <div className="text-xs text-gray-300 mt-1">
                      <span className="font-mono">{DEMO.email}</span>
                      <span className="mx-2">/</span>
                      <span className="font-mono">{DEMO.password}</span>
                    </div>
                  </div>
                  <div>
                    <button
                      type="button"
                      onClick={() => {
                        setEmail(DEMO.email);
                        setPassword(DEMO.password);
                      }}
                      className="px-3 py-1 text-sm bg-green-500 text-white rounded-md hover:bg-green-600"
                    >
                      Use demo
                    </button>
                  </div>
                </div>
              </div>

              {/* Error Message */}
              {error && (
                <div className="mb-6 p-4 bg-red-50 dark:bg-red-900/20 border-l-4 border-red-500 rounded-r-lg">
                  <p className="text-sm text-red-700 dark:text-red-300">
                    {error}
                  </p>
                </div>
              )}

              {/* Form */}
              <form onSubmit={handleSubmit} className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Email Address
                  </label>
                  <div className="relative">
                    <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                    <input
                      type="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      required
                      className="w-full pl-10 pr-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all"
                      placeholder="farmer@example.com"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Password
                  </label>
                  <div className="relative">
                    <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                    <input
                      type="password"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      required
                      className="w-full pl-10 pr-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all"
                      placeholder="••••••••"
                    />
                  </div>
                </div>

                <div className="flex items-center justify-between">
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      className="w-4 h-4 text-green-600 border-gray-300 rounded focus:ring-green-500"
                    />
                    <span className="ml-2 text-sm text-gray-700 dark:text-gray-300">
                      Remember me
                    </span>
                  </label>
                  <a
                    href="#"
                    className="text-sm text-green-600 hover:text-green-700 dark:text-green-400"
                  >
                    Forgot password?
                  </a>
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  className="w-full py-3 bg-gradient-to-r from-green-500 to-emerald-600 text-white rounded-lg font-semibold flex items-center justify-center gap-2 hover:from-green-600 hover:to-emerald-700 transition-all transform hover:scale-[1.02] active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed shadow-lg"
                >
                  {loading ? (
                    <div className="w-6 h-6 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  ) : (
                    <>
                      <LogIn className="w-5 h-5" />
                      Sign In
                    </>
                  )}
                </button>
              </form>

              {/* Register Link */}
              <div className="mt-8 text-center">
                <p className="text-gray-600 dark:text-gray-400 text-sm">
                  Don't have an account?{" "}
                  <Link
                    to="/register"
                    className="text-green-600 dark:text-green-400 font-semibold hover:underline"
                  >
                    Create Account
                  </Link>
                </p>
              </div>
            </MagicAuthCard>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="relative z-20 mt-8 w-full">
        <div className="max-w-6xl mx-auto px-6 py-6 flex items-center justify-between text-sm text-gray-300">
          <div>©️ CropEye 🌾 2025</div>
          <div>Developed by Akshi — Intelligent farming experiments</div>
        </div>
      </footer>
    </div>
  );
};

export default LoginPage;
