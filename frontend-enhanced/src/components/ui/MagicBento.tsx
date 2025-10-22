// src/components/ui/MagicBento.tsx
// Feature cards with spotlight (radius: 400), tilt, click effect, and magnetism

import React, { useRef, useState } from "react";
import { motion } from "framer-motion";
import { useMousePosition } from "../../hooks/useMousePosition";
import { cn } from "../../utils/cn";

interface MagicBentoProps {
  title: string;
  description: string;
  icon: React.ReactNode;
  onClick?: () => void;
  className?: string;
  spotlightRadius?: number;
  showStars?: boolean;
}

export const MagicBento: React.FC<MagicBentoProps> = ({
  title,
  description,
  icon,
  onClick,
  className = "",
  spotlightRadius = 400,
  showStars = true,
}) => {
  const cardRef = useRef<HTMLDivElement>(null);
  const [isHovered, setIsHovered] = useState(false);
  const [tilt, setTilt] = useState({ x: 0, y: 0 });
  const mousePosition = useMousePosition();

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!cardRef.current) return;

    const rect = cardRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    const centerX = rect.width / 2;
    const centerY = rect.height / 2;

    const tiltX = ((y - centerY) / centerY) * 10;
    const tiltY = ((x - centerX) / centerX) * -10;

    setTilt({ x: tiltX, y: tiltY });
  };

  const handleMouseLeave = () => {
    setIsHovered(false);
    setTilt({ x: 0, y: 0 });
  };

  return (
    <motion.div
      ref={cardRef}
      className={cn(
        "relative overflow-hidden rounded-2xl bg-white/5 dark:bg-white/5",
        "border border-white/10 backdrop-blur-sm",
        "cursor-pointer group",
        className
      )}
      onMouseEnter={() => setIsHovered(true)}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      onClick={onClick}
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      style={{
        transform: `perspective(1000px) rotateX(${tilt.x}deg) rotateY(${tilt.y}deg)`,
        transition: "transform 0.1s ease-out",
      }}
    >
      {/* Spotlight Effect */}
      {isHovered && (
        <motion.div
          className="absolute inset-0 opacity-50"
          style={{
            background: `radial-gradient(circle ${spotlightRadius}px at ${mousePosition.x}px ${mousePosition.y}px, rgba(255,255,255,0.2), transparent)`,
          }}
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.5 }}
          exit={{ opacity: 0 }}
        />
      )}

      {/* Stars Background */}
      {showStars && (
        <div className="absolute inset-0">
          {Array.from({ length: 20 }).map((_, i) => (
            <motion.div
              key={i}
              className="absolute w-0.5 h-0.5 bg-white rounded-full"
              style={{
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`,
              }}
              animate={{
                opacity: [0.2, 1, 0.2],
                scale: [1, 1.5, 1],
              }}
              transition={{
                duration: 2 + Math.random() * 2,
                repeat: Infinity,
                delay: Math.random() * 2,
              }}
            />
          ))}
        </div>
      )}

      {/* Content */}
      <div className="relative z-10 p-6">
        <div className="mb-4 text-4xl">{icon}</div>
        <h3 className="text-xl font-bold text-white mb-2">{title}</h3>
        <p className="text-sm text-white/70">{description}</p>
      </div>

      {/* Magnetic Border Glow */}
      <motion.div
        className="absolute inset-0 rounded-2xl"
        style={{
          background: `linear-gradient(${Math.atan2(tilt.x, tilt.y)}rad, 
            ${
              document.documentElement.classList.contains("dark")
                ? "rgba(46, 185, 255, 0.5)"
                : "rgba(41, 255, 44, 0.5)"
            }, 
            transparent)`,
          opacity: isHovered ? 1 : 0,
          transition: "opacity 0.3s ease",
        }}
      />
    </motion.div>
  );
};
