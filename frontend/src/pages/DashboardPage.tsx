import React from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { useLocation } from "../context/LocationContext";
import ModuleCard from "../components/ModuleCard";
import LocationInput from "../components/LocationInput";
import FloatingCards from "../components/FloatingCards";
import ServicesStatus from "../components/ServicesStatus";
import Navbar from "../components/Navbar";

export const DashboardPage: React.FC = () => {
  const navigate = useNavigate();
  useAuth();
  const { location } = useLocation();

  const modules = [
    {
      title: "Crop Recommendations",
      description:
        "Get AI-powered crop suggestions based on your location and soil conditions",
      icon: "🌾",
      path: "/crops",
      color: "bg-green-500",
    },
    {
      title: "NDVI Analysis",
      description: "Monitor crop health using satellite vegetation indices",
      icon: "🌱",
      path: "/ndvi",
      color: "bg-blue-500",
    },
    {
      title: "Weather Forecast",
      description:
        "7-day agricultural weather forecast with crop-specific insights",
      icon: "🌤️",
      path: "/weather",
      color: "bg-yellow-500",
    },
    {
      title: "Water Management",
      description: "Calculate irrigation needs and optimize water usage",
      icon: "💧",
      path: "/water",
      color: "bg-cyan-500",
    },
    {
      title: "Soil Analysis",
      description:
        "Analyze soil composition and get fertilization recommendations",
      icon: "🏞️",
      path: "/soil",
      color: "bg-amber-500",
    },
    {
      title: "Pest Detection",
      description: "Identify potential pests and diseases affecting your crops",
      icon: "🐛",
      path: "/pests",
      color: "bg-red-500",
    },
  ];

  const handleModuleClick = (path: string) => {
    if (!location || location.lat == null || location.lng == null) {
      alert("Please set your location first to access agricultural modules");
      return;
    }
    navigate(path);
  };

  return (
    <div className="min-h-screen bg-linear-to-br from-green-100 to-amber-100">
      <Navbar />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold italic mb-6">
            <span className="text-5xl">🌾</span>{" "}
            <span className="text-blue-600">
              CropEye - Cultivating Intelligence, Harvesting Success
            </span>
          </h1>

          {/* Platform Overview Card - Same width as What We Do */}
          <div className="bg-linear-to-r from-green-50 via-blue-50 to-purple-50 border-2 border-green-200 rounded-2xl p-8 max-w-6xl mx-auto mb-8 shadow-xl">
            <div className="bg-white/70 backdrop-blur-sm rounded-xl p-8">
              <div className="flex items-center justify-center mb-6">
                <span className="text-4xl mr-3">🚀</span>
                <h2 className="text-3xl font-bold text-green-700">
                  Precision Agriculture Powered by Space Technology
                </h2>
              </div>

              <p className="text-lg text-gray-700 leading-relaxed mb-6">
                <span className="font-semibold text-green-700">CropEye</span>{" "}
                transforms farming with cutting-edge satellite and weather data,
                delivering instant agricultural intelligence that was once
                available only to research institutions—now accessible from your
                device.
              </p>

              <div className="grid md:grid-cols-2 gap-6 mb-6">
                <div className="bg-linear-to-br from-blue-50 to-blue-100 p-5 rounded-lg border-l-4 border-blue-500">
                  <div className="flex items-start">
                    <span className="text-3xl mr-3">🛰️</span>
                    <div className="text-left">
                      <h3 className="font-bold text-blue-800 mb-2">
                        Real Satellite Data
                      </h3>
                      <p className="text-sm text-gray-700">
                        Live imagery from <strong>Copernicus Sentinel-2</strong>{" "}
                        satellites captures your fields every few days,
                        revealing crop health patterns invisible to the naked
                        eye through multispectral analysis.
                      </p>
                    </div>
                  </div>
                </div>

                <div className="bg-linear-to-br from-amber-50 to-amber-100 p-5 rounded-lg border-l-4 border-amber-500">
                  <div className="flex items-start">
                    <span className="text-3xl mr-3">🌦️</span>
                    <div className="text-left">
                      <h3 className="font-bold text-amber-800 mb-2">
                        Hyper-Local Weather
                      </h3>
                      <p className="text-sm text-gray-700">
                        Precision forecasts from <strong>OpenWeather</strong> &{" "}
                        <strong>Open-Meteo</strong> APIs provide hourly updates
                        for your exact location, helping you time irrigation,
                        fertilization, and harvesting perfectly.
                      </p>
                    </div>
                  </div>
                </div>

                <div className="bg-linear-to-br from-green-50 to-green-100 p-5 rounded-lg border-l-4 border-green-500">
                  <div className="flex items-start">
                    <span className="text-3xl mr-3">🗺️</span>
                    <div className="text-left">
                      <h3 className="font-bold text-green-800 mb-2">
                        GIS Analysis Engine
                      </h3>
                      <p className="text-sm text-gray-700">
                        Our Geographic Information System processes spatial data
                        in real-time, calculating NDVI (vegetation health), soil
                        composition, and terrain analysis instantly for any
                        location worldwide.
                      </p>
                    </div>
                  </div>
                </div>

                <div className="bg-linear-to-br from-purple-50 to-purple-100 p-5 rounded-lg border-l-4 border-purple-500">
                  <div className="flex items-start">
                    <span className="text-3xl mr-3">🤖</span>
                    <div className="text-left">
                      <h3 className="font-bold text-purple-800 mb-2">
                        AI-Powered Insights
                      </h3>
                      <p className="text-sm text-gray-700">
                        Machine learning algorithms analyze millions of data
                        points to predict pest outbreaks, recommend optimal
                        crops, and suggest precise fertilizer applications
                        tailored to your soil conditions.
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              <div className="bg-linear-to-r from-green-600 to-blue-600 text-white p-6 rounded-lg">
                <p className="text-lg font-medium text-center">
                  ✨ From satellite imagery to actionable farming advice in
                  seconds—your personal agricultural command center, available
                  24/7 from anywhere.
                </p>
              </div>
            </div>
          </div>

          {/* Dashboard Info Card - Prominent */}
          <div className="bg-linear-to-r from-green-50 via-blue-50 to-purple-50 border-2 border-green-200 rounded-2xl p-8 max-w-6xl mx-auto mb-8 shadow-xl">
            <div className="text-center">
              <div className="bg-white/70 backdrop-blur-sm rounded-xl p-8 mb-6">
                <h3 className="text-3xl font-bold text-green-700 mb-6">
                  🌾 What We Do
                </h3>
                <p className="text-gray-700 leading-relaxed text-lg mb-6">
                  CropEye revolutionizes agriculture through cutting-edge
                  technology, providing farmers with unprecedented insights and
                  control over their operations.
                </p>
                <div className="grid md:grid-cols-2 gap-8 text-left">
                  <div className="bg-green-50 p-6 rounded-lg">
                    <h4 className="font-bold text-green-700 mb-3 text-lg">
                      🛰️ Satellite Monitoring
                    </h4>
                    <p className="text-gray-700 text-base leading-relaxed">
                      Advanced NDVI analysis and multispectral satellite imagery
                      provide real-time crop health monitoring across entire
                      fields, detecting stress patterns invisible to the naked
                      eye.
                    </p>
                  </div>
                  <div className="bg-blue-50 p-6 rounded-lg">
                    <h4 className="font-bold text-blue-700 mb-3 text-lg">
                      🌤️ Weather Intelligence
                    </h4>
                    <p className="text-gray-700 text-base leading-relaxed">
                      Hyper-local 7-day forecasts with crop-specific insights,
                      frost warnings, and irrigation recommendations based on
                      your exact location and crop types.
                    </p>
                  </div>
                  <div className="bg-amber-50 p-6 rounded-lg">
                    <h4 className="font-bold text-amber-700 mb-3 text-lg">
                      🧪 Soil Analysis
                    </h4>
                    <p className="text-gray-700 text-base leading-relaxed">
                      Comprehensive soil composition analysis with AI-powered
                      fertilization recommendations, pH optimization, and
                      nutrient deficiency detection for maximum yield potential.
                    </p>
                  </div>
                  <div className="bg-cyan-50 p-6 rounded-lg">
                    <h4 className="font-bold text-cyan-700 mb-3 text-lg">
                      💧 Water Optimization
                    </h4>
                    <p className="text-gray-700 text-base leading-relaxed">
                      Smart irrigation scheduling based on soil moisture
                      sensors, weather predictions, and crop water requirements
                      to minimize waste while ensuring optimal hydration.
                    </p>
                  </div>
                </div>
              </div>

              {/* Dashboard Statistics Cards */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <div className="bg-white p-6 rounded-lg shadow border border-green-200 hover:shadow-lg transition-shadow">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-semibold text-gray-800">
                      Real-Time Monitoring
                    </h4>
                    <span className="text-2xl">📡</span>
                  </div>
                  <p className="text-3xl font-bold text-green-700 mb-2">24/7</p>
                  <p className="text-sm text-gray-600">
                    Continuous satellite & sensor data collection
                  </p>
                </div>
                <div className="bg-white p-6 rounded-lg shadow border border-blue-200 hover:shadow-lg transition-shadow">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-semibold text-gray-800">AI Accuracy</h4>
                    <span className="text-2xl">🎯</span>
                  </div>
                  <p className="text-3xl font-bold text-blue-600 mb-2">94%</p>
                  <p className="text-sm text-gray-600">
                    Precision in crop health & pest detection
                  </p>
                </div>
                <div className="bg-white p-6 rounded-lg shadow border border-cyan-200 hover:shadow-lg transition-shadow">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-semibold text-gray-800">
                      Yield Increase
                    </h4>
                    <span className="text-2xl">📈</span>
                  </div>
                  <p className="text-3xl font-bold text-cyan-600 mb-2">40%</p>
                  <p className="text-sm text-gray-600">
                    Average crop yield boost with data-driven insights
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Location Input - After main content */}
        <div className="mb-8">
          <LocationInput />
        </div>

        <div className="mb-8 flex flex-col md:flex-row gap-4 items-start">
          <ServicesStatus />
          <FloatingCards />

          {/* Current Location Display */}
          {location && (
            <div className="bg-white p-6 rounded-xl shadow-lg border border-gray-200 shrink-0 md:w-80">
              <h3 className="text-lg font-semibold text-gray-800 mb-2 text-center">
                📍 Current Location
              </h3>
              <p className="text-gray-700 text-center">
                {location.lat?.toFixed(4) ?? "N/A"},{" "}
                {location.lng?.toFixed(4) ?? "N/A"}
                {(location as { name?: string }).name && (
                  <span className="font-medium block mt-1">
                    ({(location as { name?: string }).name})
                  </span>
                )}
              </p>
            </div>
          )}
        </div>

        {/* Modules Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
          {modules.map((module) => (
            <ModuleCard
              key={module.path}
              title={module.title}
              description={module.description}
              icon={module.icon}
              color={module.color}
              onClick={() => handleModuleClick(module.path)}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
