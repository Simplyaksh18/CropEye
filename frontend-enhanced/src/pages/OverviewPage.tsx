// src/pages/OverviewPage.tsx
import React from "react";
import { useLocation } from "../hooks/useLocation";
import { useNavigate } from "react-router-dom";
import { ScrollFloat } from "../components/animations/ScrollFloat";
import { AnimatedMetricCard } from "../components/ui/AnimatedMetricCard";
import {
  Leaf,
  Cloud,
  Droplets,
  TrendingUp,
  AlertCircle,
  CheckCircle,
  Wheat,
  Bug,
} from "lucide-react";
import { motion } from "framer-motion";

const OverviewPage: React.FC = () => {
  const { analysisData, loading } = useLocation();
  const navigate = useNavigate();

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-light dark:border-primary-dark"></div>
      </div>
    );
  }

  if (!analysisData) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] text-center p-6">
        <Leaf className="w-24 h-24 text-gray-400 dark:text-gray-600 mb-6" />
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
          No Analysis Data
        </h2>
        <p className="text-gray-600 dark:text-gray-400 max-w-md">
          Please analyze a location to see your farm overview.
        </p>
      </div>
    );
  }

  const ndviValue = analysisData?.ndvi?.mean || 0;
  const vegetationCoverage =
    analysisData?.vegetation_percentage ||
    analysisData?.vegetation_coverage ||
    0;
  const weatherSummary = analysisData?.weather_forecast?.summary || "No data";
  const topCrop = analysisData?.crop_recommendations?.[0] ?? null;
  const pestCount = analysisData?.pest_alerts?.length || 0;

  const getHealthStatus = () => {
    if (ndviValue > 0.6)
      return { text: "Excellent", color: "success", icon: CheckCircle };
    if (ndviValue > 0.4)
      return { text: "Good", color: "warning", icon: CheckCircle };
    return { text: "Needs Attention", color: "error", icon: AlertCircle };
  };

  const healthStatus = getHealthStatus();

  return (
    <div className="space-y-8 p-6">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
          Farm Overview
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Complete analysis of your agricultural data
        </p>
      </motion.div>

      {/* Health Status Banner */}
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 0.2 }}
        className={`
          p-6 rounded-2xl border-2 flex items-center gap-4
          ${
            healthStatus.color === "success" &&
            "bg-green-500/10 border-green-500"
          }
          ${
            healthStatus.color === "warning" &&
            "bg-yellow-500/10 border-yellow-500"
          }
          ${healthStatus.color === "error" && "bg-red-500/10 border-red-500"}
        `}
      >
        <healthStatus.icon className="w-12 h-12" />
        <div>
          <h2 className="text-2xl font-bold">
            Overall Farm Health: {healthStatus.text}
          </h2>
          <p className="text-sm opacity-80">
            Based on NDVI, soil conditions, and weather patterns
          </p>
        </div>
      </motion.div>

      {/* Key Metrics Grid */}
      <ScrollFloat offset={30}>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <AnimatedMetricCard
            icon={Leaf}
            title="NDVI Score"
            value={ndviValue.toFixed(3)}
            status={
              ndviValue > 0.6
                ? "success"
                : ndviValue > 0.4
                ? "warning"
                : "error"
            }
            description="Vegetation health index"
          />

          <AnimatedMetricCard
            icon={TrendingUp}
            title="Vegetation Coverage"
            value={vegetationCoverage}
            unit="%"
            status="success"
            description="Green biomass coverage"
          />

          <AnimatedMetricCard
            icon={Cloud}
            title="Weather"
            value={
              analysisData?.weather_forecast?.days?.[0]?.temperature?.avg || 0
            }
            unit="°C"
            status="info"
            description={weatherSummary}
          />

          <AnimatedMetricCard
            icon={Droplets}
            title="Soil Moisture"
            value={analysisData?.soil_fertility?.moisture_level || 0}
            unit="%"
            status="info"
            description="Current moisture level"
          />
        </div>
      </ScrollFloat>

      {/* Quick Action Cards */}
      <ScrollFloat offset={40}>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <ActionCard
            icon={<Leaf className="w-8 h-8 text-green-500" />}
            title="NDVI Analysis"
            description="View detailed vegetation health trends"
            onClick={() => navigate("/ndvi")}
            color="green"
          />
          <ActionCard
            icon={<Droplets className="w-8 h-8 text-blue-500" />}
            title="Water Management"
            description="Check irrigation recommendations"
            onClick={() => navigate("/water")}
            color="blue"
          />
          <ActionCard
            icon={<Wheat className="w-8 h-8 text-yellow-500" />}
            title="Crop Recommendations"
            description={`${
              analysisData?.crop_recommendations?.length || 0
            } suitable crops`}
            onClick={() => navigate("/crops")}
            color="yellow"
          />
        </div>
      </ScrollFloat>

      {/* Alerts */}
      {pestCount > 0 && (
        <ScrollFloat offset={50}>
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="bg-red-500/10 border-2 border-red-500 rounded-2xl p-6 flex items-start gap-4"
          >
            <Bug className="w-8 h-8 text-red-500 flex-shrink-0" />
            <div>
              <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-2">
                Pest Alert
              </h3>
              <p className="text-gray-700 dark:text-gray-300 mb-3">
                {pestCount} pest issue(s) detected that require your attention.
              </p>
              <button
                onClick={() => navigate("/pests")}
                className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors"
              >
                View Details
              </button>
            </div>
          </motion.div>
        </ScrollFloat>
      )}

      {/* Top Crop Recommendation */}
      {topCrop && (
        <ScrollFloat offset={60}>
          <div className="bg-gradient-to-br from-green-500/10 to-emerald-500/10 rounded-2xl p-6 border border-green-500/30">
            <h3 className="text-xl font-bold mb-4 text-gray-900 dark:text-white">
              Top Crop Recommendation
            </h3>

            <div className="flex items-start gap-4">
              <div className="flex-shrink-0 w-16 h-16 bg-green-500 rounded-xl flex items-center justify-center text-white text-2xl font-bold">
                {topCrop.suitabilityScore}%
              </div>

              <div className="flex-1">
                <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                  {topCrop.crop}
                </h4>
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
                  {topCrop.reason}
                </p>
                <button
                  onClick={() => navigate("/crops")}
                  className="text-sm text-green-600 dark:text-green-400 hover:underline"
                >
                  View all recommendations →
                </button>
              </div>
            </div>
          </div>
        </ScrollFloat>
      )}
    </div>
  );
};

const ActionCard: React.FC<{
  icon: React.ReactNode;
  title: string;
  description: string;
  onClick: () => void;
  color: "green" | "blue" | "yellow";
}> = ({ icon, title, description, onClick, color }) => {
  const colorClasses = {
    green: "hover:bg-green-500/10 border-green-500/30",
    blue: "hover:bg-blue-500/10 border-blue-500/30",
    yellow: "hover:bg-yellow-500/10 border-yellow-500/30",
  };

  return (
    <motion.div
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      onClick={onClick}
      className={`cursor-pointer bg-white dark:bg-gray-800 rounded-xl border-2 ${colorClasses[color]} p-6 transition-all`}
    >
      <div className="mb-3">{icon}</div>
      <h4 className="text-lg font-bold text-gray-900 dark:text-white mb-2">
        {title}
      </h4>
      <p className="text-sm text-gray-600 dark:text-gray-400">{description}</p>
    </motion.div>
  );
};

export default OverviewPage;
