import React, { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { useLocation } from "../hooks/useLocation";
import { api } from "../services/api";
import type { SoilResponse } from "../types";
import LoadingSpinner from "../components/LoadingSpinner";
import ErrorMessage from "../components/ErrorMessage";
import Navbar from "../components/Navbar";

export const SoilPage: React.FC = () => {
  const navigate = useNavigate();
  const { logout } = useAuth();
  const { location } = useLocation();
  const [data, setData] = useState<SoilResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  const fetchData = useCallback(async () => {
    if (!location) return;
    setLoading(true);
    setError("");
    try {
      const result = await api.soil.analyze(location.lat, location.lng);
      setData(result);
    } catch (error) {
      console.error("Soil API error:", error);
      setError("Failed to fetch soil data. Please check backend connection.");
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

  const getNutrientStatus = (value: number, type: string) => {
    const thresholds = {
      nitrogen: { low: 100, high: 200 },
      phosphorus: { low: 30, high: 60 },
      potassium: { low: 150, high: 250 },
    };
    const t = thresholds[type as keyof typeof thresholds];
    if (value < t.low) return { status: "Low", color: "red" };
    if (value > t.high) return { status: "High", color: "blue" };
    return { status: "Optimal", color: "green" };
  };

  return (
    <div className="min-h-screen bg-linear-to-br from-green-100 to-amber-100">
      <Navbar onLogout={handleLogout} />
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <h1 className="text-3xl font-bold mb-6">Soil Analysis</h1>

        {error && <ErrorMessage message={error} />}

        {data && (
          <div className="space-y-6">
            {/* pH */}
            <div className="bg-white p-6 rounded-lg shadow border">
              <h2 className="text-lg font-semibold mb-4">Soil pH</h2>
              <p className="text-4xl font-bold text-purple-600">
                {data.ph.toFixed(1)}
              </p>
              <p className="text-sm text-gray-600 mt-2">
                {data.ph < 6
                  ? "Acidic"
                  : data.ph > 7.5
                  ? "Alkaline"
                  : "Neutral (Ideal)"}
              </p>
            </div>

            {/* NPK Levels */}
            <div className="grid md:grid-cols-3 gap-4">
              {[
                {
                  label: "Nitrogen (N)",
                  value: data.nitrogen,
                  type: "nitrogen",
                },
                {
                  label: "Phosphorus (P)",
                  value: data.phosphorus,
                  type: "phosphorus",
                },
                {
                  label: "Potassium (K)",
                  value: data.potassium,
                  type: "potassium",
                },
              ].map((nutrient) => {
                const status = getNutrientStatus(nutrient.value, nutrient.type);
                return (
                  <div
                    key={nutrient.type}
                    className="bg-white p-6 rounded-lg shadow border"
                  >
                    <h3 className="text-sm text-gray-600 mb-2">
                      {nutrient.label}
                    </h3>
                    <p
                      className={`text-3xl font-bold text-${status.color}-600`}
                    >
                      {nutrient.value}
                    </p>
                    <p className="text-sm text-gray-600 mt-1">mg/kg</p>
                    <p
                      className={`text-sm font-medium text-${status.color}-600 mt-2`}
                    >
                      {status.status}
                    </p>
                  </div>
                );
              })}
            </div>

            {/* Texture & Confidence */}
            <div className="grid md:grid-cols-2 gap-4">
              <div className="bg-white p-6 rounded-lg shadow border">
                <h3 className="text-sm text-gray-600 mb-2">Soil Texture</h3>
                <p className="text-2xl font-bold text-gray-800">
                  {data.texture}
                </p>
              </div>
              <div className="bg-white p-6 rounded-lg shadow border">
                <h3 className="text-sm text-gray-600 mb-2">Data Confidence</h3>
                <p className="text-2xl font-bold text-green-600">
                  {(data.confidence * 100).toFixed(0)}%
                </p>
                <p className="text-xs text-gray-500 mt-1">
                  Source: {data.data_source}
                </p>
              </div>
            </div>

            {/* Recommendations */}
            <div className="bg-blue-50 border border-blue-200 p-6 rounded-lg">
              <h3 className="font-semibold text-blue-900 mb-3">
                Recommendations
              </h3>
              <ul className="space-y-2">
                {data.recommendations.map((rec, idx) => (
                  <li key={idx} className="flex items-start text-blue-800">
                    <span className="mr-2">✓</span>
                    <span>{rec}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Educational Insights - Always visible */}
            <div className="bg-linear-to-r from-amber-50 to-orange-50 border border-amber-200 rounded-xl p-6 shadow-lg">
              <h3 className="text-xl font-bold text-amber-800 mb-4">
                🌱 Understanding Soil Analysis Calculations
              </h3>
              <p className="text-amber-700 leading-relaxed mb-4">
                Our soil analysis system employs advanced spectroscopic
                techniques and machine learning algorithms to provide
                comprehensive nutrient profiling. The pH measurement uses
                electrochemical sensors calibrated against standard buffers,
                while NPK analysis combines chemical extraction methods with
                optical spectroscopy for precise quantification. Soil texture
                classification integrates particle size distribution data with
                pedological databases, enabling accurate water retention and
                drainage predictions. This detailed analysis supports precision
                fertilization strategies that optimize crop nutrition while
                minimizing environmental impact.
              </p>
              <div className="grid md:grid-cols-2 gap-6">
                <div className="bg-white/70 backdrop-blur-sm rounded-lg p-4">
                  <h4 className="font-semibold text-amber-800 mb-2">
                    🧪 pH Measurement
                  </h4>
                  <p className="text-sm text-gray-700">
                    <strong>pH = -log[H⁺]</strong>
                    <br />
                    Measured using calibrated electrodes in soil-water slurry
                    (1:2.5 ratio). Values 6.0-7.0 are optimal for most crops,
                    affecting nutrient availability and microbial activity.
                  </p>
                </div>
                <div className="bg-white/70 backdrop-blur-sm rounded-lg p-4">
                  <h4 className="font-semibold text-amber-800 mb-2">
                    🧪 NPK Analysis
                  </h4>
                  <p className="text-sm text-gray-700">
                    <strong>Nitrogen:</strong> Kjeldahl digestion method
                    <br />
                    <strong>Phosphorus:</strong> Olsen extraction (NaHCO₃)
                    <br />
                    <strong>Potassium:</strong> Ammonium acetate extraction
                    <br />
                    Results expressed in mg/kg soil.
                  </p>
                </div>
                <div className="bg-white/70 backdrop-blur-sm rounded-lg p-4">
                  <h4 className="font-semibold text-amber-800 mb-2">
                    🏞️ Soil Texture
                  </h4>
                  <p className="text-sm text-gray-700">
                    Determined by hydrometer method measuring particle size
                    distribution: Sand (2.0-0.05mm), Silt (0.05-0.002mm), Clay (
                    {"<"}0.002mm). Texture affects water holding capacity and
                    nutrient retention.
                  </p>
                </div>
                <div className="bg-white/70 backdrop-blur-sm rounded-lg p-4">
                  <h4 className="font-semibold text-amber-800 mb-2">
                    📊 Nutrient Status
                  </h4>
                  <p className="text-sm text-gray-700">
                    <strong>Low:</strong> Below critical levels requiring
                    immediate fertilization
                    <br />
                    <strong>Optimal:</strong> Within recommended ranges for
                    maximum yield
                    <br />
                    <strong>High:</strong> Excess levels that may cause
                    environmental issues
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
