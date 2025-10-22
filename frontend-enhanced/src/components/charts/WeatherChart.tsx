// src/components/charts/WeatherChart.tsx
// Combined weather chart with temperature and precipitation

import React from "react";
import {
  ComposedChart,
  Line,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Area,
} from "recharts";
import { format } from "date-fns";

interface WeatherDataPoint {
  date: string;
  temperature: { min: number; max: number; avg: number };
  precipitation: number;
  humidity: number;
}

interface WeatherChartProps {
  data: WeatherDataPoint[];
  className?: string;
}

export const WeatherChart: React.FC<WeatherChartProps> = ({
  data,
  className = "",
}) => {
  const formattedData = data.map((point) => ({
    date: format(new Date(point.date), "EEE dd"),
    tempMin: point.temperature.min,
    tempMax: point.temperature.max,
    tempAvg: point.temperature.avg,
    precipitation: point.precipitation,
    humidity: point.humidity,
  }));

  return (
    <div className={className}>
      <ResponsiveContainer width="100%" height={400}>
        <ComposedChart data={formattedData}>
          <defs>
            <linearGradient id="tempGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#f97316" stopOpacity={0.3} />
              <stop offset="95%" stopColor="#f97316" stopOpacity={0} />
            </linearGradient>
          </defs>

          <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.3} />
          <XAxis dataKey="date" stroke="#9ca3af" style={{ fontSize: "12px" }} />
          <YAxis yAxisId="temp" stroke="#9ca3af" style={{ fontSize: "12px" }} />
          <YAxis
            yAxisId="precip"
            orientation="right"
            stroke="#9ca3af"
            style={{ fontSize: "12px" }}
          />
          <Tooltip />
          <Legend />

          <Area
            yAxisId="temp"
            type="monotone"
            dataKey="tempAvg"
            fill="url(#tempGradient)"
            stroke="none"
          />
          <Line
            yAxisId="temp"
            type="monotone"
            dataKey="tempMax"
            stroke="#ef4444"
            strokeWidth={2}
            dot={{ fill: "#ef4444", r: 4 }}
            name="Max Temp"
          />
          <Line
            yAxisId="temp"
            type="monotone"
            dataKey="tempAvg"
            stroke="#f97316"
            strokeWidth={3}
            dot={{ fill: "#f97316", r: 5 }}
            name="Avg Temp"
          />
          <Line
            yAxisId="temp"
            type="monotone"
            dataKey="tempMin"
            stroke="#3b82f6"
            strokeWidth={2}
            dot={{ fill: "#3b82f6", r: 4 }}
            name="Min Temp"
          />
          <Bar
            yAxisId="precip"
            dataKey="precipitation"
            fill="#06b6d4"
            opacity={0.6}
            radius={[8, 8, 0, 0]}
            name="Precipitation"
          />
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  );
};
