// src/pages/WeatherPage.tsx
import React from "react";
import { Cloud, Droplets, Wind, Sun } from "lucide-react";
import { useLocation } from "../hooks/useLocation";
import { ScrollFloat } from "../components/animations/ScrollFloat";
import { WeatherChart } from "../components/charts/WeatherChart";
import { AnimatedMetricCard } from "../components/ui/AnimatedMetricCard";
import { LoadingSkeleton } from "../components/ui/LoadingSkeleton";

const WeatherPage: React.FC = () => {
  const { analysisData, loading } = useLocation();
  const weather = analysisData?.weather_forecast;

  if (loading) {
    return <LoadingSkeleton variant="card" count={3} />;
  }

  if (!weather || !weather.days || weather.days.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] text-center">
        <Cloud className="w-24 h-24 text-gray-400 mb-6" />
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
          No Weather Data Available
        </h2>
        <p className="text-gray-600 dark:text-gray-400">
          Analyze a location to see weather forecast.
        </p>
      </div>
    );
  }

  const today = weather.days[0];

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
          Weather Forecast
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          7-day weather prediction for your location
        </p>
      </div>

      <ScrollFloat>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <AnimatedMetricCard
            icon={Sun}
            title="Temperature"
            value={today.temperature.avg}
            unit="°C"
            status="info"
            description={`Range: ${today.temperature.min}°C - ${today.temperature.max}°C`}
          />

          <AnimatedMetricCard
            icon={Droplets}
            title="Precipitation"
            value={today.precipitation}
            unit="mm"
            status="info"
            description="Expected rainfall"
          />

          <AnimatedMetricCard
            icon={Droplets}
            title="Humidity"
            value={today.humidity}
            unit="%"
            status="info"
            description="Relative humidity"
          />

          <AnimatedMetricCard
            icon={Wind}
            title="Wind Speed"
            value={today.wind.avg_speed}
            unit="km/h"
            status="info"
            description={`Gusts up to ${today.wind.gust_max} km/h`}
          />
        </div>
      </ScrollFloat>

      <ScrollFloat offset={40}>
        <div className="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-6">
          <h3 className="text-xl font-semibold mb-4 text-gray-900 dark:text-white">
            7-Day Forecast
          </h3>
          <WeatherChart data={weather.days} />
        </div>
      </ScrollFloat>

      <ScrollFloat offset={50}>
        <div className="bg-gradient-to-br from-blue-500/10 to-cyan-500/10 rounded-2xl p-6 border border-blue-500/30">
          <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">
            Weather Summary
          </h3>
          <p className="text-gray-700 dark:text-gray-300">{weather.summary}</p>
        </div>
      </ScrollFloat>
    </div>
  );
};

export default WeatherPage;
