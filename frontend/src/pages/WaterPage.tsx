import { useEffect, useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { LocationContext } from "../context/LocationContext";
import { useAuth } from "../hooks/useAuth";
import api from "../services/api";
import Navbar from "../components/Navbar";
import LoadingSpinner from "../components/LoadingSpinner";
import ErrorMessage from "../components/ErrorMessage";
import type { Crop } from "../types";

export default function WaterPage() {
  const navigate = useNavigate();
  const { logout } = useAuth();
  const { location } = useContext(LocationContext)!;
  const [cropsData, setCropsData] = useState<Crop[]>([]);
  const [waterAnalysis, setWaterAnalysis] = useState<
    Map<
      string,
      {
        crop_type?: string;
        schedule?: {
          irrigation?: {
            gross_irrigation_mm?: number;
            irrigation_interval_days?: number;
            recommendation?: string;
            net_irrigation_mm?: number;
            effective_rainfall_mm?: number;
          };
        };
        weather_data?: {
          temp_min?: number;
          temp_max?: number;
          rh_mean?: number;
          wind_speed?: number;
          solar_radiation?: number;
        };
        soil_data?: {
          soil_type?: string;
          moisture?: number;
          rainfall?: number;
        };
      }
    >
  >(new Map());
  const [waterData, setWaterData] = useState<{
    crop_type?: string;
    schedule?: {
      irrigation?: {
        gross_irrigation_mm?: number;
        irrigation_interval_days?: number;
        recommendation?: string;
        net_irrigation_mm?: number;
        effective_rainfall_mm?: number;
      };
    };
    weather_data?: {
      temp_min?: number;
      temp_max?: number;
      rh_mean?: number;
      wind_speed?: number;
      solar_radiation?: number;
    };
    soil_data?: {
      soil_type?: string;
      moisture?: number;
      rainfall?: number;
    };
  } | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  // Fetch crop recommendations first
  useEffect(() => {
    const fetchCrops = async () => {
      if (!location?.lat || !location?.lng) return;

      setLoading(true);
      setError("");

      try {
        const cropsRes = await api.crops.recommend(location.lat, location.lng);
        const topCrops = (
          (cropsRes.crops && cropsRes.crops.length
            ? cropsRes.crops
            : cropsRes.recommendations) as Crop[]
        ).slice(0, 3);
        setCropsData(topCrops);
      } catch (err) {
        console.error("Crops API error:", err);
        setError("Failed to fetch crop recommendations.");
      }
    };

    fetchCrops();
  }, [location?.lat, location?.lng]);

  // Fetch irrigation analysis for each recommended crop
  useEffect(() => {
    const fetchWaterAnalysis = async () => {
      if (!location?.lat || !location?.lng || cropsData.length === 0) return;

      setLoading(true);
      setError("");

      try {
        const analysisMap = new Map<
          string,
          {
            crop_type?: string;
            schedule?: {
              irrigation?: {
                gross_irrigation_mm?: number;
                irrigation_interval_days?: number;
                recommendation?: string;
              };
            };
            weather_data?: {
              temp_min?: number;
              temp_max?: number;
              rh_mean?: number;
              wind_speed?: number;
              solar_radiation?: number;
            };
            soil_data?: {
              soil_type?: string;
              moisture?: number;
              rainfall?: number;
            };
          }
        >();

        for (const crop of cropsData) {
          const res = await api.water.calculate(
            location.lat,
            location.lng,
            crop.crop,
            "initial"
          );
          analysisMap.set(crop.crop, res);
        }

        setWaterAnalysis(analysisMap);
        // Set waterData to first crop analysis for detailed view
        const firstCropData = analysisMap.get(cropsData[0].crop);
        if (firstCropData) {
          setWaterData(firstCropData);
        }
      } catch (err) {
        console.error("Water API error:", err);
        setError("Failed to fetch irrigation analysis.");
      } finally {
        setLoading(false);
      }
    };

    if (cropsData.length > 0) {
      fetchWaterAnalysis();
    }
  }, [location?.lat, location?.lng, cropsData]);

  if (!location?.lat || !location?.lng) {
    return <ErrorMessage message="Set location first" />;
  }

  const getIrrigationColor = (index: number) => {
    const colors = [
      "bg-gradient-to-br from-green-100 to-emerald-100 border-green-400",
      "bg-gradient-to-br from-emerald-100 to-cyan-100 border-emerald-400",
      "bg-gradient-to-br from-cyan-100 to-amber-100 border-cyan-400",
    ];
    return colors[index] || colors[0];
  };

  return (
    <div className="min-h-screen bg-linear-to-br from-blue-50 to-cyan-50">
      <Navbar onLogout={handleLogout} />
      <main className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <h1 className="text-3xl font-bold text-blue-700 mb-3">
          💧 Irrigation Recommendations
        </h1>
        <p className="text-gray-600 mb-6">
          Smart water management based on crop type, soil & weather conditions.
        </p>

        {loading && (
          <LoadingSpinner message="💧 Calculating irrigation requirements..." />
        )}
        {error && <ErrorMessage message={error} />}

        {!loading && !error && cropsData.length > 0 && (
          <div className="space-y-8">
            {/* Top 3 Crops with Irrigation Analysis */}
            <div className="grid md:grid-cols-3 gap-6">
              {cropsData.map((crop, idx) => {
                const analysis = waterAnalysis.get(crop.crop);
                return (
                  <div
                    key={crop.crop}
                    className={`rounded-xl shadow-lg p-6 border-2 ${getIrrigationColor(
                      idx
                    )}`}
                  >
                    {/* Header with Crop Name and Rank */}
                    <div className="flex items-center justify-between mb-4">
                      <h2 className="text-2xl font-bold text-gray-800">
                        {crop.crop}
                      </h2>
                      <span className="text-3xl">
                        {idx === 0 ? "🥇" : idx === 1 ? "🥈" : "🥉"}
                      </span>
                    </div>

                    {/* Suitability Score */}
                    <div className="mb-4">
                      <p className="text-sm text-gray-600 mb-1">
                        Suitability Score
                      </p>
                      <p className="text-3xl font-bold text-blue-600">
                        {(crop.score * 100).toFixed(0)}%
                      </p>
                    </div>

                    {/* Irrigation Requirement */}
                    {analysis && (
                      <div className="bg-white/60 backdrop-blur-sm rounded-lg p-4 space-y-3">
                        <div>
                          <p className="text-xs text-gray-600 mb-1">
                            Irrigation Needed
                          </p>
                          <p className="text-2xl font-bold text-blue-700">
                            {analysis.schedule?.irrigation?.gross_irrigation_mm?.toFixed(
                              1
                            ) || 0}
                            <span className="text-sm ml-1">mm</span>
                          </p>
                        </div>

                        <div className="pt-2 border-t border-white/30">
                          <p className="text-xs text-gray-600 mb-1">Interval</p>
                          <p className="text-lg font-semibold text-emerald-700">
                            Every{" "}
                            {analysis.schedule?.irrigation?.irrigation_interval_days?.toFixed(
                              0
                            ) || 0}{" "}
                            days
                          </p>
                        </div>

                        {analysis.schedule?.irrigation?.recommendation && (
                          <div className="pt-2 border-t border-white/30">
                            <p className="text-xs font-semibold text-amber-700">
                              💡 {analysis.schedule.irrigation.recommendation}
                            </p>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>

            {/* Detailed Analysis Section */}
            {cropsData.length > 0 && waterData && (
              <div>
                <h3 className="text-2xl font-bold text-gray-800 mb-6">
                  📊 Detailed Analysis: {cropsData[0].crop}
                </h3>
                {/* Main Irrigation Recommendation */}
                <div className="bg-white shadow-lg rounded-xl p-6">
                  <h2 className="text-blue-700 text-xl font-semibold mb-4">
                    🌾 Crop: {waterData?.crop_type || "Wheat"}
                  </h2>
                  <div className="grid md:grid-cols-2 gap-6">
                    {/* Irrigation Amount */}
                    <div className="bg-blue-50 p-6 rounded-lg border border-blue-200">
                      <p className="text-gray-600 text-sm mb-2">
                        Recommended Irrigation
                      </p>
                      <p className="text-4xl font-bold text-blue-600">
                        {waterData.schedule?.irrigation?.gross_irrigation_mm?.toFixed(
                          1
                        ) || 0}
                      </p>
                      <p className="text-sm text-gray-600 mt-1">mm</p>
                    </div>

                    {/* Irrigation Interval */}
                    <div className="bg-cyan-50 p-6 rounded-lg border border-cyan-200">
                      <p className="text-gray-600 text-sm mb-2">
                        Irrigation Interval
                      </p>
                      <p className="text-4xl font-bold text-cyan-600">
                        {waterData.schedule?.irrigation?.irrigation_interval_days?.toFixed(
                          0
                        ) || 0}
                      </p>
                      <p className="text-sm text-gray-600 mt-1">days</p>
                    </div>
                  </div>

                  {/* Recommendation Message */}
                  {waterData.schedule?.irrigation?.recommendation && (
                    <div className="bg-green-50 border border-green-300 rounded-lg p-4 mt-6">
                      <p className="text-green-800 font-semibold">
                        💡 {waterData.schedule.irrigation.recommendation}
                      </p>
                    </div>
                  )}
                </div>

                {/* Weather & Soil Data */}
                <div className="grid md:grid-cols-2 gap-6">
                  {/* Weather Info */}
                  {waterData.weather_data && (
                    <div className="bg-white shadow-lg rounded-xl p-6">
                      <h3 className="text-lg font-semibold text-orange-700 mb-4">
                        🌡️ Current Weather
                      </h3>
                      <div className="space-y-2 text-sm">
                        <p>
                          <strong>Temperature:</strong>{" "}
                          {waterData.weather_data.temp_min?.toFixed(1)}°C -{" "}
                          {waterData.weather_data.temp_max?.toFixed(1)}°C
                        </p>
                        <p>
                          <strong>Humidity:</strong>{" "}
                          {waterData.weather_data.rh_mean?.toFixed(0)}%
                        </p>
                        <p>
                          <strong>Wind Speed:</strong>{" "}
                          {waterData.weather_data.wind_speed?.toFixed(1)} m/s
                        </p>
                      </div>
                    </div>
                  )}

                  {/* Soil Info */}
                  {waterData.soil_data && (
                    <div className="bg-white shadow-lg rounded-xl p-6">
                      <h3 className="text-lg font-semibold text-amber-700 mb-4">
                        🌱 Soil Properties
                      </h3>
                      <div className="space-y-2 text-sm">
                        <p>
                          <strong>Soil Type:</strong>{" "}
                          {waterData.soil_data?.soil_type || "N/A"}
                        </p>
                        <p>
                          <strong>Moisture:</strong>{" "}
                          {waterData.soil_data?.moisture
                            ? (waterData.soil_data.moisture * 100)?.toFixed(0)
                            : 0}
                          %
                        </p>
                        <p>
                          <strong>Rainfall (last 1 hour):</strong>{" "}
                          {waterData.soil_data?.rainfall || 0} mm
                        </p>
                      </div>
                    </div>
                  )}
                </div>

                {/* Educational Info */}
                <div className="bg-blue-50 border border-blue-200 rounded-xl p-6">
                  <h3 className="text-lg font-semibold text-blue-800 mb-3">
                    📘 How Irrigation is Calculated
                  </h3>
                  <ul className="text-gray-700 space-y-2 text-sm">
                    <li>
                      <strong>ET₀ (Reference ET):</strong> Based on temperature,
                      humidity, wind & solar radiation
                    </li>
                    <li>
                      <strong>ETc (Crop ET):</strong> ET₀ × Crop Coefficient
                      (depends on crop type & growth stage)
                    </li>
                    <li>
                      <strong>Net Irrigation:</strong> ETc - Effective Rainfall
                    </li>
                    <li>
                      <strong>Gross Irrigation:</strong> Net Irrigation /
                      Application Efficiency
                    </li>
                  </ul>
                  <p className="text-gray-600 text-xs mt-4">
                    This estimation updates with real weather data and adapts to
                    seasonal changes.
                  </p>
                </div>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}
