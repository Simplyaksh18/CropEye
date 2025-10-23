import React, { useMemo } from "react";
import {
  NavLink,
  Outlet,
  useLocation as useRouterLocation,
} from "react-router-dom";
import { AnimatePresence, motion } from "framer-motion";
import {
  Sprout,
  ThermometerSun,
  Leaf,
  Wheat,
  Bug,
  Sparkles,
  MoonStar,
  SunMedium,
  LogOut,
} from "lucide-react";
import { useTheme } from "../../context/ThemeContext";
import { AnimatedThemeToggler } from "../UI/AnimatedThemeToggler";
import { useAuth } from "../../context/AuthContext";
import LocationInput from "../LocationInput/LocationInput";
import { useLocation as useAnalysisLocation } from "../../context/LocationContext";
import Footer from "./Footer";
import "./MainLayout.css";
import "../Pages/Pages.css";
import StaggeredMenu from "./StaggeredMenu";

const navItems = [
  { path: "overview", label: "Overview", icon: <Sprout /> },
  { path: "weather", label: "Weather", icon: <ThermometerSun /> },
  { path: "ndvi", label: "NDVI", icon: <Leaf /> },
  { path: "crops", label: "Crops", icon: <Wheat /> },
  { path: "pests", label: "Pests", icon: <Bug /> },
  { path: "insights", label: "Insights", icon: <Sparkles /> },
];

const pageMotion = {
  initial: { opacity: 0, y: 24 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -24 },
};

const MainLayout = () => {
  const routerLocation = useRouterLocation();
  const { theme, toggleTheme } = useTheme();
  const { user, logout } = useAuth();
  const { analysisData, loading } = useAnalysisLocation();

  const welcomeTitle = useMemo(() => {
    if (!user) return "Farmer";
    const firstName = user.firstName || user.email?.split("@")[0];
    return firstName
      ? firstName.charAt(0).toUpperCase() + firstName.slice(1)
      : "Farmer";
  }, [user]);

  return (
    <div className={`main-layout theme-${theme}`}>
      <div className="layout-aurora" />
      <header className="layout-header">
        <div className="layout-brand">
          <span className="emoji-logo" role="img" aria-label="CropEye sapling">
            🌱
          </span>
          <div>
            <h1>CropEye</h1>
            <p>Real-time agronomy intelligence console</p>
          </div>
        </div>
        <div className="layout-actions">
          <div className="welcome-copy">
            <span>Namaste,</span>
            <strong>{welcomeTitle}</strong>
            {loading && <span className="loading-chip">Analyzing...</span>}
          </div>
          <AnimatedThemeToggler />
          <button
            className="logout-button"
            onClick={logout}
            aria-label="Logout"
          >
            <LogOut size={18} />
          </button>
        </div>
      </header>

      <nav className="layout-nav">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              isActive ? "nav-item active" : "nav-item"
            }
          >
            <span className="icon">{item.icon}</span>
            <span>{item.label}</span>
          </NavLink>
        ))}
      </nav>

      <div className="layout-columns">
        {user && <StaggeredMenu isFixed={false} items={[]} socialItems={[]} />}
        <aside className="layout-sidebar">
          <LocationInput />
          {analysisData && (
            <div className="analysis-snippet">
              <h3>Field Pulse</h3>
              <p>
                NDVI status:{" "}
                <strong>
                  {analysisData?.ndvi_report?.status ||
                    analysisData?.health_analysis?.status ||
                    "N/A"}
                </strong>
              </p>
              <p>
                Vegetation cover:{" "}
                <strong>
                  {analysisData?.vegetation_percentage ??
                    analysisData?.vegetation_coverage ??
                    analysisData?.ndvi_analysis?.vegetation_percentage ??
                    "-"}
                  %
                </strong>
              </p>
            </div>
          )}
        </aside>
        <main className="layout-main" aria-live="polite">
          <AnimatePresence mode="wait">
            <motion.div
              key={routerLocation.pathname}
              initial={pageMotion.initial}
              animate={pageMotion.animate}
              exit={pageMotion.exit}
              transition={{ duration: 0.35, ease: "easeOut" }}
            >
              <Outlet />
            </motion.div>
          </AnimatePresence>
        </main>
      </div>
      <Footer />
    </div>
  );
};

export default MainLayout;
