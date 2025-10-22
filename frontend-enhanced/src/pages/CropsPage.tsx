// src/pages/CropsPage.tsx
import React from "react";
import { Wheat } from "lucide-react";
import { useLocation } from "../hooks/useLocation";
import { ScrollFloat } from "../components/animations/ScrollFloat";
import { CropSuitabilityChart } from "../components/charts/CropSuitabilityChart";
import { LoadingSkeleton } from "../components/ui/LoadingSkeleton";

const CropsPage: React.FC = () => {
  const { analysisData, loading } = useLocation();
  const recommendations = analysisData?.crop_recommendations || [];

  if (loading) {
    return <LoadingSkeleton variant="card" count={3} />;
  }

  if (recommendations.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] text-center">
        <Wheat className="w-24 h-24 text-gray-400 dark:text-gray-600 mb-6" />
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
          No Crop Recommendations Available
        </h2>
        <p className="text-gray-600 dark:text-gray-400 max-w-md">
          Analyze a location to receive AI-powered crop recommendations.
        </p>
      </div>
    );
  }

  const chartData = recommendations.map((rec) => ({
    crop: rec.crop,
    suitabilityScore: rec.suitabilityScore,
  }));

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
          Crop Recommendations
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          AI-powered crop suitability analysis for your location
        </p>
      </div>

      <ScrollFloat>
        <div className="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-6">
          <h3 className="text-xl font-semibold mb-4 text-gray-900 dark:text-white">
            Crop Suitability Scores
          </h3>
          <CropSuitabilityChart data={chartData} />
        </div>
      </ScrollFloat>

      <ScrollFloat offset={40}>
        <div className="space-y-4">
          {recommendations.map((rec, index) => (
            <div
              key={index}
              className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-6"
            >
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h4 className="text-xl font-bold text-gray-900 dark:text-white">
                    {rec.crop}
                  </h4>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    Expected success: {rec.expectedHarvestSuccessRate}
                  </p>
                </div>
                <div className="text-right">
                  <div
                    className={`text-2xl font-bold ${
                      rec.suitabilityScore >= 80
                        ? "text-green-600"
                        : rec.suitabilityScore >= 60
                        ? "text-yellow-600"
                        : "text-orange-600"
                    }`}
                  >
                    {rec.suitabilityScore}%
                  </div>
                  <div className="text-xs text-gray-500">Suitability</div>
                </div>
              </div>

              <p className="text-gray-700 dark:text-gray-300 mb-4">
                {rec.reason}
              </p>

              <div className="bg-gray-50 dark:bg-gray-900 rounded-lg p-4">
                <h5 className="font-semibold text-sm text-gray-900 dark:text-white mb-2">
                  Recommended Practices:
                </h5>
                <ul className="space-y-1">
                  {rec.recommendedPractices.map((practice, idx) => (
                    <li
                      key={idx}
                      className="text-sm text-gray-600 dark:text-gray-400 flex items-start"
                    >
                      <span className="text-green-500 mr-2">✓</span>
                      {practice}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          ))}
        </div>
      </ScrollFloat>
    </div>
  );
};

export default CropsPage;
