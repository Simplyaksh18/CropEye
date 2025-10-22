// src/components/ui/AnimatedMetricCard.tsx
// Animated metric display cards with trend indicators

import React, { useEffect, useState } from "react";
import { motion } from "framer-motion";
import type { LucideIcon } from "lucide-react";

interface AnimatedMetricCardProps {
  icon: LucideIcon;
  title: string;
  value: string | number;
  unit?: string;
  status?: "success" | "warning" | "error" | "info";
  description?: string;
  trend?: { value: number; isPositive: boolean };
  className?: string;
}

export const AnimatedMetricCard: React.FC<AnimatedMetricCardProps> = ({
  icon: Icon,
  title,
  value,
  unit,
  status = "info",
  description,
  trend,
  className = "",
}) => {
  const [displayValue, setDisplayValue] = useState(0);

  useEffect(() => {
    if (typeof value === "number") {
      let start = 0;
      const end = value;
      const duration = 1000;
      const increment = end / (duration / 16);

      const timer = setInterval(() => {
        start += increment;
        if (start >= end) {
          setDisplayValue(end);
          clearInterval(timer);
        } else {
          setDisplayValue(start);
        }
      }, 16);

      return () => clearInterval(timer);
    }
  }, [value]);

  const statusColors = {
    success: "from-green-500/20 to-emerald-500/20 border-green-500/50",
    warning: "from-yellow-500/20 to-orange-500/20 border-yellow-500/50",
    error: "from-red-500/20 to-rose-500/20 border-red-500/50",
    info: "from-blue-500/20 to-cyan-500/20 border-blue-500/50",
  };

  const iconColors = {
    success: "text-green-500",
    warning: "text-yellow-500",
    error: "text-red-500",
    info: "text-blue-500",
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      whileHover={{ scale: 1.02, boxShadow: "0 10px 30px rgba(0,0,0,0.1)" }}
      className={`relative overflow-hidden rounded-xl border bg-gradient-to-br ${statusColors[status]} p-6 backdrop-blur-sm ${className}`}
    >
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-2">
            <Icon className={`w-5 h-5 ${iconColors[status]}`} />
            <p className="text-sm font-medium text-gray-600 dark:text-gray-300">
              {title}
            </p>
          </div>

          <div className="flex items-baseline gap-2">
            <motion.p
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ type: "spring", stiffness: 100, delay: 0.2 }}
              className="text-3xl font-bold text-gray-900 dark:text-white"
            >
              {typeof value === "number" ? displayValue.toFixed(2) : value}
            </motion.p>
            {unit && (
              <span className="text-sm text-gray-500 dark:text-gray-400">
                {unit}
              </span>
            )}
          </div>

          {description && (
            <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
              {description}
            </p>
          )}

          {trend && (
            <motion.div
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.4 }}
              className={`mt-2 inline-flex items-center gap-1 text-sm ${
                trend.isPositive ? "text-green-600" : "text-red-600"
              }`}
            >
              <span>{trend.isPositive ? "↑" : "↓"}</span>
              <span>{Math.abs(trend.value).toFixed(1)}%</span>
            </motion.div>
          )}
        </div>
      </div>
    </motion.div>
  );
};
