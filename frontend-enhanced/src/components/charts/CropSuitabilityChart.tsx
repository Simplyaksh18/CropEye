// src/components/charts/CropSuitabilityChart.tsx
// Horizontal bar chart with color-coded suitability scores

import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";

interface CropSuitabilityChartProps {
  data: Array<{ crop: string; suitabilityScore: number }>;
  className?: string;
}

export const CropSuitabilityChart: React.FC<CropSuitabilityChartProps> = ({
  data,
  className = "",
}) => {
  const sortedData = [...data].sort(
    (a, b) => b.suitabilityScore - a.suitabilityScore
  );

  const getColor = (score: number) => {
    if (score >= 80) return "#22c55e";
    if (score >= 60) return "#84cc16";
    if (score >= 40) return "#eab308";
    return "#f97316";
  };

  return (
    <div className={className}>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={sortedData} layout="horizontal">
          <CartesianGrid
            strokeDasharray="3 3"
            className="stroke-gray-200 dark:stroke-gray-700"
          />
          <XAxis
            type="number"
            domain={[0, 100]}
            className="text-xs text-gray-600 dark:text-gray-400"
          />
          <YAxis
            type="category"
            dataKey="crop"
            width={100}
            className="text-xs text-gray-600 dark:text-gray-400"
          />
          {/** Use a dedicated tooltip component to avoid named collisions */}
          <Tooltip
            content={(tp) => {
              const active = tp?.active;
              const payload = tp?.payload;
              if (active && payload && payload.length) {
                const item = payload[0].payload as {
                  crop: string;
                  suitabilityScore: number;
                };
                return (
                  <div className="bg-white dark:bg-gray-800 p-3 rounded-lg shadow-lg border">
                    <p className="font-semibold">{item.crop}</p>
                    <p
                      className="text-lg font-bold"
                      style={{ color: getColor(item.suitabilityScore) }}
                    >
                      {item.suitabilityScore}% suitable
                    </p>
                  </div>
                );
              }
              return null;
            }}
          />

          <Bar dataKey="suitabilityScore" radius={[0, 8, 8, 0]}>
            {sortedData.map((entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={getColor(entry.suitabilityScore)}
              />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};
