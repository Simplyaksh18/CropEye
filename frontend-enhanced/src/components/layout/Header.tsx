// src/components/layout/Header.tsx
import React from "react";
import { useNavigate } from "react-router-dom";
import {
  Home,
  Leaf,
  Cloud,
  Wheat,
  Bug,
  Droplets,
  Settings,
  LogOut,
} from "lucide-react";
import { GradientText } from "../animations/GradientText";
import { StarBorder } from "../animations/StarBorder";
import { StaggeredMenu } from "../ui/StaggeredMenu";
import { useAuth } from "../../context/AuthContext";
import { useTheme } from "../../context/ThemeContext";

const Header: React.FC = () => {
  const navigate = useNavigate();
  const { logout, user } = useAuth();
  const { toggleTheme, theme } = useTheme();

  const handleLogout = async () => {
    await logout();
    navigate("/login");
  };

  const menuItems = [
    {
      label: "Dashboard",
      onClick: () => navigate("/"),
      icon: <Home size={20} />,
    },
    {
      label: "Overview",
      onClick: () => navigate("/overview"),
      icon: <Leaf size={20} />,
    },
    {
      label: "NDVI Analysis",
      onClick: () => navigate("/ndvi"),
      icon: <Leaf size={20} />,
    },
    {
      label: "Weather",
      onClick: () => navigate("/weather"),
      icon: <Cloud size={20} />,
    },
    {
      label: "Water Management",
      onClick: () => navigate("/water"),
      icon: <Droplets size={20} />,
    },
    {
      label: "Crops",
      onClick: () => navigate("/crops"),
      icon: <Wheat size={20} />,
    },
    {
      label: "Pests",
      onClick: () => navigate("/pests"),
      icon: <Bug size={20} />,
    },
    {
      label: "Soil",
      onClick: () => navigate("/soil"),
      icon: <Droplets size={20} />,
    },
    {
      label: `Theme: ${theme}`,
      onClick: toggleTheme,
      icon: <Settings size={20} />,
    },
    { label: "Logout", onClick: handleLogout, icon: <LogOut size={20} /> },
  ];

  return (
    <header className="sticky top-0 z-50 backdrop-blur-lg bg-white/80 dark:bg-gray-900/80 border-b border-gray-200 dark:border-gray-700">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <StarBorder className="w-16 h-16">
              <div className="w-full h-full rounded-full bg-gradient-to-br from-green-400 to-blue-500 flex items-center justify-center">
                <Leaf className="w-8 h-8 text-white" />
              </div>
            </StarBorder>

            <div>
              <GradientText text="CropEye" className="text-2xl md:text-3xl" />
              <p className="text-xs text-gray-600 dark:text-gray-400">
                GIS Dashboard
              </p>
            </div>
          </div>

          <div className="flex items-center gap-4">
            {user && (
              <div className="hidden md:block text-right">
                <p className="text-sm font-semibold">
                  {user.firstName} {user.lastName}
                </p>
                {user.farmName && (
                  <p className="text-xs text-gray-600 dark:text-gray-400">
                    {user.farmName}
                  </p>
                )}
              </div>
            )}
            <StaggeredMenu items={menuItems} />
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
