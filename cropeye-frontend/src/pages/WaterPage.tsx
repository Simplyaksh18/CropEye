import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { useLocation } from "../hooks/useLocation";
import { api } from "../services/api";
import type { WaterResponse } from "../types";
import LoadingSpinner from "../components/LoadingSpinner";
import ErrorMessage from "../components/ErrorMessage";
import Navbar from "../components/Navbar";

export const WaterPage: React.FC = () => {
  const navigate = useNavigate();
  const { logout } = useAuth();
  const { location } = useLocation();
  const [data, setData] = useState<WaterResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [cropType, setCropType] = useState("wheat");
  const [growthStage, setGrowthStage] = useState("vegetative");

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  const fetchData = React.useCallback(async () => {
    if (!location) return;
    setLoading(true);
    setError("");
    try {
      const result = await api.water.calculate({
        weather_data: { temp: 28, humidity: 65 },
        soil_data: { texture: "loam" },
        crop_type: cropType,
        growth_stage: growthStage,
      });
      setData(result);
    } catch (error) {
      console.error("Water API error:", error);
      setError(
        "Failed to fetch water management data. Please check backend connection."
      );
      setData(null);
    } finally {
      setLoading(false);
    }
  }, [location, cropType, growthStage]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  if (!location) return <ErrorMessage message="Set location first" />;
  if (loading) return <LoadingSpinner />;

  // normalize water response fields: use top-level aliases if present, otherwise fall back to nested schedule
  let et0 = 0,
    etc = 0,
    irrigationReq = 0,
    irrigationScheduleDays = 0,
    waterStressIndex = 0,
    recommendationStr = "";

  if (data) {
    et0 = data.et0_mm_day ?? data.schedule?.et0_mm_day ?? 0;
    etc = data.etc_mm_day ?? data.schedule?.etc_mm_day ?? 0;
    irrigationReq =
      data.irrigation_requirement_mm ??
      data.schedule?.irrigation?.gross_irrigation_mm ??
      0;
    irrigationScheduleDays =
      data.irrigation_schedule_days ??
      data.schedule?.schedule?.irrigation_schedule_days ??
      0;
    waterStressIndex =
      data.water_stress_index ??
      data.schedule?.schedule?.water_stress_index ??
      0;
    recommendationStr =
      data.recommendation ?? data.schedule?.schedule?.recommendation ?? "";
  }

  return (
    <div className="min-h-screen bg-linear-to-br from-green-100 to-amber-100">
      <Navbar onLogout={handleLogout} />
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <h1 className="text-3xl font-bold mb-6">Water Management</h1>

        {error && <ErrorMessage message={error} />}

        {/* Crop Selection */}
        <div className="bg-white p-6 rounded-lg shadow mb-6">
          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-2">
                Crop Type
              </label>
              <select
                value={cropType}
                onChange={(e) => setCropType(e.target.value)}
                className="w-full p-2 border rounded"
              >
                <option value="wheat">Wheat</option>
                <option value="rice">Rice</option>
                <option value="corn">Corn</option>
                <option value="cotton">Cotton</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">
                Growth Stage
              </label>
              <select
                value={growthStage}
                onChange={(e) => setGrowthStage(e.target.value)}
                className="w-full p-2 border rounded"
              >
                <option value="initial">Initial</option>
                <option value="vegetative">Vegetative</option>
                <option value="flowering">Flowering</option>
                <option value="maturity">Maturity</option>
              </select>
            </div>
          </div>
        </div>

        {data && (
          <div className="space-y-6">
            {/* ET Values */}
            <div className="grid md:grid-cols-3 gap-4">
              <div className="bg-blue-50 p-6 rounded-lg border border-blue-200">
                <p className="text-sm text-gray-600 mb-1">ET₀ (Reference)</p>
                <p className="text-3xl font-bold text-blue-600">
                  {et0.toFixed(1)}
                </p>
                <p className="text-sm text-gray-600">mm/day</p>
              </div>
              <div className="bg-green-50 p-6 rounded-lg border border-green-200">
                <p className="text-sm text-gray-600 mb-1">ETc (Crop)</p>
                <p className="text-3xl font-bold text-green-600">
                  {etc.toFixed(1)}
                </p>
                <p className="text-sm text-gray-600">mm/day</p>
              </div>
              <div className="bg-purple-50 p-6 rounded-lg border border-purple-200">
                <p className="text-sm text-gray-600 mb-1">Irrigation Need</p>
                <p className="text-3xl font-bold text-purple-600">
                  {irrigationReq.toFixed(1)}
                </p>
                <p className="text-sm text-gray-600">mm</p>
              </div>
            </div>

            {/* Schedule */}
            <div className="bg-white p-6 rounded-lg shadow border">
              <h2 className="text-xl font-bold mb-4">Irrigation Schedule</h2>
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-600 text-sm">Next Irrigation</p>
                  <p className="text-3xl font-bold text-blue-600">
                    {irrigationScheduleDays.toFixed(1)} days
                  </p>
                </div>
                <div className="text-6xl">💧</div>
              </div>
            </div>

            {/* Water Stress */}
            <div className="bg-white p-6 rounded-lg shadow border">
              <h2 className="text-xl font-bold mb-4">Water Stress Index</h2>
              <p className="text-4xl font-bold text-orange-600 mb-2">
                {(waterStressIndex * 100).toFixed(0)}%
              </p>
              <div className="w-full bg-gray-200 rounded-full h-4">
                <div
                  className="bg-orange-600 h-4 rounded-full"
                  style={{ width: `${waterStressIndex * 100}%` }}
                />
              </div>
              <p className="text-sm text-gray-600 mt-2">
                {waterStressIndex < 0.3
                  ? "Low Stress"
                  : waterStressIndex < 0.6
                  ? "Moderate Stress"
                  : "High Stress"}
              </p>
            </div>

            {/* Recommendation */}
            <div className="bg-green-50 border border-green-200 p-6 rounded-lg">
              <h3 className="font-semibold text-green-900 mb-2">
                Recommendation
              </h3>
              <p className="text-green-800">{recommendationStr}</p>
            </div>

            {/* Educational Insights - Always visible */}
            <div className="bg-linear-to-r from-cyan-50 to-blue-50 border border-cyan-200 rounded-xl p-6 shadow-lg">
              <h3 className="text-xl font-bold text-cyan-800 mb-4">
                💧 Understanding Water Management Calculations
              </h3>
              <p className="text-cyan-700 leading-relaxed mb-4">
                Water management in agriculture relies on precise
                evapotranspiration calculations and soil moisture monitoring to
                optimize irrigation efficiency. The system uses advanced
                meteorological data and crop physiology models to determine
                exact water requirements, preventing both water waste and crop
                stress.
              </p>
              <div className="grid md:grid-cols-2 gap-6">
                <div className="bg-white/70 backdrop-blur-sm rounded-lg p-4">
                  <h4 className="font-semibold text-cyan-800 mb-2">
                    🌡️ Evapotranspiration (ET) Calculations
                  </h4>
                  <p className="text-sm text-gray-700">
                    <strong>
                      ET₀ = (0.408Δ(Rn-G) +
                      γ(900/(T+273))u₂(es-ea))/(Δ+γ(1+0.34u₂))
                    </strong>
                    <br />
                    Reference ET calculated using Penman-Monteith equation. ETc
                    (Crop ET) = ET₀ × Kc, where Kc varies by crop type and
                    growth stage (0.3-1.2).
                  </p>
                </div>
                <div className="bg-white/70 backdrop-blur-sm rounded-lg p-4">
                  <h4 className="font-semibold text-cyan-800 mb-2">
                    💧 Irrigation Requirements
                  </h4>
                  <p className="text-sm text-gray-700">
                    <strong>
                      Irrigation Need = ETc - Effective Rainfall + Leaching
                    </strong>
                    <br />
                    Considers soil water holding capacity, root depth, and
                    salinity leaching requirements. Prevents over/under-watering
                    through precise scheduling.
                  </p>
                </div>
                <div className="bg-white/70 backdrop-blur-sm rounded-lg p-4">
                  <h4 className="font-semibold text-cyan-800 mb-2">
                    📊 Water Stress Index
                  </h4>
                  <p className="text-sm text-gray-700">
                    <strong>WSI = 1 - (Actual ET / Potential ET)</strong>
                    <br />
                    WSI {">"} 0.3 indicates stress. Integrates soil moisture
                    sensors, canopy temperature, and spectral reflectance for
                    real-time assessment.
                  </p>
                </div>
                <div className="bg-white/70 backdrop-blur-sm rounded-lg p-4">
                  <h4 className="font-semibold text-cyan-800 mb-2">
                    📅 Irrigation Scheduling
                  </h4>
                  <p className="text-sm text-gray-700">
                    Based on soil moisture depletion thresholds (typically 50%
                    of available water capacity). Considers crop sensitivity,
                    weather forecasts, and irrigation efficiency to optimize
                    timing and amounts.
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
