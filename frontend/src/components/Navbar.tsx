import React from "react";
import { Link, useLocation } from "react-router-dom";
import { useLocation as useCoordinates } from "../hooks/useLocation";

interface NavbarProps {
  onLogout?: () => void;
}

export default function Navbar({ onLogout }: NavbarProps) {
  const location = useLocation();
  const { location: coordinates } = useCoordinates();

  const navItems = [
    { path: "/dashboard", label: "Dashboard" },
    { path: "/crops", label: "Crops" },
    { path: "/ndvi", label: "NDVI" },
    { path: "/weather", label: "Weather" },
    { path: "/water", label: "Water" },
    { path: "/soil", label: "Soil" },
    { path: "/pests", label: "Pests" },
  ];

  const getGreeting = () => {
    const hour = new Date().getHours();
    const userName = localStorage.getItem("user")
      ? JSON.parse(localStorage.getItem("user")!).name
      : "User";

    if (hour < 12) return `Good Morning, ${userName}`;
    if (hour < 18) return `Good Afternoon, ${userName}`;
    return `Good Evening, ${userName}`;
  };

  // Get navbar background and text colors based on current route
  const getNavbarColors = () => {
    switch (location.pathname) {
      case "/ndvi":
        return {
          bg: "bg-green-100",
          textActive: "text-green-700",
          bgActive: "bg-green-200",
          hover: "hover:text-green-700 hover:bg-green-50",
        };
      case "/water":
        return {
          bg: "bg-blue-100",
          textActive: "text-blue-700",
          bgActive: "bg-blue-200",
          hover: "hover:text-blue-700 hover:bg-blue-50",
        };
      case "/pests":
        return {
          bg: "bg-red-200",
          textActive: "text-red-700",
          bgActive: "bg-red-300",
          hover: "hover:text-red-700 hover:bg-red-100",
        };
      case "/soil":
        return {
          bg: "bg-amber-100",
          textActive: "text-amber-700",
          bgActive: "bg-amber-200",
          hover: "hover:text-amber-700 hover:bg-amber-50",
        };
      case "/crops":
        return {
          bg: "bg-lime-100",
          textActive: "text-lime-700",
          bgActive: "bg-lime-200",
          hover: "hover:text-lime-700 hover:bg-lime-50",
        };
      case "/weather":
        return {
          bg: "bg-blue-200",
          textActive: "text-indigo-700",
          bgActive: "bg-indigo-300",
          hover: "hover:text-indigo-700 hover:bg-blue-100",
        };
      default:
        return {
          bg: "bg-gray-100",
          textActive: "text-green-700",
          bgActive: "bg-green-100",
          hover: "hover:text-green-600 hover:bg-gray-100",
        };
    }
  };

  const colors = getNavbarColors();

  return (
    <nav className={`${colors.bg} shadow-sm border-b border-gray-200`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/dashboard" className="flex items-center">
            <img
              src="/cropeye-logo.svg"
              alt="CropEye Logo"
              className="h-8 w-auto mr-3"
            />
            <span className="text-xl font-bold text-gray-900">CropEye</span>
          </Link>

          {/* Navigation Links */}
          <div className="hidden md:flex space-x-8">
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  location.pathname === item.path
                    ? `${colors.bgActive} ${colors.textActive}`
                    : `text-gray-700 ${colors.hover}`
                }`}
              >
                {item.label}
              </Link>
            ))}
          </div>

          {/* User Info and Logout */}
          <div className="flex items-center space-x-4">
            <span className="text-gray-700 font-medium hidden lg:block">
              {getGreeting()}
            </span>
            {coordinates?.lat && coordinates?.lng && (
              <span className="text-sm text-gray-500 hidden md:block">
                📍 {coordinates.lat.toFixed(2)}, {coordinates.lng.toFixed(2)}
              </span>
            )}
            <button
              onClick={onLogout}
              className="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 font-medium transition-colors"
            >
              Logout
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        <div className="md:hidden pb-3">
          <div className="flex space-x-4 overflow-x-auto">
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={`px-3 py-2 rounded-md text-sm font-medium whitespace-nowrap transition-colors ${
                  location.pathname === item.path
                    ? `${colors.bgActive} ${colors.textActive}`
                    : `text-gray-700 ${colors.hover}`
                }`}
              >
                {item.label}
              </Link>
            ))}
          </div>
        </div>
      </div>
    </nav>
  );
}
