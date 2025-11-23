// src/pages/NDVIPage.tsx

import React, { useState, useEffect, useCallback } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { useLocation } from "../hooks/useLocation";
import { api } from "../services/api";
import type { NDVIResponse } from "../types";
import LoadingSpinner from "../components/LoadingSpinner";
import ErrorMessage from "../components/ErrorMessage";
import Navbar from "../components/Navbar";

export const NDVIPage: React.FC = () => {
  const navigate = useNavigate();
  const { logout } = useAuth();
  const { location } = useLocation();
  const [data, setData] = useState<NDVIResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [, setError] = useState("");

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  const fetchData = useCallback(async () => {
    if (!location) {
      setError("Please set a location first");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const result = await api.ndvi.analyze(location.lat, location.lng);
      setData(result);
    } catch (error) {
      console.error("NDVI API error:", error);
      setError("Failed to fetch NDVI data. Please check backend connection.");
      // Remove mock data fallback - show error instead
      setData(null);
    } finally {
      setLoading(false);
    }
  }, [location]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const getHealthColor = (ndvi: number) => {
    if (ndvi >= 0.6) return "text-green-600";
    if (ndvi >= 0.4) return "text-yellow-600";
    return "text-red-600";
  };

  const getHealthBgColor = (ndvi: number) => {
    if (ndvi >= 0.6) return "bg-green-100 border-green-300";
    if (ndvi >= 0.4) return "bg-yellow-100 border-yellow-300";
    return "bg-red-100 border-red-300";
  };

  const getRecommendation = (ndvi: number) => {
    if (ndvi >= 0.6)
      return "Crop is healthy. Continue current management practices.";
    if (ndvi >= 0.4)
      return "Moderate stress detected. Consider increasing irrigation and nutrient application.";
    return "Significant stress detected. Immediate intervention required - check irrigation, nutrients, and pest pressure.";
  };

  if (!location) {
    return (
      <div className="min-h-screen bg-linear-to-br from-green-100 to-amber-100 p-6">
        <div className="max-w-4xl mx-auto">
          <ErrorMessage message="Please set a location from the dashboard to view NDVI data" />
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-linear-to-br from-green-100 to-amber-100 p-6">
        <LoadingSpinner message="Fetching NDVI data..." />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-linear-to-br from-green-100 to-amber-100">
      <Navbar onLogout={handleLogout} />
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            NDVI Analysis
          </h1>
          <p className="text-gray-600">
            Normalized Difference Vegetation Index - Crop Health Monitoring
          </p>
        </div>

        {/* Error display removed since error is not used */}

        {data && (
          <div className="space-y-6">
            {/* Main NDVI Card */}
            <div
              className={`p-6 rounded-xl shadow-lg border-2 ${getHealthBgColor(
                data.ndvi_value
              )}`}
            >
              <div className="flex flex-col md:flex-row md:items-center md:justify-between">
                <div>
                  <h2 className="text-xl font-semibold text-gray-800 mb-1">
                    Current NDVI Value
                  </h2>
                  <p
                    className={`text-6xl font-bold ${getHealthColor(
                      data.ndvi_value
                    )}`}
                  >
                    {data.ndvi_value.toFixed(3)}
                  </p>
                  <p className="text-lg mt-2 text-gray-700">
                    Status:{" "}
                    <span className="font-semibold">{data.health_status}</span>
                  </p>
                </div>
                <div className="mt-4 md:mt-0 text-center">
                  <div className="text-4xl mb-2">
                    {data.ndvi_value >= 0.6
                      ? "✅"
                      : data.ndvi_value >= 0.4
                      ? "⚠️"
                      : "🚨"}
                  </div>
                  <p className="text-sm text-gray-600">Health Indicator</p>
                </div>
              </div>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-white p-6 rounded-lg shadow border border-gray-200">
                <h3 className="text-gray-600 text-sm font-medium mb-2">
                  Vegetation Coverage
                </h3>
                <p className="text-3xl font-bold text-green-600">
                  {data.vegetation_coverage.toFixed(1)}%
                </p>
                <div className="mt-3 bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-green-600 h-2 rounded-full"
                    style={{ width: `${data.vegetation_coverage}%` }}
                  />
                </div>
              </div>

              <div className="bg-white p-6 rounded-lg shadow border border-gray-200">
                <h3 className="text-gray-600 text-sm font-medium mb-2">
                  NDVI Range
                </h3>
                <p className="text-lg text-gray-800">
                  <span className="font-mono text-2xl font-bold">-1.0</span> to{" "}
                  <span className="font-mono text-2xl font-bold">+1.0</span>
                </p>
                <p className="text-xs text-gray-500 mt-2">
                  Higher values indicate healthier vegetation
                </p>
              </div>

              <div className="bg-white p-6 rounded-lg shadow border border-gray-200">
                <h3 className="text-gray-600 text-sm font-medium mb-2">
                  Last Updated
                </h3>
                <p className="text-sm text-gray-800">
                  {new Date(data.timestamp).toLocaleString()}
                </p>
                <button
                  onClick={fetchData}
                  className="mt-3 text-sm text-blue-600 hover:text-blue-700 font-medium"
                >
                  Refresh Data →
                </button>
              </div>
            </div>

            {/* Trend Chart */}
            <div className="bg-white p-6 rounded-lg shadow border border-gray-200">
              <h2 className="text-xl font-bold text-gray-900 mb-4">
                7-Day NDVI Trend
              </h2>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={data.trend}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis domain={[0, 1]} />
                  <Tooltip />
                  <Line
                    type="monotone"
                    dataKey="value"
                    stroke="#16a34a"
                    strokeWidth={3}
                    dot={{ fill: "#16a34a", r: 4 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>

            {/* Recommendations */}
            <div className="bg-blue-50 border border-blue-200 p-6 rounded-lg">
              <h2 className="text-xl font-bold text-gray-900 mb-3">
                Recommendations
              </h2>
              <p className="text-gray-800 leading-relaxed">
                {getRecommendation(data.ndvi_value)}
              </p>
            </div>

            {/* NDVI Scale Reference */}
            <div className="bg-white p-6 rounded-lg shadow border border-gray-200">
              <h2 className="text-xl font-bold text-gray-900 mb-4">
                NDVI Scale Reference
              </h2>
              <div className="space-y-3">
                <div className="flex items-center">
                  <div className="w-12 h-12 bg-red-500 rounded mr-4"></div>
                  <div>
                    <p className="font-semibold text-gray-900">
                      0.0 - 0.3: Poor/Stressed
                    </p>
                    <p className="text-sm text-gray-600">
                      Bare soil, dead vegetation, or severe stress
                    </p>
                  </div>
                </div>
                <div className="flex items-center">
                  <div className="w-12 h-12 bg-yellow-500 rounded mr-4"></div>
                  <div>
                    <p className="font-semibold text-gray-900">
                      0.3 - 0.6: Moderate
                    </p>
                    <p className="text-sm text-gray-600">
                      Stressed vegetation, sparse coverage
                    </p>
                  </div>
                </div>
                <div className="flex items-center">
                  <div className="w-12 h-12 bg-green-500 rounded mr-4"></div>
                  <div>
                    <p className="font-semibold text-gray-900">
                      0.6 - 1.0: Healthy/Dense
                    </p>
                    <p className="text-sm text-gray-600">
                      Dense, healthy vegetation with good coverage
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* Educational Insights - Always visible */}
            <div className="bg-linear-to-r from-green-50 to-emerald-50 border border-green-200 rounded-xl p-6 shadow-lg">
              <h3 className="text-xl font-bold text-green-800 mb-4">
                🌱 Understanding NDVI Calculations and Applications
              </h3>
              <p className="text-green-700 leading-relaxed mb-4">
                NDVI (Normalized Difference Vegetation Index) is a crucial
                metric in precision agriculture, calculated using satellite
                multispectral imagery to assess vegetation health and density.
              </p>
              <div className="grid md:grid-cols-2 gap-6">
                <div className="bg-white/70 backdrop-blur-sm rounded-lg p-4">
                  <h4 className="font-semibold text-green-800 mb-2">
                    📐 NDVI Formula
                  </h4>
                  <p className="text-sm text-gray-700">
                    <strong>NDVI = (NIR - Red) / (NIR + Red)</strong>
                    <br />
                    Where NIR is near-infrared reflectance (0.7-1.1 μm) and Red
                    is red light reflectance (0.6-0.7 μm). Values range from -1
                    to +1, with higher values indicating healthier, denser
                    vegetation.
                  </p>
                </div>
                <div className="bg-white/70 backdrop-blur-sm rounded-lg p-4">
                  <h4 className="font-semibold text-green-800 mb-2">
                    🛰️ Satellite Data Sources
                  </h4>
                  <p className="text-sm text-gray-700">
                    Utilizes multispectral sensors from satellites like Landsat,
                    Sentinel-2, and MODIS. Near-infrared and red bands are
                    processed to calculate vegetation indices with high spatial
                    resolution.
                  </p>
                </div>
                <div className="bg-white/70 backdrop-blur-sm rounded-lg p-4">
                  <h4 className="font-semibold text-green-800 mb-2">
                    📊 Health Interpretation
                  </h4>
                  <p className="text-sm text-gray-700">
                    NDVI {">"} 0.6: Dense healthy vegetation
                    <br />
                    0.3-0.6: Moderate health/stress
                    <br />
                    {"<"} 0.3: Poor vegetation or bare soil
                    <br />
                    Temporal trends help detect changes in crop health over
                    time.
                  </p>
                </div>
                <div className="bg-white/70 backdrop-blur-sm rounded-lg p-4">
                  <h4 className="font-semibold text-green-800 mb-2">
                    🌾 Agricultural Applications
                  </h4>
                  <p className="text-sm text-gray-700">
                    Used for drought monitoring, yield prediction, irrigation
                    scheduling, and precision agriculture. Helps identify stress
                    areas before visible symptoms appear, enabling proactive
                    management.
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default NDVIPage;
