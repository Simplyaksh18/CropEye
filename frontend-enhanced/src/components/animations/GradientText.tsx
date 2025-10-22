// src/components/animations/GradientText.tsx
// Animated gradient text component for main dashboard title

import React from "react";
import { motion } from "framer-motion";

/**
 * Lightweight "cn" utility to conditionally join class names.
 * Mirrors common "clsx"/"classnames" behavior used across the codebase.
 */
const cn = (...args: Array<string | false | null | undefined>) =>
  args.filter(Boolean).join(" ");

interface GradientTextProps {
  text: string;
  className?: string;
  gradient?: string;
  animate?: boolean;
}

export const GradientText: React.FC<GradientTextProps> = ({
  text,
  className = "",
  gradient,
  animate = true,
}) => {
  // Auto-detect theme and use appropriate gradient
  const isDark = document.documentElement.classList.contains("dark");

  const defaultGradient = isDark
    ? "linear-gradient(90deg, rgb(46, 185, 255) 0%, #3B82F6 50%, #6366F1 100%)"
    : "linear-gradient(90deg, rgb(41, 255, 44) 0%, #10B981 50%, #059669 100%)";

  const gradientStyle = gradient || defaultGradient;

  return (
    <motion.h1
      className={cn(
        "text-transparent bg-clip-text font-bold",
        animate && "bg-[length:200%_auto]",
        className
      )}
      style={{
        backgroundImage: gradientStyle,
      }}
      animate={
        animate
          ? {
              backgroundPosition: ["0% center", "200% center"],
            }
          : undefined
      }
      transition={
        animate
          ? {
              duration: 8,
              repeat: Infinity,
              ease: "linear",
            }
          : undefined
      }
    >
      {text}
    </motion.h1>
  );
};

// Usage Example:
// <GradientText
//   text="CropEye GIS Dashboard"
//   className="text-5xl md:text-7xl"
//   animate={true}
// />
