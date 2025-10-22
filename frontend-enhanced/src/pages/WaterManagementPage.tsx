// src/pages/WaterManagementPage.tsx
import React, { useState, useEffect } from "react";
import { Droplets, AlertTriangle, TrendingUp, Calendar } from "lucide-react";
import { useLocation } from "../hooks/useLocation";
import { ScrollFloat } from "../components/animations/ScrollFloat";
import { AnimatedMetricCard } from "../components/ui/AnimatedMetricCard";
import { LoadingSkeleton } from "../components/ui/LoadingSkeleton";
import api from "../api/api-client";
import { motion } from "framer-motion";

interface WaterManagementData {
  et0_mm_day: number;
  etc_mm_day: number;
  irrigation: {
    net_irrigation_mm: number;
    gross_irrigation_mm: number;
    irrigation_interval_days: number;
    etc_mm_day: number;
    effective_rainfall_mm: number;
    water_deficit_mm: number;
    recommendation: string;
  };
  water_stress_index: number;
  crop_type: string;
  growth_stage: string;
  timestamp: string;
}

const WaterManagementPage: React.FC = () => {
  const { userLocation, loading: contextLoading } = useLocation();
  const [waterData, setWaterData] = useState<WaterManagementData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [cropType, setCropType] = useState("wheat");
  const [growthStage, setGrowthStage] = useState("mid");

  const fetchWaterManagement = React.useCallback(async () => {
    if (!userLocation) {
      setError("No location selected. Please analyze a location first.");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await api.post(
        "http://localhost:5005/api/water/irrigation/integrated",
        {
          latitude: userLocation.lat,
          longitude: userLocation.lng,
          crop_type: cropType,
          growth_stage: growthStage,
        }
      );

      if (response.data.success && response.data.schedule) {
        setWaterData({
          ...response.data.schedule,
          crop_type: cropType,
          growth_stage: growthStage,
        });
      } else {
        setError("Failed to fetch water management data");
      }
    } catch (err) {
      const e = err as {
        response?: { data?: { error?: string } };
        message?: string;
      };
      setError(
        e.response?.data?.error || e.message || "Failed to fetch water data"
      );
    } finally {
      setLoading(false);
    }
  }, [userLocation, cropType, growthStage]);

  useEffect(() => {
    if (userLocation) {
      fetchWaterManagement();
    }
  }, [userLocation, fetchWaterManagement]);

  if (contextLoading || loading) {
    return <LoadingSkeleton variant="card" count={4} />;
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] text-center">
        <AlertTriangle className="w-24 h-24 text-orange-500 mb-6" />
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
          Water Management Data Unavailable
        </h2>
        <p className="text-gray-600 dark:text-gray-400 max-w-md mb-4">
          {error}
        </p>
        <button
          onClick={fetchWaterManagement}
          className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
        >
          Retry
        </button>
      </div>
    );
  }

  if (!waterData) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] text-center">
        <Droplets className="w-24 h-24 text-gray-400 mb-6" />
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
          No Water Management Data
        </h2>
        <p className="text-gray-600 dark:text-gray-400 max-w-md">
          Analyze a location to see irrigation recommendations.
        </p>
      </div>
    );
  }

  type Status = "success" | "warning" | "error" | "info";

  const getStressLevel = (index: number): { text: string; color: Status } => {
    if (index < 0.3) return { text: "Low", color: "success" };
    if (index < 0.6) return { text: "Moderate", color: "warning" };
    return { text: "High", color: "error" };
  };

  const stressLevel = getStressLevel(waterData.water_stress_index);

  return (
    <div className="space-y-8">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
          Water Management
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Irrigation scheduling and water stress analysis
        </p>
      </motion.div>

      {/* Crop Selection */}
      <ScrollFloat>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Crop Type
            </label>
            <select
              value={cropType}
              onChange={(e) => setCropType(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
            >
              <option value="wheat">Wheat</option>
              <option value="rice">Rice</option>
              <option value="maize">Maize</option>
              <option value="cotton">Cotton</option>
              <option value="sugarcane">Sugarcane</option>
              <option value="sorghum">Sorghum</option>
              <option value="millets">Millets</option>
              <option value="sunflower">Sunflower</option>
              <option value="groundnut">Groundnut</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Growth Stage
            </label>
            <select
              value={growthStage}
              onChange={(e) => setGrowthStage(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
            >
              <option value="initial">Initial</option>
              <option value="mid">Mid</option>
              <option value="late">Late</option>
            </select>
          </div>
        </div>
      </ScrollFloat>

      {/* Key Metrics */}
      <ScrollFloat offset={30}>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <AnimatedMetricCard
            icon={Droplets}
            title="Irrigation Required"
            value={waterData.irrigation.gross_irrigation_mm}
            unit="mm"
            status={
              waterData.irrigation.gross_irrigation_mm > 40
                ? "warning"
                : "success"
            }
            description="Gross irrigation amount"
          />

          <AnimatedMetricCard
            icon={Calendar}
            title="Next Irrigation"
            value={waterData.irrigation.irrigation_interval_days}
            unit="days"
            status="info"
            description="Recommended interval"
          />

          <AnimatedMetricCard
            icon={TrendingUp}
            title="Water Stress"
            value={waterData.water_stress_index}
            status={stressLevel.color}
            description={`${stressLevel.text} stress level`}
          />

          <AnimatedMetricCard
            icon={Droplets}
            title="ET₀"
            value={waterData.et0_mm_day}
            unit="mm/day"
            status="info"
            description="Reference evapotranspiration"
          />
        </div>
      </ScrollFloat>

      {/* Detailed Analysis */}
      <ScrollFloat offset={40}>
        <div className="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-6">
          <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
            Irrigation Schedule Details
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h4 className="font-semibold text-gray-700 dark:text-gray-300 mb-3">
                Water Requirements
              </h4>
              <div className="space-y-2">
                <DataRow
                  label="Net Irrigation"
                  value={`${waterData.irrigation.net_irrigation_mm} mm`}
                />
                <DataRow
                  label="Gross Irrigation"
                  value={`${waterData.irrigation.gross_irrigation_mm} mm`}
                />
                <DataRow
                  label="Crop ETc"
                  value={`${waterData.irrigation.etc_mm_day} mm/day`}
                />
                <DataRow
                  label="Water Deficit"
                  value={`${waterData.irrigation.water_deficit_mm} mm`}
                />
              </div>
            </div>

            <div>
              <h4 className="font-semibold text-gray-700 dark:text-gray-300 mb-3">
                Additional Info
              </h4>
              <div className="space-y-2">
                <DataRow
                  label="Effective Rainfall"
                  value={`${waterData.irrigation.effective_rainfall_mm} mm`}
                />
                <DataRow label="Crop Type" value={waterData.crop_type} />
                <DataRow label="Growth Stage" value={waterData.growth_stage} />
                <DataRow
                  label="Irrigation Interval"
                  value={`${waterData.irrigation.irrigation_interval_days} days`}
                />
              </div>
            </div>
          </div>
        </div>
      </ScrollFloat>

      {/* Recommendation */}
      <ScrollFloat offset={50}>
        <div
          className={`
          rounded-2xl p-6 border-2
          ${
            waterData.irrigation.gross_irrigation_mm < 20
              ? "bg-green-500/10 border-green-500"
              : waterData.irrigation.gross_irrigation_mm < 40
              ? "bg-yellow-500/10 border-yellow-500"
              : "bg-red-500/10 border-red-500"
          }
        `}
        >
          <div className="flex items-start gap-4">
            <Droplets className="w-8 h-8 flex-shrink-0" />
            <div>
              <h4 className="text-lg font-bold text-gray-900 dark:text-white mb-2">
                Irrigation Recommendation
              </h4>
              <p className="text-gray-700 dark:text-gray-300">
                {waterData.irrigation.recommendation}
              </p>
            </div>
          </div>
        </div>
      </ScrollFloat>
    </div>
  );
};

const DataRow: React.FC<{ label: string; value: string | number }> = ({
  label,
  value,
}) => (
  <div className="flex justify-between items-center py-1 border-b border-gray-200 dark:border-gray-700">
    <span className="text-sm text-gray-600 dark:text-gray-400">{label}:</span>
    <span className="text-sm font-semibold text-gray-900 dark:text-white">
      {value}
    </span>
  </div>
);

export default WaterManagementPage;
