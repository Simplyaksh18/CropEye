import React from "react";
import { useNavigate, useLocation } from "react-router-dom";
import ModuleCalculationCard from "./ModuleCalculationCard";

export const Footer: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const handleServiceClick = (path: string) => {
    navigate(path);
  };

  // Map routes to their background colors
  const getFooterColor = () => {
    switch (location.pathname) {
      case "/ndvi":
        return "bg-linear-to-br from-green-50 to-amber-50"; // NDVI: Green for vegetation
      case "/water":
        return "bg-linear-to-br from-blue-50 to-cyan-50"; // Water: Blue for irrigation
      case "/pests":
        return "bg-linear-to-br from-red-200 to-orange-300"; // Pests: Red/Orange for threats
      case "/soil":
        return "bg-linear-to-br from-amber-50 to-yellow-50"; // Soil: Brown/Earth
      case "/crops":
        return "bg-linear-to-br from-lime-100 to-yellow-100"; // Crops: Green/Gold
      case "/weather":
        return "bg-linear-to-br from-blue-200 to-indigo-300"; // Weather: Sky blue
      default:
        return "bg-linear-to-br from-green-100 to-amber-100"; // Dashboard: Default green-amber
    }
  };

  return (
    <footer className={`${getFooterColor()} text-gray-900 py-12 relative`}>
      {/* Module Calculation Card - Always visible */}
      <div className="mb-8">
        <ModuleCalculationCard
          title="How Our Agricultural Intelligence Works"
          description="CropEye's AI platform integrates satellite imagery, weather data, soil sensors, and machine learning algorithms to provide comprehensive farm management insights. Our system analyzes real-time environmental factors including NDVI vegetation indices, precipitation patterns, soil moisture levels, and historical yield data to deliver actionable recommendations. The platform uses advanced predictive analytics to forecast crop performance, optimize resource allocation, and prevent potential issues before they impact yields."
        />
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Company Info */}
          <div className="col-span-1 md:col-span-2">
            <h3 className="text-2xl font-bold text-green-400 mb-4">CropEye</h3>
            <p className="text-gray-700 mb-4 leading-relaxed">
              Revolutionizing agriculture through AI-powered insights, satellite
              monitoring, and data-driven farming solutions. Empowering farmers
              with cutting-edge technology for sustainable and profitable
              agriculture.
            </p>
            <div className="flex space-x-4">
              <a
                href="#"
                className="text-gray-600 hover:text-green-600 transition-colors"
              >
                <span className="sr-only">CropEye</span>
                🌾
              </a>
              <a
                href="#"
                className="text-gray-600 hover:text-green-600 transition-colors"
              >
                <span className="sr-only">Satellite</span>
                🛰️
              </a>
              <a
                href="#"
                className="text-gray-600 hover:text-green-600 transition-colors"
              >
                <span className="sr-only">Weather</span>
                🌤️
              </a>
              <a
                href="#"
                className="text-gray-600 hover:text-green-600 transition-colors"
              >
                <span className="sr-only">Agriculture</span>
                🏞️
              </a>
            </div>
          </div>

          {/* Services */}
          <div>
            <h4 className="text-lg font-semibold mb-4">Services</h4>
            <ul className="space-y-2">
              <li>
                <button
                  onClick={() => handleServiceClick("/ndvi")}
                  className="text-gray-700 hover:text-green-600 transition-colors text-left"
                >
                  NDVI Vegetation Health
                </button>
              </li>
              <li>
                <button
                  onClick={() => handleServiceClick("/weather")}
                  className="text-gray-700 hover:text-green-600 transition-colors text-left"
                >
                  Weather Intelligence
                </button>
              </li>
              <li>
                <button
                  onClick={() => handleServiceClick("/soil")}
                  className="text-gray-700 hover:text-green-600 transition-colors text-left"
                >
                  Soil Analysis
                </button>
              </li>
              <li>
                <button
                  onClick={() => handleServiceClick("/water")}
                  className="text-gray-700 hover:text-green-600 transition-colors text-left"
                >
                  Water Optimization
                </button>
              </li>
              <li>
                <button
                  onClick={() => handleServiceClick("/crops")}
                  className="text-gray-700 hover:text-green-600 transition-colors text-left"
                >
                  Crop Recommendations
                </button>
              </li>
              <li>
                <button
                  onClick={() => handleServiceClick("/pests")}
                  className="text-gray-700 hover:text-green-600 transition-colors text-left"
                >
                  Pest Detection
                </button>
              </li>
            </ul>
          </div>

          {/* Support */}
          <div>
            <h4 className="text-lg font-semibold mb-4">Support</h4>
            <ul className="space-y-2">
              <li>
                <a
                  href="#"
                  className="text-gray-700 hover:text-green-600 transition-colors"
                >
                  Help Center
                </a>
              </li>
              <li>
                <a
                  href="#"
                  className="text-gray-700 hover:text-green-600 transition-colors"
                >
                  Documentation
                </a>
              </li>
              <li>
                <a
                  href="#"
                  className="text-gray-700 hover:text-green-600 transition-colors"
                >
                  API Reference
                </a>
              </li>
              <li>
                <a
                  href="#"
                  className="text-gray-700 hover:text-green-600 transition-colors"
                >
                  Contact Us
                </a>
              </li>
              <li>
                <a
                  href="#"
                  className="text-gray-700 hover:text-green-600 transition-colors"
                >
                  Privacy Policy
                </a>
              </li>
              <li>
                <a
                  href="#"
                  className="text-gray-700 hover:text-green-600 transition-colors"
                >
                  Terms of Service
                </a>
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t border-gray-300 mt-8 pt-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <p className="text-gray-600 text-sm">
              © 2025 CropEye. All rights reserved. Empowering farmers worldwide.
            </p>
            <div className="flex space-x-6 mt-4 md:mt-0">
              <a
                href="#"
                className="text-gray-600 hover:text-green-600 text-sm transition-colors"
              >
                Privacy
              </a>
              <a
                href="#"
                className="text-gray-600 hover:text-green-600 text-sm transition-colors"
              >
                Terms
              </a>
              <a
                href="#"
                className="text-gray-600 hover:text-green-600 text-sm transition-colors"
              >
                Cookies
              </a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
