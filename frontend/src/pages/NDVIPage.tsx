// src/pages/NDVIPage.tsx
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { useLocation } from "../hooks/useLocation";
import api from "../services/api";
import LoadingSpinner from "../components/LoadingSpinner";
import ErrorMessage from "../components/ErrorMessage";
import Navbar from "../components/Navbar";

export default function NDVIPage() {
  const navigate = useNavigate();
  const { logout } = useAuth();
  const { location } = useLocation();

  interface NdviData {
    ndvi: number;
    red_band?: number;
    nir_band?: number;
    health_category?: string;
    health_score?: number;
    description?: string;
    acquisition_date?: string;
  }

  interface NdviMetadata {
    data_source?: string;
    is_real_data?: boolean;
    date?: string;
    latitude?: number;
    longitude?: number;
  }

  const [ndviData, setNdviData] = useState<NdviData | null>(null);
  const [ndviMeta, setNdviMeta] = useState<NdviMetadata | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>("");

  useEffect(() => {
    const fetchNDVI = async () => {
      if (!location.lat || !location.lng) return;

      setLoading(true);
      setError("");

      try {
        const res = await api.ndvi.analyze(location.lat, location.lng);
        setNdviData(res.data);
        setNdviMeta(res.metadata ?? null);
      } catch {
        setError("Failed to fetch NDVI vegetation health data.");
      } finally {
        setLoading(false);
      }
    };

    fetchNDVI();
  }, [location.lat, location.lng]);

  const getScoreLabel = (value: number) => {
    if (value >= 0.6) return { label: "High", color: "text-green-600" };
    if (value >= 0.3) return { label: "Medium", color: "text-yellow-600" };
    return { label: "Low", color: "text-red-600" };
  };

  const ndviValue = ndviData?.ndvi ?? null;
  const score = ndviValue !== null ? getScoreLabel(ndviValue) : null;
  const fillPercent = ndviValue ? ndviValue * 100 : 0;

  const getRecommendation = (value: number) => {
    if (value >= 0.6)
      return "Crop is healthy. Continue current management practices.";
    if (value >= 0.4)
      return "Moderate stress detected. Consider increasing irrigation and nutrient application.";
    return "Significant stress detected. Immediate intervention required - check irrigation, nutrients, and pest pressure.";
  };

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  return (
    <div className="min-h-screen bg-linear-to-br from-green-50 to-amber-50 text-gray-900">
      <Navbar onLogout={handleLogout} />

      <main className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <h1 className="text-3xl font-bold text-green-700 mb-3">
          🌱 NDVI Vegetation Health
        </h1>
        <p className="text-gray-600 mb-6">
          Satellite-based crop canopy health analysis.
        </p>

        {loading && <LoadingSpinner message="Fetching NDVI data..." />}
        {error && <ErrorMessage message={error} />}

        {!loading && !error && ndviValue !== null && (
          <div className="space-y-6">
            {/* Main NDVI Card */}
            <div className="bg-white shadow-lg rounded-xl p-8 border border-gray-200">
              <h2 className="text-xl font-semibold text-gray-800 mb-6">
                Current NDVI Value
              </h2>

              <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 items-center">
                {/* NDVI Value Display */}
                <div className="text-center lg:text-left">
                  <div className="text-6xl font-bold text-gray-900 mb-2">
                    {ndviValue.toFixed(3)}
                  </div>
                  <div className="text-lg text-gray-700">
                    Status:{" "}
                    <span className={`font-semibold ${score?.color}`}>
                      {score?.label}
                    </span>
                  </div>
                  <p className="text-xs text-gray-500 mt-2">
                    Source:{" "}
                    {ndviMeta?.is_real_data
                      ? "Copernicus API"
                      : "Synthetic Fallback"}
                  </p>
                </div>

                {/* NDVI Bar */}
                <div className="lg:col-span-2 space-y-3">
                  <div className="relative group">
                    <div className="h-8 rounded-full bg-linear-to-r from-red-600 via-amber-500 to-emerald-700 shadow-inner relative overflow-visible">
                      <div
                        className="absolute top-1/2 w-5 h-5 bg-white border-2 border-gray-400 rounded-full shadow-lg cursor-pointer transition-transform hover:scale-125"
                        style={{
                          left: `${Math.min(Math.max(fillPercent, 0), 100)}%`,
                          transform: "translate(-50%, -50%)",
                        }}
                        title={`NDVI: ${ndviValue.toFixed(3)}`}
                      >
                        {/* Tooltip on hover */}
                        <div className="absolute bottom-full mb-2 left-1/2 -translate-x-1/2 bg-gray-900 text-white text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none">
                          {ndviValue.toFixed(3)}
                        </div>
                      </div>
                    </div>
                  </div>
                  <div className="flex justify-between text-sm text-gray-600 px-1">
                    <span>-1.0 (Low)</span>
                    <span className="text-xs text-gray-400">0.0</span>
                    <span>+1.0 (High)</span>
                  </div>

                  {/* Health Indicator */}
                  <div className="flex items-center justify-center gap-3 pt-2">
                    <div className="text-3xl">
                      {ndviValue >= 0.6 ? "✅" : ndviValue >= 0.4 ? "⚠️" : "🚨"}
                    </div>
                    <p className="text-sm text-gray-600">Health Indicator</p>
                  </div>
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
                  {(ndviValue * 100).toFixed(1)}%
                </p>
                <div className="mt-3 bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-green-600 h-2 rounded-full"
                    style={{ width: `${Math.min(ndviValue * 100, 100)}%` }}
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
                  Recommendations
                </h3>
                <p className="text-sm text-gray-800 leading-relaxed">
                  {getRecommendation(ndviValue)}
                </p>
              </div>
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

            {/* Insights */}
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

        {!loading && !ndviValue && (
          <p className="text-gray-500 mt-4">
            Set a location on the dashboard to begin.
          </p>
        )}
      </main>
    </div>
  );
}
