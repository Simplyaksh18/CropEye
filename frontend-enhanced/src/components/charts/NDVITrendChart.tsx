// src/components/charts/NDVITrendChart.tsx
// NDVI time-series visualization with health thresholds

import React from "react";
import {
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
  Area,
  ComposedChart,
} from "recharts";
// TooltipProps import omitted — using a local lightweight type for tooltip props
// import type { TooltipProps } from "recharts";
import { format } from "date-fns";

interface NDVIDataPoint {
  date: string;
  value: number;
}

interface NDVITrendChartProps {
  data: NDVIDataPoint[];
  className?: string;
}

export const NDVITrendChart: React.FC<NDVITrendChartProps> = ({
  data,
  className = "",
}) => {
  const formattedData = data.map((point) => ({
    ...point,
    displayDate: format(new Date(point.date), "MMM dd"),
  }));

  type LocalTooltipProps = {
    active?: boolean;
    payload?: Array<{ payload: NDVIDataPoint & { displayDate?: string } }>;
  };

  const CustomTooltip = (props: LocalTooltipProps) => {
    const { active, payload } = props;
    if (active && payload && payload.length) {
      const point = payload[0].payload as NDVIDataPoint & {
        displayDate?: string;
      };
      const value = point.value as number;
      let status = "Poor";
      let color = "#ef4444";

      if (value > 0.6) {
        status = "Healthy";
        color = "#22c55e";
      } else if (value > 0.4) {
        status = "Moderate";
        color = "#eab308";
      } else if (value > 0.2) {
        status = "Fair";
        color = "#f97316";
      }

      return (
        <div className="bg-white dark:bg-gray-800 p-3 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700">
          <p className="text-sm font-semibold text-gray-900 dark:text-white">
            {point.displayDate ?? point.date}
          </p>
          <p className="text-lg font-bold" style={{ color }}>
            NDVI: {value.toFixed(3)}
          </p>
          <p className="text-xs text-gray-600 dark:text-gray-400">
            Status: {status}
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className={className}>
      <ResponsiveContainer width="100%" height={300}>
        <ComposedChart data={formattedData}>
          <defs>
            <linearGradient id="ndviGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#22c55e" stopOpacity={0.6} />
              <stop offset="95%" stopColor="#22c55e" stopOpacity={0.05} />
            </linearGradient>
          </defs>

          <CartesianGrid strokeDasharray="3 3" strokeOpacity={0.06} />
          <XAxis dataKey="displayDate" tick={{ fill: "#9ca3af" }} />
          <YAxis domain={[0, 1]} tick={{ fill: "#9ca3af" }} />
          <Tooltip content={(tp) => <CustomTooltip {...tp} />} />

          {/* Health thresholds */}
          <ReferenceLine y={0.2} stroke="#ef4444" strokeDasharray="3 3" />
          <ReferenceLine y={0.4} stroke="#f97316" strokeDasharray="3 3" />
          <ReferenceLine y={0.6} stroke="#22c55e" strokeDasharray="3 3" />

          <Area
            type="monotone"
            dataKey="value"
            stroke="none"
            fill="url(#ndviGradient)"
          />
          <Line
            type="monotone"
            dataKey="value"
            stroke="#06b6d4"
            strokeWidth={2}
            dot={{ r: 2 }}
          />
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  );
};
