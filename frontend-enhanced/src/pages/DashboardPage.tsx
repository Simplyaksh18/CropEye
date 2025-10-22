// src/pages/DashboardPage.tsx
import React from "react";
import { useNavigate } from "react-router-dom";
import { Leaf, Cloud, Bug, Droplets, Wheat } from "lucide-react";
import { GradientText } from "../components/animations/GradientText";
import { RotatingText } from "../components/ui/RotatingText";
import { MagicBento } from "../components/ui/MagicBento";
import { ScrollFloat } from "../components/animations/ScrollFloat";

const DashboardPage: React.FC = () => {
  const navigate = useNavigate();

  const modules = [
    "Pest & Disease Management",
    "Water Management",
    "Weather Forecast",
    "Crop Recommendations",
    "Soil Analysis",
  ];

  return (
    <div className="space-y-12">
      <div className="text-center">
        <GradientText
          text="GIS Agriculture Dashboard"
          className="text-4xl md:text-6xl mb-4"
        />
        <p className="text-gray-600 dark:text-gray-400 text-lg">
          Comprehensive farm analysis powered by satellite imagery and AI
        </p>
      </div>

      <RotatingText items={modules} interval={3000} className="my-12" />

      <ScrollFloat offset={30}>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <MagicBento
            title="NDVI Analysis"
            description="Track vegetation health with satellite imagery"
            icon={<Leaf className="w-12 h-12 text-green-500" />}
            onClick={() => navigate("/ndvi")}
            spotlightRadius={400}
            showStars={true}
          />

          <MagicBento
            title="Weather Forecast"
            description="Real-time weather data and predictions"
            icon={<Cloud className="w-12 h-12 text-blue-500" />}
            onClick={() => navigate("/weather")}
            spotlightRadius={400}
            showStars={true}
          />
          <MagicBento
            title="Water Management"
            description="Irrigation scheduling and water stress analysis"
            icon={<Droplets className="w-12 h-12 text-blue-500" />}
            onClick={() => navigate("/water")}
            spotlightRadius={400}
            showStars={true}
          />
          <MagicBento
            title="Pest Management"
            description="Early detection and prevention strategies"
            icon={<Bug className="w-12 h-12 text-red-500" />}
            onClick={() => navigate("/pests")}
            spotlightRadius={400}
            showStars={true}
          />

          <MagicBento
            title="Soil Analysis"
            description="Comprehensive soil health metrics"
            icon={<Droplets className="w-12 h-12 text-cyan-500" />}
            onClick={() => navigate("/soil")}
            spotlightRadius={400}
            showStars={true}
          />

          <MagicBento
            title="Crop Recommendations"
            description="AI-powered crop selection guidance"
            icon={<Wheat className="w-12 h-12 text-yellow-500" />}
            onClick={() => navigate("/crops")}
            spotlightRadius={400}
            showStars={true}
          />

          <MagicBento
            title="Overview"
            description="Complete farm health summary"
            icon={<Leaf className="w-12 h-12 text-emerald-500" />}
            onClick={() => navigate("/overview")}
            spotlightRadius={400}
            showStars={true}
          />
        </div>
      </ScrollFloat>
    </div>
  );
};

export default DashboardPage;
