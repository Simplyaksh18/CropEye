// src/components/animations/ScrollFloat.tsx
// Scroll-triggered floating animation

import React, { useRef } from "react";
import { motion, useScroll, useTransform } from "framer-motion";
import { cn } from "../../utils/cn";

interface ScrollFloatProps {
  children: React.ReactNode;
  className?: string;
  offset?: number;
}

export const ScrollFloat: React.FC<ScrollFloatProps> = ({
  children,
  className = "",
  offset = 50,
}) => {
  const ref = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start end", "end start"],
  });

  const y = useTransform(scrollYProgress, [0, 1], [offset, -offset]);
  const opacity = useTransform(scrollYProgress, [0, 0.2, 0.8, 1], [0, 1, 1, 0]);

  return (
    <motion.div
      ref={ref}
      style={{ y, opacity }}
      className={cn("will-change-transform", className)}
    >
      {children}
    </motion.div>
  );
};
