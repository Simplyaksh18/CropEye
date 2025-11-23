import React from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { useLocation } from "../hooks/useLocation";
import ModuleCard from "../components/ModuleCard";
import LocationInput from "../components/LocationInput";
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

              <div className="bg-white/70 backdrop-blur-sm rounded-xl p-8">
                <h3 className="text-3xl font-bold text-blue-700 mb-6">
                  💡 Why Choose CropEye?
                </h3>
                <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 text-left">
                  <div className="bg-linear-to-br from-green-100 to-green-200 p-4 rounded-lg border border-green-300">
                    <h4 className="font-bold text-green-800 mb-3 text-base">
                      📈 Increase Yields
                    </h4>
                    <p className="text-gray-700 text-sm leading-relaxed">
                      Boost productivity by 15-25% through precision agriculture
                      techniques and data-driven crop management strategies.
                    </p>
                  </div>
                  <div className="bg-linear-to-br from-blue-100 to-blue-200 p-4 rounded-lg border border-blue-300">
                    <h4 className="font-bold text-blue-800 mb-3 text-base">
                      💰 Reduce Costs
                    </h4>
                    <p className="text-gray-700 text-sm leading-relaxed">
                      Save up to 30% on inputs through optimized resource
                      allocation, reduced waste, and targeted application of
                      fertilizers and pesticides.
                    </p>
                  </div>
                  <div className="bg-linear-to-br from-yellow-100 to-yellow-200 p-4 rounded-lg border border-yellow-300">
                    <h4 className="font-bold text-yellow-800 mb-3 text-base">
                      🌱 Early Detection
                    </h4>
                    <p className="text-gray-700 text-sm leading-relaxed">
                      Identify problems before they become visible with
                      continuous monitoring and predictive analytics for
                      proactive intervention.
                    </p>
                  </div>
                  <div className="bg-linear-to-br from-purple-100 to-purple-200 p-4 rounded-lg border border-purple-300">
                    <h4 className="font-bold text-purple-800 mb-3 text-base">
                      📊 Smart Decisions
                    </h4>
                    <p className="text-gray-700 text-sm leading-relaxed">
                      Make informed choices backed by satellite data, AI
                      analysis, and historical trends for sustainable and
                      profitable farming.
                    </p>
                  </div>
                  <div className="bg-linear-to-br from-indigo-100 to-indigo-200 p-4 rounded-lg border border-indigo-300">
                    <h4 className="font-bold text-indigo-800 mb-3 text-base">
                      🌍 Climate Adaptation
                    </h4>
                    <p className="text-gray-700 text-sm leading-relaxed">
                      Adapt to changing weather patterns with predictive
                      analytics and climate-resilient crop recommendations for
                      future-proof farming.
                    </p>
                  </div>
                  <div className="bg-linear-to-br from-pink-100 to-pink-200 p-4 rounded-lg border border-pink-300">
                    <h4 className="font-bold text-pink-800 mb-3 text-base">
                      📱 Easy Access
                    </h4>
                    <p className="text-gray-700 text-sm leading-relaxed">
                      User-friendly mobile and web interface accessible
                      anywhere, anytime for modern farmers and agricultural
                      professionals.
                    </p>
                  </div>
                  <div className="bg-linear-to-br from-teal-100 to-teal-200 p-4 rounded-lg border border-teal-300">
                    <h4 className="font-bold text-teal-800 mb-3 text-base">
                      🔄 Continuous Learning
                    </h4>
                    <p className="text-gray-700 text-sm leading-relaxed">
                      AI models continuously improve with new data, providing
                      increasingly accurate recommendations and adapting to your
                      farm.
                    </p>
                  </div>
                  <div className="bg-linear-to-br from-orange-100 to-orange-200 p-4 rounded-lg border border-orange-300">
                    <h4 className="font-bold text-orange-800 mb-3 text-base">
                      🤝 Expert Support
                    </h4>
                    <p className="text-gray-700 text-sm leading-relaxed">
                      Access to agricultural experts, community insights, and
                      personalized support for complex farming challenges.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Location Input - After main content */}
        <div className="mb-8">
          <LocationInput onLocationSelect={setLocation} />
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
