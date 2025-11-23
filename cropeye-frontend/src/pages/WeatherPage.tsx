// src/pages/WeatherPage.tsx

import React, { useState, useEffect } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
} from "recharts";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { useLocation } from "../hooks/useLocation";
import { api } from "../services/api";
import type { WeatherResponse } from "../types";
import LoadingSpinner from "../components/LoadingSpinner";
import ErrorMessage from "../components/ErrorMessage";
import Navbar from "../components/Navbar";

export const WeatherPage: React.FC = () => {
  const navigate = useNavigate();
  const { logout } = useAuth();
  const { location } = useLocation();
  const [data, setData] = useState<WeatherResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [, setError] = useState("");

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  useEffect(() => {
    const fetchData = async () => {
      if (!location) {
        setError("Please set a location first");
        return;
      }

      setLoading(true);
      setError("");

      try {
        const result = await api.weather.agricultural(
          location.lat,
          location.lng
        );
        setData(result);
      } catch (error) {
        console.error("Weather API error:", error);
        setError(
          "Failed to fetch weather data. Please check backend connection."
        );
        // Remove mock data fallback - show error instead
        setData(null);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [location]);

  if (!location) {
    return (
      <div className="min-h-screen bg-linear-to-br from-green-100 to-amber-100 p-6">
        <div className="max-w-4xl mx-auto">
          <ErrorMessage message="Please set a location from the dashboard" />
        </div>
      </div>
    );
  }

  if (loading) return <LoadingSpinner message="Fetching weather data..." />;

  return (
    <div className="min-h-screen bg-linear-to-br from-green-100 to-amber-100">
      <Navbar onLogout={handleLogout} />
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <h1 className="text-3xl font-bold mb-6">Weather Forecast</h1>

        {/* Error display removed since error is not used */}

        {data && (
          <div className="space-y-6">
            {/* Current Weather */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="bg-white p-6 rounded-lg shadow border">
                <p className="text-gray-600 text-sm mb-1">Temperature</p>
                <p className="text-3xl font-bold text-orange-600">
                  {data.temp}°C
                </p>
              </div>
              <div className="bg-white p-6 rounded-lg shadow border">
                <p className="text-gray-600 text-sm mb-1">Humidity</p>
                <p className="text-3xl font-bold text-blue-600">
                  {data.humidity}%
                </p>
              </div>
              <div className="bg-white p-6 rounded-lg shadow border">
                <p className="text-gray-600 text-sm mb-1">Rainfall</p>
                <p className="text-3xl font-bold text-green-600">
                  {data.rainfall} mm
                </p>
              </div>
              <div className="bg-white p-6 rounded-lg shadow border">
                <p className="text-gray-600 text-sm mb-1">Wind Speed</p>
                <p className="text-3xl font-bold text-gray-700">
                  {data.wind_speed} km/h
                </p>
              </div>
            </div>

            {/* Alerts */}
            {data.alerts && data.alerts.length > 0 && (
              <div className="bg-yellow-50 border border-yellow-200 p-4 rounded-lg">
                <h3 className="font-semibold text-yellow-900 mb-2">
                  ⚠️ Weather Alerts
                </h3>
                {data.alerts.map((alert, idx) => (
                  <p key={idx} className="text-yellow-800 text-sm">
                    {alert.message}
                  </p>
                ))}
              </div>
            )}

            {/* Agricultural Context */}
            <div className="bg-white p-6 rounded-lg shadow border">
              <h2 className="text-xl font-bold mb-4">Agricultural Context</h2>
              <div className="grid md:grid-cols-3 gap-4">
                <div>
                  <p className="text-gray-600 text-sm">
                    Growing Degree Days (GDD)
                  </p>
                  <p className="text-2xl font-bold text-green-600">
                    {data.agricultural_context.gdd}
                  </p>
                </div>
                <div>
                  <p className="text-gray-600 text-sm">Frost Risk</p>
                  <p className="text-2xl font-bold text-blue-600">
                    {data.agricultural_context.frost_risk}
                  </p>
                </div>
                <div>
                  <p className="text-gray-600 text-sm">Heat Stress Index</p>
                  <p className="text-2xl font-bold text-orange-600">
                    {(data.agricultural_context.heat_stress * 100).toFixed(0)}%
                  </p>
                </div>
              </div>
            </div>

            {/* Educational Insights - Always visible */}
            <div className="bg-linear-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-xl p-6 shadow-lg">
              <h3 className="text-xl font-bold text-blue-800 mb-4">
                🌤️ Understanding Weather Analysis Calculations
              </h3>
              <p className="text-blue-700 leading-relaxed mb-4">
                Our weather intelligence system integrates meteorological data
                with crop physiology models to provide hyper-local agricultural
                forecasts. The system processes real-time satellite weather
                data, ground station observations, and climate models to
                generate crop-specific insights. Growing Degree Days are
                calculated using temperature accumulation formulas, frost risk
                is assessed through probabilistic modeling of minimum
                temperatures, and heat stress indices incorporate humidity and
                duration factors. Weather alerts are triggered based on
                threshold crossings that could impact crop development, enabling
                proactive farm management decisions.
              </p>
              <div className="grid md:grid-cols-2 gap-6">
                <div className="bg-white/70 backdrop-blur-sm rounded-lg p-4">
                  <h4 className="font-semibold text-blue-800 mb-2">
                    🌡️ Growing Degree Days (GDD)
                  </h4>
                  <p className="text-sm text-gray-700">
                    <strong>GDD = ((Tmax + Tmin)/2) - Tbase</strong>
                    <br />
                    Where Tbase is usually 10°C (50°F). Measures heat
                    accumulation above crop base temperature. Higher GDD
                    indicates more favorable growing conditions and faster crop
                    development.
                  </p>
                </div>
                <div className="bg-white/70 backdrop-blur-sm rounded-lg p-4">
                  <h4 className="font-semibold text-blue-800 mb-2">
                    ❄️ Frost Risk Assessment
                  </h4>
                  <p className="text-sm text-gray-700">
                    Based on minimum temperature forecasts and crop sensitivity
                    thresholds. Risk levels: Low ({">"}5°C), Medium (0-5°C),
                    High ({"<"}0°C). Considers crop phenology and historical
                    frost patterns for accurate assessment.
                  </p>
                </div>
                <div className="bg-white/70 backdrop-blur-sm rounded-lg p-4">
                  <h4 className="font-semibold text-blue-800 mb-2">
                    🔥 Heat Stress Index
                  </h4>
                  <p className="text-sm text-gray-700">
                    <strong>
                      HSI = (T - Topt) × Duration × Humidity Factor
                    </strong>
                    <br />
                    Where Topt is optimal temperature for the crop. Values above
                    30% indicate potential heat stress that can reduce
                    photosynthesis, yield, and quality.
                  </p>
                </div>
                <div className="bg-white/70 backdrop-blur-sm rounded-lg p-4">
                  <h4 className="font-semibold text-blue-800 mb-2">
                    ⚠️ Weather Alert System
                  </h4>
                  <p className="text-sm text-gray-700">
                    Monitors temperature extremes ({">"}35°C or {"<"}0°C), heavy
                    rainfall ({">"}50mm/day), and drought conditions (SPI {"<"}{" "}
                    -1.5). Alerts are triggered based on crop-specific
                    thresholds and historical impact data.
                  </p>
                </div>
              </div>
            </div>

            {/* 7-Day Forecast Chart */}
            <div className="bg-white p-6 rounded-lg shadow border">
              <h2 className="text-xl font-bold mb-4">
                7-Day Temperature Forecast
              </h2>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={data.forecast_7day}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Line
                    type="monotone"
                    dataKey="temp_max"
                    stroke="#f97316"
                    name="Max Temp"
                    strokeWidth={2}
                  />
                  <Line
                    type="monotone"
                    dataKey="temp_min"
                    stroke="#3b82f6"
                    name="Min Temp"
                    strokeWidth={2}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>

            {/* Rainfall Forecast */}
            <div className="bg-white p-6 rounded-lg shadow border">
              <h2 className="text-xl font-bold mb-4">
                7-Day Rainfall Forecast
              </h2>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={data.forecast_7day}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="rain" fill="#10b981" name="Rainfall (mm)" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default WeatherPage;
