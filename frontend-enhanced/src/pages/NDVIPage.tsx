import React from "react";
import { useLocation } from "../hooks/useLocation";
import { ScrollFloat } from "../components/animations/ScrollFloat";
import { AnimatedMetricCard } from "../components/ui/AnimatedMetricCard";
import { NDVITrendChart } from "../components/charts/NDVITrendChart";
import { LoadingSkeleton } from "../components/ui/LoadingSkeleton";
import { Leaf, TrendingUp, Activity, AlertCircle } from "lucide-react";
import { motion } from "framer-motion";

const NdviPage: React.FC = () => {
  const { analysisData, loading } = useLocation();

  if (loading) {
    return (
      <div className="space-y-6 p-6">
        <LoadingSkeleton variant="card" count={3} />
        <LoadingSkeleton variant="chart" />
      </div>
    );
  }

  // Transform backend data to match expected format
  const ndvi =
    analysisData?.ndvi_report ||
    (analysisData?.ndvi
      ? {
          latestValue: analysisData.ndvi.mean,
          latestDate: analysisData.analysis_date || new Date().toISOString(),
          status: analysisData.health_analysis?.status || "Unknown",
          trend:
            analysisData.trend_analysis?.summary ||
            analysisData.trend_analysis?.trend ||
            "",
          change:
            analysisData.ndvi.mean && analysisData.ndvi.median
              ? Number(
                  (analysisData.ndvi.mean - analysisData.ndvi.median).toFixed(3)
                )
              : null,
          seasonalAverage: analysisData.ndvi.mean,
          history: Array.isArray(analysisData.ndvi_history)
            ? analysisData.ndvi_history
            : [],
        }
      : null);

  if (!ndvi) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] text-center p-6">
        <Activity className="w-24 h-24 text-gray-400 dark:text-gray-600 mb-6" />
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
          No NDVI Data Available
        </h2>
        <p className="text-gray-600 dark:text-gray-400 max-w-md">
          Analyze a location to see detailed vegetation health metrics and
          trends.
        </p>
      </div>
    );
  }

  const getStatusColor = (
    status: string
  ): "success" | "warning" | "error" | "info" => {
    const statusLower = status?.toLowerCase();
    if (statusLower?.includes("healthy") || statusLower?.includes("excellent"))
      return "success";
    if (statusLower?.includes("moderate") || statusLower?.includes("good"))
      return "warning";
    if (statusLower?.includes("poor") || statusLower?.includes("critical"))
      return "error";
    return "info";
  };

  return (
    <div className="space-y-8 p-6">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
          NDVI Analysis
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Normalized Difference Vegetation Index - Track crop health through
          satellite imagery
        </p>
      </motion.div>

      <ScrollFloat>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <AnimatedMetricCard
            icon={Activity}
            title="Current NDVI"
            value={ndvi.latestValue}
            status={getStatusColor(ndvi.status)}
            description={`Measured on ${new Date(
              ndvi.latestDate
            ).toLocaleDateString()}`}
          />

          <AnimatedMetricCard
            icon={TrendingUp}
            title="Vegetation Coverage"
            value={
              analysisData?.vegetation_percentage ??
              analysisData?.vegetation_coverage ??
              0
            }
            unit="%"
            status="success"
            description="Green biomass coverage area"
          />

          <AnimatedMetricCard
            icon={Leaf}
            title="Seasonal Average"
            value={ndvi.seasonalAverage}
            status="info"
            description="6-pass rolling average"
            trend={
              ndvi.change
                ? {
                    value: (ndvi.change / ndvi.seasonalAverage) * 100,
                    isPositive: ndvi.change > 0,
                  }
                : undefined
            }
          />
        </div>
      </ScrollFloat>

      {ndvi.history && ndvi.history.length > 0 && (
        <ScrollFloat offset={40}>
          <div className="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-6">
            <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
              NDVI Trend Over Time
            </h3>
            <NDVITrendChart data={ndvi.history} />
          </div>
        </ScrollFloat>
      )}

      <ScrollFloat offset={50}>
        <div
          className={`
          rounded-2xl p-6 border-2
          ${
            getStatusColor(ndvi.status) === "success" &&
            "bg-green-500/10 border-green-500"
          }
          ${
            getStatusColor(ndvi.status) === "warning" &&
            "bg-yellow-500/10 border-yellow-500"
          }
          ${
            getStatusColor(ndvi.status) === "error" &&
            "bg-red-500/10 border-red-500"
          }
        `}
        >
          <div className="flex items-start gap-4">
            <div
              className={`
              w-12 h-12 rounded-xl flex items-center justify-center
              ${getStatusColor(ndvi.status) === "success" && "bg-green-500"}
              ${getStatusColor(ndvi.status) === "warning" && "bg-yellow-500"}
              ${getStatusColor(ndvi.status) === "error" && "bg-red-500"}
            `}
            >
              {getStatusColor(ndvi.status) === "error" ? (
                <AlertCircle className="w-6 h-6 text-white" />
              ) : (
                <Leaf className="w-6 h-6 text-white" />
              )}
            </div>

            <div className="flex-1">
              <h4 className="text-lg font-bold text-gray-900 dark:text-white mb-2">
                Current Status: {ndvi.status}
              </h4>
              <p className="text-gray-700 dark:text-gray-300">{ndvi.trend}</p>

              {/* NDVI Interpretation Guide */}
              <div className="mt-4 p-4 bg-gray-50 dark:bg-gray-900 rounded-lg">
                <h5 className="font-semibold text-sm text-gray-900 dark:text-white mb-2">
                  NDVI Value Interpretation:
                </h5>
                <ul className="space-y-1 text-sm text-gray-600 dark:text-gray-400">
                  <li>
                    <span className="text-green-600">0.6 - 1.0:</span> Healthy,
                    dense vegetation
                  </li>
                  <li>
                    <span className="text-yellow-600">0.4 - 0.6:</span> Moderate
                    vegetation, may need attention
                  </li>
                  <li>
                    <span className="text-orange-600">0.2 - 0.4:</span> Sparse
                    vegetation, stress indicators
                  </li>
                  <li>
                    <span className="text-red-600">Below 0.2:</span> Critical,
                    immediate action required
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </ScrollFloat>
    </div>
  );
};

export default NdviPage;
