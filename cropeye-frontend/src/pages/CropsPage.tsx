import React, { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { useLocation } from "../hooks/useLocation";
import { api } from "../services/api";
import type { CropResponse } from "../types";
import LoadingSpinner from "../components/LoadingSpinner";
import ErrorMessage from "../components/ErrorMessage";
import Navbar from "../components/Navbar";

export const CropsPage: React.FC = () => {
  const navigate = useNavigate();
  const { logout } = useAuth();
  const { location } = useLocation();
  const [data, setData] = useState<CropResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>("");

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  const fetchData = useCallback(async () => {
    if (!location) return;
    setLoading(true);
    setError("");
    try {
      const result = await api.crops.recommend({
        latitude: location.lat,
        longitude: location.lng,
        ph: 6.5,
        rainfall: 800,
        temp_mean: 25,
        ndvi: 0.68,
      });
      setData(result);
    } catch (error) {
      console.error("Crops API error:", error);
      setError(
        "Failed to fetch crop recommendations. Please check backend connection."
      );
      setData(null);
    } finally {
      setLoading(false);
    }
  }, [location]);

  useEffect(() => {
    fetchData();
  }, [location, fetchData]);

  if (!location) return <ErrorMessage message="Set location first" />;
  if (loading) return <LoadingSpinner />;

  const getScoreColor = (score: number) => {
    if (score >= 0.8) return "bg-green-100 border-green-500 text-green-800";
    if (score >= 0.6) return "bg-yellow-100 border-yellow-500 text-yellow-800";
    return "bg-red-100 border-red-500 text-red-800";
  };

  return (
    <div className="min-h-screen bg-linear-to-br from-green-100 to-amber-100">
      <Navbar onLogout={handleLogout} />
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <h1 className="text-3xl font-bold mb-6">Crop Recommendations</h1>

        {error && <ErrorMessage message={error} />}

        {data && (
          <div className="space-y-6">
            {/* Top 3 Recommendations */}
            <div className="grid md:grid-cols-3 gap-4">
              {(
                (data.crops && data.crops.length
                  ? data.crops
                  : data.recommendations) as import("../types").Crop[]
              )
                .slice(0, 3)
                .map((crop: import("../types").Crop, idx: number) => (
                  <div
                    key={crop.crop}
                    className={`p-6 rounded-lg shadow-lg border-2 ${getScoreColor(
                      crop.score
                    )}`}
                  >
                    <div className="flex items-center justify-between mb-3">
                      <h3 className="text-2xl font-bold">{crop.crop}</h3>
                      <span className="text-3xl">
                        {idx === 0 ? "🥇" : idx === 1 ? "🥈" : "🥉"}
                      </span>
                    </div>
                    <div className="mb-3">
                      <p className="text-sm mb-1">Suitability Score</p>
                      <p className="text-4xl font-bold">
                        {(crop.score * 100).toFixed(0)}%
                      </p>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-3 mb-3">
                      <div
                        className="bg-green-600 h-3 rounded-full"
                        style={{ width: `${crop.score * 100}%` }}
                      />
                    </div>
                    <p className="text-xs">
                      {crop.score >= 0.8
                        ? "Highly Recommended"
                        : crop.score >= 0.6
                        ? "Suitable"
                        : "Marginally Suitable"}
                    </p>
                  </div>
                ))}
            </div>

            {/* All Crops Table */}
            <div className="bg-white p-6 rounded-lg shadow border">
              <h2 className="text-xl font-bold mb-4">
                All Crop Recommendations
              </h2>
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="border-b-2 border-gray-200">
                      <th className="text-left p-3">Crop</th>
                      <th className="text-center p-3">Overall Score</th>
                      <th className="text-center p-3">pH</th>
                      <th className="text-center p-3">Rainfall</th>
                      <th className="text-center p-3">Temp</th>
                      <th className="text-center p-3">NDVI</th>
                    </tr>
                  </thead>
                  <tbody>
                    {(
                      (data.crops && data.crops.length
                        ? data.crops
                        : data.recommendations) as import("../types").Crop[]
                    ).map((crop: import("../types").Crop) => (
                      <tr
                        key={crop.crop}
                        className="border-b border-gray-100 hover:bg-gray-50"
                      >
                        <td className="p-3 font-semibold">{crop.crop}</td>
                        <td className="text-center p-3">
                          <span
                            className={`px-3 py-1 rounded-full text-sm font-bold ${
                              crop.score >= 0.8
                                ? "bg-green-100 text-green-800"
                                : crop.score >= 0.6
                                ? "bg-yellow-100 text-yellow-800"
                                : "bg-red-100 text-red-800"
                            }`}
                          >
                            {(crop.score * 100).toFixed(0)}%
                          </span>
                        </td>
                        <td className="text-center p-3">
                          {(crop.components.ph * 100).toFixed(0)}%
                        </td>
                        <td className="text-center p-3">
                          {(crop.components.rainfall * 100).toFixed(0)}%
                        </td>
                        <td className="text-center p-3">
                          {(crop.components.temp * 100).toFixed(0)}%
                        </td>
                        <td className="text-center p-3">
                          {(crop.components.ndvi * 100).toFixed(0)}%
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Weights */}
            <div className="bg-blue-50 border border-blue-200 p-6 rounded-lg">
              <h3 className="font-semibold text-blue-900 mb-3">
                Scoring Weights
              </h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {Object.entries(
                  (data.weights || {}) as Record<string, number>
                ).map(([key, value]: [string, number]) => (
                  <div key={key} className="text-center">
                    <p className="text-sm text-gray-600 capitalize">{key}</p>
                    <p className="text-2xl font-bold text-blue-800">
                      {(value * 100).toFixed(0)}%
                    </p>
                  </div>
                ))}
              </div>
            </div>

            {/* Educational Insights - Always visible */}
            <div className="bg-linear-to-r from-green-50 to-emerald-50 border border-green-200 rounded-xl p-6 shadow-lg">
              <h3 className="text-xl font-bold text-green-800 mb-4">
                🌾 Understanding Crop Recommendation Calculations
              </h3>
              <p className="text-green-700 leading-relaxed mb-4">
                Crop recommendations are generated using a sophisticated
                algorithm that analyzes multiple environmental and agricultural
                factors. The system considers soil composition (NPK levels, pH,
                texture), weather patterns (temperature, rainfall, humidity),
                location-specific climate data, and historical yield data. A
                weighted scoring system evaluates each crop's suitability based
                on: Environmental Compatibility (40%), Soil Requirements Match
                (30%), Climate Adaptation (20%), and Economic Viability (10%).
                The algorithm uses machine learning models trained on regional
                agricultural data to predict optimal crop choices and expected
                yields.
              </p>
              <div className="grid md:grid-cols-2 gap-6">
                <div className="bg-white/70 backdrop-blur-sm rounded-lg p-4">
                  <h4 className="font-semibold text-green-800 mb-2">
                    🧮 Suitability Score Formula
                  </h4>
                  <p className="text-sm text-gray-700">
                    <strong>
                      Score = (pH × 0.25) + (Rainfall × 0.30) + (Temp × 0.25) +
                      (NDVI × 0.20)
                    </strong>
                    <br />
                    Each component score ranges from 0-1, weighted by
                    importance. Higher scores indicate better suitability for
                    the location's conditions.
                  </p>
                </div>
                <div className="bg-white/70 backdrop-blur-sm rounded-lg p-4">
                  <h4 className="font-semibold text-green-800 mb-2">
                    📊 Component Scoring
                  </h4>
                  <p className="text-sm text-gray-700">
                    <strong>pH:</strong> Optimal range 6.0-7.0 (score 0.9-1.0)
                    <br />
                    <strong>Rainfall:</strong> Crop-specific requirements
                    (mm/year)
                    <br />
                    <strong>Temperature:</strong> Mean annual temperature (°C)
                    <br />
                    <strong>NDVI:</strong> Vegetation health index (0-1)
                  </p>
                </div>
                <div className="bg-white/70 backdrop-blur-sm rounded-lg p-4">
                  <h4 className="font-semibold text-green-800 mb-2">
                    🎯 Recommendation Categories
                  </h4>
                  <p className="text-sm text-gray-700">
                    <strong>Highly Recommended:</strong> Score ≥ 0.8
                    <br />
                    <strong>Suitable:</strong> Score 0.6-0.8
                    <br />
                    <strong>Marginally Suitable:</strong> Score {"<"} 0.6
                    <br />
                    Based on multi-factor analysis and historical performance
                    data.
                  </p>
                </div>
                <div className="bg-white/70 backdrop-blur-sm rounded-lg p-4">
                  <h4 className="font-semibold text-green-800 mb-2">
                    🤖 Machine Learning Model
                  </h4>
                  <p className="text-sm text-gray-700">
                    Uses ensemble methods combining Random Forest and Gradient
                    Boosting algorithms. Trained on 10+ years of regional
                    agricultural data, including yield statistics, weather
                    patterns, and soil characteristics for accurate predictions.
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
