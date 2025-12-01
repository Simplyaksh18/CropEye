import React from "react";
import {
  Link,
  useLocation as useRouteLocation,
  useNavigate,
} from "react-router-dom";
import { useLocation as useAppLocation } from "../hooks/useLocation";

interface NavbarProps {
  onLogout: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({ onLogout }) => {
  const routeLocation = useRouteLocation();
  const navigate = useNavigate();
  const { location: appLocation } = useAppLocation();

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

  return (
    <nav className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center h-16">
          {/* Logo */}
          <Link to="/dashboard" className="flex items-center">
            <div className="w-8 h-8 bg-green-600 rounded-lg flex items-center justify-center mr-3">
              <span className="text-white font-bold text-sm">C</span>
            </div>
            <span className="text-xl font-bold text-gray-900">CropEye</span>
          </Link>

          {/* Navigation Links (centered on md+) */}
          <div className="hidden md:flex md:flex-1 md:justify-center space-x-8">
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  routeLocation.pathname === item.path
                    ? "bg-green-100 text-green-700"
                    : "text-gray-700 hover:text-green-600 hover:bg-gray-100"
                }`}
              >
                {item.label}
              </Link>
            ))}
          </div>
          {/* Right-side controls */}
          <div className="ml-auto flex items-center space-x-3">
            <span className="hidden sm:inline text-sm text-gray-700 font-medium">
              {getGreeting()}
            </span>

            {appLocation && (
              <button
                onClick={() => navigate("/dashboard")}
                title="Current location — click to change"
                className="bg-gray-100 text-gray-800 px-2 py-1 rounded-full text-sm border border-gray-200 hover:bg-gray-50 flex items-center gap-2"
              >
                <span className="text-xs">📍</span>
                <span className="text-xs">
                  {appLocation.lat.toFixed(3)}, {appLocation.lng.toFixed(3)}
                </span>
              </button>
            )}

            <button
              onClick={onLogout}
              className="bg-red-600 text-white px-3 py-1 rounded-md hover:bg-red-700 font-medium transition-colors text-sm"
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
                  routeLocation.pathname === item.path
                    ? "bg-green-100 text-green-700"
                    : "text-gray-700 hover:text-green-600 hover:bg-gray-100"
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
};

export default Navbar;
