// src/components/ui/LoadingSkeleton.tsx
// Loading skeleton component for various content types

import React from "react";
import { motion } from "framer-motion";

interface LoadingSkeletonProps {
  variant?: "card" | "text" | "chart" | "list";
  count?: number;
  className?: string;
}

export const LoadingSkeleton: React.FC<LoadingSkeletonProps> = ({
  variant = "card",
  count = 1,
  className = "",
}) => {
  const shimmer = {
    animate: { backgroundPosition: ["200% 0", "-200% 0"] },
    transition: { duration: 2, repeat: Infinity },
  };

  const SkeletonCard = () => (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className={`rounded-xl border border-gray-200 dark:border-gray-700 p-6 ${className}`}
    >
      <div className="flex items-start gap-4">
        <motion.div
          {...shimmer}
          className="w-12 h-12 rounded-lg bg-gradient-to-r from-gray-200 via-gray-300 to-gray-200 dark:from-gray-700 dark:via-gray-600 dark:to-gray-700"
          style={{ backgroundSize: "200% 100%" }}
        />
        <div className="flex-1 space-y-3">
          <motion.div
            {...shimmer}
            className="h-4 w-1/3 rounded bg-gradient-to-r from-gray-200 via-gray-300 to-gray-200 dark:from-gray-700 dark:via-gray-600 dark:to-gray-700"
            style={{ backgroundSize: "200% 100%" }}
          />
          <motion.div
            {...shimmer}
            className="h-8 w-2/3 rounded bg-gradient-to-r from-gray-200 via-gray-300 to-gray-200 dark:from-gray-700 dark:via-gray-600 dark:to-gray-700"
            style={{ backgroundSize: "200% 100%" }}
          />
          <motion.div
            {...shimmer}
            className="h-3 w-full rounded bg-gradient-to-r from-gray-200 via-gray-300 to-gray-200 dark:from-gray-700 dark:via-gray-600 dark:to-gray-700"
            style={{ backgroundSize: "200% 100%" }}
          />
        </div>
      </div>
    </motion.div>
  );

  const SkeletonChart = () => (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className={`rounded-xl border border-gray-200 dark:border-gray-700 p-6 ${className}`}
    >
      <motion.div
        {...shimmer}
        className="h-[300px] w-full rounded bg-gradient-to-r from-gray-200 via-gray-300 to-gray-200 dark:from-gray-700 dark:via-gray-600 dark:to-gray-700"
        style={{ backgroundSize: "200% 100%" }}
      />
    </motion.div>
  );

  if (variant === "chart") return <SkeletonChart />;

  return (
    <>
      {Array.from({ length: count }).map((_, index) => (
        <SkeletonCard key={index} />
      ))}
    </>
  );
};
