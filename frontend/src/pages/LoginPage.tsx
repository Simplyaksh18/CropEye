// src/pages/LoginPage.tsx

import React, { useState } from "react";
import { useAuth } from "../hooks/useAuth";

interface LoginPageProps {
  onLoginSuccess: () => void;
}

export const LoginPage: React.FC<LoginPageProps> = ({ onLoginSuccess }) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();

  const validateEmail = (email: string) => {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (!email || !password) {
      setError("Please fill in all fields");
      return;
    }

    if (!validateEmail(email)) {
      setError("Please enter a valid email address");
      return;
    }

    if (password.length < 6) {
      setError("Password must be at least 6 characters");
      return;
    }

    setLoading(true);

    try {
      await login(email, password);
      onLoginSuccess();
    } catch {
      setError("Login failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-linear-to-br from-green-900 via-green-800 to-gray-900 flex items-center justify-center p-4">
      <div className="bg-white p-8 rounded-2xl shadow-2xl w-full max-w-md">
        {/* Logo and Header */}
        <div className="text-center mb-8">
          <div className="w-20 h-20 bg-linear-to-br from-green-500 to-green-600 rounded-full mx-auto mb-4 flex items-center justify-center text-3xl">
            🌿
          </div>
          <h1 className="text-3xl font-bold text-gray-900">CropEye</h1>
          <p className="text-gray-600 mt-2">
            Agriculture Intelligence Platform
          </p>
        </div>

        {/* Login Form */}
        <form onSubmit={handleSubmit} className="space-y-5">
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
              {error}
            </div>
          )}

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Email Address
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none transition"
              placeholder="your@email.com"
              disabled={loading}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Password
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none transition"
              placeholder="••••••••"
              disabled={loading}
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-green-600 text-white py-3 rounded-lg hover:bg-green-700 font-medium transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            {loading ? "Logging in..." : "Login"}
          </button>
        </form>

        {/* Demo Notice */}
        <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
          <p className="text-center text-sm text-blue-800">
            <strong>Demo Mode:</strong> Use any email and password (6+ chars) to
            login
          </p>
        </div>

        {/* Features */}
        <div className="mt-6 pt-6 border-t border-gray-200">
          <p className="text-xs text-gray-500 text-center mb-3">
            Platform Features
          </p>
          <div className="grid grid-cols-2 gap-2 text-xs text-gray-600">
            <div className="flex items-center">
              <span className="mr-1">🌱</span> NDVI Analysis
            </div>
            <div className="flex items-center">
              <span className="mr-1">🌤️</span> Weather Forecast
            </div>
            <div className="flex items-center">
              <span className="mr-1">💧</span> Water Management
            </div>
            <div className="flex items-center">
              <span className="mr-1">🏞️</span> Soil Analysis
            </div>
            <div className="flex items-center">
              <span className="mr-1">🌾</span> Crop Recommendations
            </div>
            <div className="flex items-center">
              <span className="mr-1">🐛</span> Pest Detection
            </div>
          </div>
        </div>

        {/* Did You Know Facts */}
        <div className="mt-6 bg-green-50 border border-green-200 rounded-lg p-4">
          <h3 className="text-sm font-semibold text-green-800 mb-2 flex items-center">
            <span className="mr-2">💡</span> Did You Know?
          </h3>
          <div className="text-xs text-green-700 space-y-2">
            <p>
              • Precision agriculture can increase crop yields by up to 20%
              while reducing resource use.
            </p>
            <p>
              • Satellite imagery enables monitoring of thousands of acres in
              real-time.
            </p>
            <p>
              • AI-powered crop recommendations consider 15+ environmental
              factors for optimal results.
            </p>
            <p>
              • Early pest detection can prevent up to 30% of potential crop
              losses.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
