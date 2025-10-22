// src/pages/PestsPage.tsx
import React from "react";
import { Bug, AlertCircle } from "lucide-react";
import { useLocation } from "../hooks/useLocation";
import type { PestAlert } from "../types/analysis.types";
import { ScrollFloat } from "../components/animations/ScrollFloat";

const PestsPage: React.FC = () => {
  const { analysisData, loading } = useLocation();
  const pestAlerts: PestAlert[] = analysisData?.pest_alerts || [];

  if (loading) {
    return <div>Loading...</div>;
  }

  if (pestAlerts.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] text-center">
        <Bug className="w-24 h-24 text-gray-400 mb-6" />
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
          No Pest Alerts
        </h2>
        <p className="text-gray-600 dark:text-gray-400">
          Your location is currently pest-free!
        </p>
      </div>
    );
  }

  const getRiskColor = (level: string) => {
    switch (level.toLowerCase()) {
      case "high":
      case "critical":
        return "from-red-500/20 to-rose-500/20 border-red-500";
      case "medium":
        return "from-yellow-500/20 to-orange-500/20 border-yellow-500";
      default:
        return "from-green-500/20 to-emerald-500/20 border-green-500";
    }
  };

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
          Pest & Disease Management
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Early detection and prevention strategies
        </p>
      </div>

      <ScrollFloat>
        <div className="space-y-4">
          {pestAlerts.map((alert, index) => (
            <div
              key={index}
              className={`bg-gradient-to-br ${getRiskColor(
                alert.risk_level
              )} rounded-2xl p-6 border-2`}
            >
              <div className="flex items-start gap-4">
                <AlertCircle className="w-8 h-8 flex-shrink-0 mt-1" />
                <div className="flex-1">
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="text-xl font-bold text-gray-900 dark:text-white">
                      {alert.pest_name}
                    </h3>
                    <span
                      className={`px-3 py-1 rounded-full text-sm font-semibold ${
                        alert.risk_level === "High" ||
                        alert.risk_level === "Critical"
                          ? "bg-red-500 text-white"
                          : alert.risk_level === "Medium"
                          ? "bg-yellow-500 text-white"
                          : "bg-green-500 text-white"
                      }`}
                    >
                      {alert.risk_level} Risk
                    </span>
                  </div>

                  <p className="text-gray-700 dark:text-gray-300 mb-4">
                    {alert.description}
                  </p>

                  <div className="bg-white/50 dark:bg-black/20 rounded-lg p-4">
                    <h4 className="font-semibold text-sm mb-2 text-gray-900 dark:text-white">
                      Prevention Measures:
                    </h4>
                    <ul className="space-y-1">
                      {alert.prevention_measures.map((measure, idx) => (
                        <li
                          key={idx}
                          className="text-sm text-gray-700 dark:text-gray-300 flex items-start"
                        >
                          <span className="text-green-500 mr-2">•</span>
                          {measure}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </ScrollFloat>
    </div>
  );
};

export default PestsPage;
