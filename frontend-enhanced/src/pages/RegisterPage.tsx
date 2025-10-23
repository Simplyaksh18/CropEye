// src/pages/RegisterPage.tsx
// Enhanced Register Page with Agriculture Theme

import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { Mail, Lock, MapPin, UserPlus, Leaf, Building2 } from "lucide-react";
import { useAuth } from "../context/AuthContext";
import { MagicAuthCard } from "../components/ui/MagicAuthCard";
import { AgricultureFacts } from "../components/ui/AgricultureFacts";
import logo from "../assets/cropeye-logo.svg";
import { LiquidChrome } from "../components/animations/LiquidChrome";

const RegisterPage: React.FC = () => {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
    confirmPassword: "",
    firstName: "",
    lastName: "",
    farmName: "",
    location: "",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  // Demo registration info (dev only)
  const DEMO_REG = {
    email: "demo+signup@cropeye.test",
    password: "demo1234",
    confirmPassword: "demo1234",
    firstName: "Demo",
    lastName: "Farmer",
    farmName: "Demo Farm",
    location: "Demoville",
  };

  const { register } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (formData.password !== formData.confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    if (formData.password.length < 6) {
      setError("Password must be at least 6 characters");
      return;
    }

    setLoading(true);
    const result = await register(formData);

    if (result.success) {
      navigate("/");
    } else {
      setError(result.error || "Registration failed");
    }

    setLoading(false);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  return (
    <div className="relative min-h-screen bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50 dark:from-gray-900 dark:via-green-900/20 dark:to-gray-900">
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
            {/* subtle overlay to improve contrast */}
            <div className="absolute inset-0 bg-black/10 dark:bg-black/20 rounded-xl pointer-events-none -z-10" />
            <AgricultureFacts />
            <div className="grid grid-cols-2 gap-4 mt-4">
              <div className="bg-white/5 p-4 rounded-xl">
                <h4 className="text-white font-semibold">NDVI Insights</h4>
                <p className="text-sm text-gray-200/80">
                  Quick NDVI snapshots for your fields.
                </p>
              </div>
              <div className="bg-white/5 p-4 rounded-xl">
                <h4 className="text-white font-semibold">Crop Planner</h4>
                <p className="text-sm text-gray-200/80">
                  Sowing recommendations and timelines.
                </p>
              </div>
            </div>
          </div>

          {/* Right Side - Register Card */}
          <div className="flex items-start justify-center">
            <MagicAuthCard className="w-full max-w-lg mx-auto">
              {/* Logo */}
              <div className="flex justify-center mb-6">
                <div className="relative">
                  <div className="w-20 h-20 rounded-full overflow-hidden border-4 border-green-500 shadow-lg">
                    <img
                      src={logo}
                      alt="CropEye Logo"
                      className="w-full h-full object-cover"
                    />
                  </div>
                  <div className="absolute -bottom-2 -right-2 w-8 h-8 bg-green-500 rounded-full flex items-center justify-center shadow-lg">
                    <Leaf className="w-5 h-5 text-white" />
                  </div>
                </div>
              </div>

              {/* Title */}
              <div className="text-center mb-6">
                <h1 className="text-3xl font-bold text-gray-800 dark:text-white mb-2">
                  Join CropEye
                </h1>
                <p className="text-gray-600 dark:text-gray-400 text-sm">
                  Create your account to start smart farming
                </p>
              </div>

              {/* Demo credentials (dev) */}
              <div className="mb-3 text-sm text-gray-700 dark:text-gray-300">
                <div className="flex items-center justify-between bg-white/5 dark:bg-gray-800/60 rounded-md p-3 border border-gray-800">
                  <div>
                    <div className="font-semibold">Demo signup</div>
                    <div className="text-xs text-gray-300 mt-1">
                      <span className="font-mono">{DEMO_REG.email}</span>
                      <span className="mx-2">/</span>
                      <span className="font-mono">{DEMO_REG.password}</span>
                    </div>
                  </div>
                  <div>
                    <button
                      type="button"
                      onClick={() => setFormData({ ...DEMO_REG })}
                      className="px-3 py-1 text-sm bg-green-500 text-white rounded-md hover:bg-green-600"
                    >
                      Use demo
                    </button>
                  </div>
                </div>
              </div>

              {/* Error Message */}
              {error && (
                <div className="mb-4 p-3 bg-red-50 dark:bg-red-900/20 border-l-4 border-red-500 rounded-r-lg">
                  <p className="text-sm text-red-700 dark:text-red-300">
                    {error}
                  </p>
                </div>
              )}

              {/* Form */}
              <form onSubmit={handleSubmit} className="space-y-4">
                {/* Name Fields */}
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-medium text-gray-700 dark:text-gray-300 mb-1">
                      First Name *
                    </label>
                    <input
                      type="text"
                      name="firstName"
                      value={formData.firstName}
                      onChange={handleChange}
                      required
                      className="w-full px-3 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
                      placeholder="John"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Last Name *
                    </label>
                    <input
                      type="text"
                      name="lastName"
                      value={formData.lastName}
                      onChange={handleChange}
                      required
                      className="w-full px-3 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
                      placeholder="Doe"
                    />
                  </div>
                </div>

                {/* Email */}
                <div>
                  <label className="block text-xs font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Email Address *
                  </label>
                  <div className="relative">
                    <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                    <input
                      type="email"
                      name="email"
                      value={formData.email}
                      onChange={handleChange}
                      required
                      className="w-full pl-10 pr-3 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
                      placeholder="farmer@example.com"
                    />
                  </div>
                </div>

                {/* Farm Details */}
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-medium text-gray-700 dark:text-gray-300 mb-1">
                      <Building2 className="inline w-3 h-3 mr-1" />
                      Farm Name
                    </label>
                    <input
                      type="text"
                      name="farmName"
                      value={formData.farmName}
                      onChange={handleChange}
                      className="w-full px-3 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
                      placeholder="Green Acres"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-medium text-gray-700 dark:text-gray-300 mb-1">
                      <MapPin className="inline w-3 h-3 mr-1" />
                      Location
                    </label>
                    <input
                      type="text"
                      name="location"
                      value={formData.location}
                      onChange={handleChange}
                      className="w-full px-3 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
                      placeholder="Punjab, India"
                    />
                  </div>
                </div>

                {/* Password Fields */}
                <div>
                  <label className="block text-xs font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Password *
                  </label>
                  <div className="relative">
                    <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                    <input
                      type="password"
                      name="password"
                      value={formData.password}
                      onChange={handleChange}
                      required
                      className="w-full pl-10 pr-3 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
                      placeholder="••••••••"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Confirm Password *
                  </label>
                  <div className="relative">
                    <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                    <input
                      type="password"
                      name="confirmPassword"
                      value={formData.confirmPassword}
                      onChange={handleChange}
                      required
                      className="w-full pl-10 pr-3 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
                      placeholder="••••••••"
                    />
                  </div>
                </div>

                {/* Terms */}
                <div className="flex items-start">
                  <input
                    type="checkbox"
                    required
                    className="mt-1 w-4 h-4 text-green-600 border-gray-300 rounded focus:ring-green-500"
                  />
                  <label className="ml-2 text-xs text-gray-700 dark:text-gray-300">
                    I agree to the{" "}
                    <a href="#" className="text-green-600 hover:underline">
                      Terms of Service
                    </a>{" "}
                    and{" "}
                    <a href="#" className="text-green-600 hover:underline">
                      Privacy Policy
                    </a>
                  </label>
                </div>

                {/* Submit Button */}
                <button
                  type="submit"
                  disabled={loading}
                  className="w-full py-3 bg-gradient-to-r from-green-500 to-emerald-600 text-white rounded-lg font-semibold flex items-center justify-center gap-2 hover:from-green-600 hover:to-emerald-700 transition-all transform hover:scale-[1.02] active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed shadow-lg mt-6"
                >
                  {loading ? (
                    <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  ) : (
                    <>
                      <UserPlus className="w-5 h-5" />
                      Create Account
                    </>
                  )}
                </button>
              </form>

              {/* Login Link */}
              <div className="mt-6 text-center">
                <p className="text-gray-600 dark:text-gray-400 text-sm">
                  Already have an account?{" "}
                  <Link
                    to="/login"
                    className="text-green-600 dark:text-green-400 font-semibold hover:underline"
                  >
                    Sign In
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

export default RegisterPage;
