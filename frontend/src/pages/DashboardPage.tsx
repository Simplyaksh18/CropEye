import React from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { useLocation } from "../hooks/useLocation";
import ModuleCard from "../components/ModuleCard";
import LocationInput from "../components/LocationInput";
import FloatingCards from "../components/FloatingCards";
import ServicesStatus from "../components/ServicesStatus";
import Navbar from "../components/Navbar";

export const DashboardPage: React.FC = () => {
  const navigate = useNavigate();
  const { logout } = useAuth();
  const { location, setLocation } = useLocation();

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
    if (!location) {
      alert("Please set your location first to access agricultural modules");
      return;
    }
    navigate(path);
  };

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  return (
    <div className="min-h-screen bg-linear-to-br from-green-100 to-amber-100">
      <Navbar onLogout={handleLogout} />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">CropEye</h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto mb-6">
            Welcome to your agricultural intelligence platform. Access various
            tools to optimize your farming operations and maximize yields.
          </p>

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

              {/* Compact highlights - keep dashboard informative while
                  FloatingCards provides the dynamic Why-Choose messages */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <div className="bg-white p-6 rounded-lg shadow border">
                  <h4 className="font-semibold text-gray-800 mb-2">
                    Active Fields
                  </h4>
                  <p className="text-3xl font-bold text-green-700">27</p>
                  <p className="text-sm text-gray-500">
                    Fields being monitored
                  </p>
                </div>
                <div className="bg-white p-6 rounded-lg shadow border">
                  <h4 className="font-semibold text-gray-800 mb-2">Avg NDVI</h4>
                  <p className="text-3xl font-bold text-blue-600">0.62</p>
                  <p className="text-sm text-gray-500">
                    Field health index (sample)
                  </p>
                </div>
                <div className="bg-white p-6 rounded-lg shadow border">
                  <h4 className="font-semibold text-gray-800 mb-2">
                    Connected Sensors
                  </h4>
                  <p className="text-3xl font-bold text-orange-600">12</p>
                  <p className="text-sm text-gray-500">
                    Live soil & weather sensors
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Location Input - After main content */}
        <div className="mb-8">
          <LocationInput onLocationSelect={setLocation} />
        </div>

        <div className="mb-8 flex flex-col md:flex-row gap-4 items-start">
          <ServicesStatus />
          <FloatingCards />
        </div>

        {/* Current Location Display */}
        {location && (
          <div className="bg-white p-6 rounded-xl shadow-lg border border-gray-200 mb-8 max-w-md mx-auto">
            <h3 className="text-lg font-semibold text-gray-800 mb-2 text-center">
              📍 Current Location
            </h3>
            <p className="text-gray-700 text-center">
              {location.lat.toFixed(4)}, {location.lng.toFixed(4)}
              {location.name && (
                <span className="font-medium block mt-1">
                  ({location.name})
                </span>
              )}
            </p>
          </div>
        )}

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
