import React from "react";
import { Droplets } from "lucide-react";
import { useLocation } from "../hooks/useLocation";
import { AnimatedMetricCard } from "../components/ui/AnimatedMetricCard";
import { ScrollFloat } from "../components/animations/ScrollFloat";

const SoilPage: React.FC = () => {
  const { analysisData, loading } = useLocation();
  const soil = analysisData?.soil_fertility;

  if (loading || !soil) {
    return (
      <div className="text-center">
        <Droplets className="w-24 h-24 mx-auto text-gray-400 mb-4" />
        <p className="text-gray-600 dark:text-gray-400">
          No soil data available. Analyze a location first.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <h1 className="text-4xl font-bold text-gray-900 dark:text-white">
        Soil Analysis
      </h1>

      <ScrollFloat>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {soil.nitrogen_level && (
            <AnimatedMetricCard
              icon={Droplets}
              title="Nitrogen"
              value={soil.nitrogen_level}
              unit="ppm"
              status="info"
            />
          )}
          {soil.phosphorus_level && (
            <AnimatedMetricCard
              icon={Droplets}
              title="Phosphorus"
              value={soil.phosphorus_level}
              unit="ppm"
              status="info"
            />
          )}
          {soil.potassium_level && (
            <AnimatedMetricCard
              icon={Droplets}
              title="Potassium"
              value={soil.potassium_level}
              unit="ppm"
              status="info"
            />
          )}
          {soil.ph_level && (
            <AnimatedMetricCard
              icon={Droplets}
              title="pH Level"
              value={soil.ph_level}
              status="info"
            />
          )}
          {soil.moisture_level && (
            <AnimatedMetricCard
              icon={Droplets}
              title="Moisture"
              value={soil.moisture_level}
              unit="%"
              status="info"
            />
          )}
          {soil.organic_matter && (
            <AnimatedMetricCard
              icon={Droplets}
              title="Organic Matter"
              value={soil.organic_matter}
              unit="%"
              status="info"
            />
          )}
        </div>
      </ScrollFloat>

      {soil.quality_assessment && (
        <ScrollFloat offset={40}>
          <div className="bg-gradient-to-br from-green-500/10 to-emerald-500/10 rounded-2xl p-6 border border-green-500/30">
            <h3 className="text-xl font-bold mb-2 text-gray-900 dark:text-white">
              Quality Assessment
            </h3>
            <p className="text-gray-700 dark:text-gray-300">
              {soil.quality_assessment}
            </p>
          </div>
        </ScrollFloat>
      )}
    </div>
  );
};

export default SoilPage;
