// src/components/ui/AgricultureFacts.tsx
// Rotating agriculture fun facts with animations

import React, { useState, useEffect } from "react";
import {
  Sprout,
  Droplet,
  Sun,
  Wind,
  Satellite,
  BarChart3,
  Activity,
  Wheat,
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

interface Fact {
  icon: React.ReactNode;
  title: string;
  description: string;
  color: string;
}

const AGRICULTURE_FACTS: Fact[] = [
  {
    icon: <Satellite className="w-8 h-8" />,
    title: "Satellite‑Driven Intelligence",
    description:
      "CropEye integrates Sentinel‑2 and NDVI data to detect early crop stress, guiding precision irrigation and fertilizer use.",
    color: "from-indigo-500 to-blue-600",
  },
  {
    icon: <Sprout className="w-8 h-8" />,
    title: "AI for Smart Farming",
    description:
      "AI models in CropEye analyze soil moisture, weather, and crop health to optimize yield while reducing input costs.",
    color: "from-green-500 to-emerald-600",
  },
  {
    icon: <Droplet className="w-8 h-8" />,
    title: "Intelligent Water Management",
    description:
      "Dynamic irrigation scheduling using Copernicus weather data saves up to 45% water per acre, improving sustainability.",
    color: "from-cyan-500 to-blue-600",
  },
  {
    icon: <BarChart3 className="w-8 h-8" />,
    title: "Data‑Driven Soil Insights",
    description:
      "SoilGrids and in‑field sensors map nutrient richness, pH, and organic matter—powering data‑centric agronomy decisions.",
    color: "from-amber-500 to-yellow-600",
  },
  {
    icon: <Sun className="w-8 h-8" />,
    title: "Climate‑Aligned Cultivation",
    description:
      "CropEye correlates real‑time weather and evapotranspiration to predict yield zones and mitigate drought risk.",
    color: "from-orange-500 to-red-500",
  },
  {
    icon: <Wind className="w-8 h-8" />,
    title: "Pest & Disease Forecasting",
    description:
      "Our pest‑risk engine predicts outbreaks based on temperature, humidity, and soil factors up to 10 days in advance.",
    color: "from-purple-500 to-violet-600",
  },
  {
    icon: <Wheat className="w-8 h-8" />,
    title: "Crop Recommendation Engine",
    description:
      "Integrated analysis of soil nitrogen, rainfall, and NDVI indices helps farmers select the best crop for current season.",
    color: "from-lime-500 to-green-600",
  },
  {
    icon: <Activity className="w-8 h-8" />,
    title: "Performance Dashboard",
    description:
      "The unified dashboard provides live KPIs on irrigation, soil, yield, and crop stress — all in one smart interface.",
    color: "from-gray-700 to-slate-900",
  },
];

interface AgricultureFactsProps {
  className?: string;
}

export const AgricultureFacts: React.FC<AgricultureFactsProps> = ({
  className = "",
}) => {
  const [currentFactIndex, setCurrentFactIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentFactIndex((prev) => (prev + 1) % AGRICULTURE_FACTS.length);
    }, 5000); // Change fact every 5 seconds

    return () => clearInterval(interval);
  }, []);

  const currentFact = AGRICULTURE_FACTS[currentFactIndex];

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Main Fact Card */}
      <AnimatePresence mode="wait">
        <motion.div
          key={currentFactIndex}
          initial={{ opacity: 0, x: -50 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: 50 }}
          transition={{ duration: 0.5 }}
          className={`bg-gradient-to-br ${currentFact.color} p-8 rounded-3xl shadow-2xl text-white relative overflow-hidden`}
        >
          {/* Decorative Elements */}
          <div className="absolute top-0 right-0 w-40 h-40 bg-white/10 rounded-full -mr-20 -mt-20" />
          <div className="absolute bottom-0 left-0 w-32 h-32 bg-white/10 rounded-full -ml-16 -mb-16" />

          <div className="relative z-10">
            <div className="mb-4">{currentFact.icon}</div>
            <h3 className="text-2xl font-bold mb-3">{currentFact.title}</h3>
            <p className="text-white/90 leading-relaxed">
              {currentFact.description}
            </p>
          </div>

          {/* Progress Indicator */}
          <div className="mt-6 flex gap-1.5">
            {AGRICULTURE_FACTS.map((_, index) => (
              <div
                key={index}
                className={`h-1 rounded-full flex-1 transition-all duration-300 ${
                  index === currentFactIndex ? "bg-white" : "bg-white/30"
                }`}
              />
            ))}
          </div>
        </motion.div>
      </AnimatePresence>

      {/* Title Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="text-center lg:text-left"
      >
        <h2 className="text-4xl font-bold text-gray-800 dark:text-white mb-4">
          Welcome to
          <span className="block text-transparent bg-clip-text bg-gradient-to-r from-green-500 to-emerald-600">
            CropEye
          </span>
        </h2>
        <p className="text-lg text-gray-600 dark:text-gray-400 max-w-md">
          Your intelligent farming companion powered by satellite imagery, AI,
          and real-time data analytics.
        </p>
      </motion.div>

      {/* Quick Stats & Testimonial (replaces small feature cards) */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
        className="space-y-4"
      >
        {/* Inject Google Fonts for this component (dev-friendly) */}
        <link
          rel="stylesheet"
          href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Lora:wght@400;700&display=swap"
        />

        <div className="grid grid-cols-2 gap-4">
          <div className="bg-white/90 dark:bg-gray-800/70 p-4 rounded-xl shadow-md border border-gray-200 dark:border-gray-700">
            <div className="text-sm text-gray-500">Avg Yield Uplift</div>
            <div
              className="mt-2 text-2xl font-bold"
              style={{ fontFamily: "Lora, serif" }}
            >
              +28%
            </div>
            <div className="text-xs text-gray-400 mt-1">
              Across active pilot farms
            </div>
          </div>

          <div className="bg-white/90 dark:bg-gray-800/70 p-4 rounded-xl shadow-md border border-gray-200 dark:border-gray-700">
            <div className="text-sm text-gray-500">Water Saved</div>
            <div
              className="mt-2 text-2xl font-bold"
              style={{ fontFamily: "Lora, serif" }}
            >
              -42%
            </div>
            <div className="text-xs text-gray-400 mt-1">
              Compared to baseline irrigation
            </div>
          </div>
        </div>

        <div className="bg-gradient-to-r from-green-50/40 to-emerald-50/20 dark:from-gray-800/40 dark:to-gray-900/30 p-4 rounded-xl border border-gray-200 dark:border-gray-700">
          <div className="flex items-start gap-4">
            <div className="w-12 h-12 rounded-full bg-white/10 flex items-center justify-center">
              <svg
                width="28"
                height="28"
                viewBox="0 0 24 24"
                fill="none"
                stroke="white"
                strokeWidth="1.5"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                <polyline points="7 10 12 15 17 10" />
                <line x1="12" y1="15" x2="12" y2="3" />
              </svg>
            </div>
            <div>
              <div
                className="text-sm text-gray-700 dark:text-gray-200 font-semibold"
                style={{ fontFamily: "Inter, sans-serif" }}
              >
                Farmer testimonial
              </div>
              <div
                className="text-sm text-gray-600 dark:text-gray-300 mt-2"
                style={{ fontFamily: "Inter, sans-serif" }}
              >
                "CropEye helped reduce water use and improved yield
                predictability on our fields — the NDVI alerts are a game
                changer."
              </div>
              <div className="mt-3 text-xs text-gray-400">
                — R. Singh, Punjab
              </div>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  );
};
