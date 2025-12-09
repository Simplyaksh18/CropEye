// src/pages/WeatherPage.tsx
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { useLocation } from "../context/LocationContext";
import Navbar from "../components/Navbar";
import LoadingSpinner from "../components/LoadingSpinner";
import ErrorMessage from "../components/ErrorMessage";

interface WeatherResponse {
  temperature: {
    current: number;
    feels_like: number;
    min: number;
    max: number;
  };
  humidity: number;
  rain?: number;
  pressure: number;
  wind: { speed: number };
  clouds: number;
  weather: {
    main: string;
    description: string;
    icon: string;
  };
  agricultural_context?: {
    heat_stress?: {
      temperature_c: number;
      humidity_percent: number;
      stress_level: string;
      recommendation: string;
    };
    frost_risk?: {
      current_temperature: number;
      risk_level: string;
      recommendation: string;
    };
    gdd?: number;
    et?: {
      et_mm_day: number;
    };
  };
  data_source?: string;
}

export default function WeatherPage() {
  const navigate = useNavigate();
  const { logout } = useAuth();
  const { location } = useLocation();
  const [weather, setWeather] = useState<WeatherResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  useEffect(() => {
    if (!location?.lat || !location?.lng) {
      setLoading(false);
      return;
    }

    console.log("📡 Fetching Weather for:", location);
    setLoading(true);
    setError("");

    fetch(
      `http://localhost:5003/api/weather/current?lat=${location.lat}&lng=${location.lng}`
    )
      .then((res) => res.json())
      .then((data) => {
        console.log("🌦 API Response:", data);
        setWeather(data);
        setLoading(false);
      })
      .catch((e) => {
        console.error("❌ Weather fetch error:", e);
        setError("Failed to fetch weather data.");
        setLoading(false);
      });
  }, [location?.lat, location?.lng]);

  if (!location?.lat || !location?.lng) {
    return <ErrorMessage message="Set location first" />;
  }

  const agri = weather?.agricultural_context;

  return (
    <div className="min-h-screen bg-linear-to-br from-blue-200 to-indigo-300 text-gray-900">
      <Navbar onLogout={handleLogout} />

      <main className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <h1 className="text-3xl font-bold text-purple-700 mb-3">
          🌤️ Weather Conditions
        </h1>
        <p className="text-gray-600 mb-6">
          Real-time weather data with agricultural insights for crop management.
        </p>

        {loading && <LoadingSpinner message="🌡️ Fetching current weather..." />}
        {error && <ErrorMessage message={error} />}

        {!loading && !error && weather && (
          <div className="space-y-6">
            {/* Current weather */}
            <div className="bg-white rounded-xl p-6 shadow-lg">
              <h2 className="text-xl font-bold mb-4">🌤 Current Weather</h2>

              <div className="grid grid-cols-2 md:grid-cols-3 gap-6">
                <WeatherItem
                  label="Temperature"
                  value={`${weather.temperature.current}°C`}
                />
                <WeatherItem
                  label="Feels Like"
                  value={`${weather.temperature.feels_like}°C`}
                />
                <WeatherItem label="Humidity" value={`${weather.humidity}%`} />
                <WeatherItem
                  label="Pressure"
                  value={`${weather.pressure} hPa`}
                />
                <WeatherItem
                  label="Wind Speed"
                  value={`${weather.wind.speed} m/s`}
                />
                <WeatherItem label="Clouds" value={`${weather.clouds}%`} />
                <WeatherItem
                  label="Rain (Last 1h)"
                  value={`${weather.rain ? weather.rain : 0} mm`}
                />
              </div>

              <p className="mt-3 text-gray-600 text-sm">
                Source: {weather.data_source || "OpenWeather"}
              </p>
            </div>

            {/* Agri Weather Insights */}
            {agri && (
              <div className="bg-white rounded-xl p-6 shadow-xl">
                <h2 className="text-xl font-bold mb-4">
                  🌱 Agricultural Weather Insights
                </h2>

                <div className="grid md:grid-cols-3 gap-6">
                  {agri.heat_stress && (
                    <AgriCard
                      title="🔥 Heat Stress"
                      value={`${agri.heat_stress.temperature_c}°C / ${agri.heat_stress.humidity_percent}%`}
                      desc={agri.heat_stress.recommendation}
                    />
                  )}

                  {agri.frost_risk && (
                    <AgriCard
                      title="❄ Frost Risk"
                      value={agri.frost_risk.risk_level}
                      desc={agri.frost_risk.recommendation}
                    />
                  )}

                  {agri.et && (
                    <AgriCard
                      title="💧 Evapotranspiration"
                      value={`${agri.et.et_mm_day} mm/day`}
                      desc="Higher ET → More irrigation needed"
                    />
                  )}

                  {agri.gdd && (
                    <AgriCard
                      title="🌾 Growing Degree Days"
                      value={`${agri.gdd.toFixed(1)}`}
                      desc="Good for crop progress analysis"
                    />
                  )}
                </div>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}

function WeatherItem({
  label,
  value,
}: {
  label: string;
  value: string | number;
}) {
  return (
    <div className="bg-gray-100 p-4 rounded-lg text-center">
      <p className="text-gray-600 text-sm">{label}</p>
      <p className="font-semibold text-lg mt-1 text-gray-900">{value}</p>
    </div>
  );
}

function AgriCard({
  title,
  value,
  desc,
}: {
  title: string;
  value: string | number;
  desc: string;
}) {
  return (
    <div className="border border-gray-300 bg-gray-100 p-4 rounded-lg">
      <h3 className="font-semibold mb-2 text-gray-900">{title}</h3>
      <p className="text-green-600 font-bold text-xl">{value}</p>
      <p className="text-gray-600 text-xs mt-2">{desc}</p>
    </div>
  );
}
