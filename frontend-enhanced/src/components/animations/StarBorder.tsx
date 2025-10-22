import React from "react";
import { motion } from "framer-motion";
import { cn } from "../../utils/cn";

interface StarBorderProps {
  children: React.ReactNode;
  className?: string;
  borderWidth?: number;
  starCount?: number;
}

export const StarBorder: React.FC<StarBorderProps> = ({
  children,
  className = "",
  borderWidth = 2,
  starCount = 20,
}) => {
  const stars = Array.from({ length: starCount }, (_, i) => i);
  const isDark = document.documentElement.classList.contains("dark");
  const color = isDark ? "rgb(46, 185, 255)" : "rgb(41, 255, 44)";

  return (
    <div className={cn("relative inline-block", className)}>
      <motion.div
        className="absolute inset-0 rounded-full"
        animate={{ rotate: 360 }}
        transition={{
          duration: 3,
          repeat: Infinity,
          ease: "linear",
        }}
        style={{
          background: `conic-gradient(from 0deg, transparent 0deg, ${color} 180deg, transparent 360deg)`,
          padding: borderWidth,
          WebkitMask:
            "linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0)",
          WebkitMaskComposite: "xor",
          maskComposite: "exclude",
        }}
      >
        {stars.map((index) => {
          const angle = (index / starCount) * 360;
          return (
            <motion.div
              key={index}
              className="absolute w-1 h-1 bg-white rounded-full"
              style={{
                left: "50%",
                top: "50%",
                transform: `rotate(${angle}deg) translateX(50px)`,
              }}
              animate={{
                scale: [1, 1.5, 1],
                opacity: [0.5, 1, 0.5],
              }}
              transition={{
                duration: 2,
                repeat: Infinity,
                delay: index * 0.1,
              }}
            />
          );
        })}
      </motion.div>
      <div className="relative">{children}</div>
    </div>
  );
};
