// src/components/animations/NoiseAnimation.tsx
// Error state overlay with noise effect

import React, { useEffect, useRef } from "react";
import { motion } from "framer-motion";
import { AlertTriangle } from "lucide-react";

interface NoiseAnimationProps {
  show: boolean;
  errorMessage?: string;
  onDismiss?: () => void;
}

export const NoiseAnimation: React.FC<NoiseAnimationProps> = ({
  show,
  errorMessage = "An error occurred",
  onDismiss,
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    if (!show) return;

    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    let animationId: number;

    const drawNoise = () => {
      const imageData = ctx.createImageData(canvas.width, canvas.height);
      const data = imageData.data;

      for (let i = 0; i < data.length; i += 4) {
        const gray = Math.random() * 255;
        data[i] = gray;
        data[i + 1] = gray;
        data[i + 2] = gray;
        data[i + 3] = 50;
      }

      ctx.putImageData(imageData, 0, 0);
      animationId = requestAnimationFrame(drawNoise);
    };

    drawNoise();

    return () => {
      cancelAnimationFrame(animationId);
    };
  }, [show]);

  if (!show) return null;

  return (
    <motion.div
      className="fixed inset-0 z-[9999] flex items-center justify-center"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    >
      <canvas ref={canvasRef} className="absolute inset-0" />

      <motion.div
        className="relative z-10 bg-red-500/90 backdrop-blur-sm rounded-2xl p-8 max-w-md mx-4 border-2 border-red-400"
        initial={{ scale: 0.8, y: 50 }}
        animate={{ scale: 1, y: 0 }}
        transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
      >
        <div className="flex flex-col items-center gap-4">
          <motion.div
            animate={{ rotate: [0, 10, -10, 0] }}
            transition={{ duration: 0.5, repeat: Infinity, repeatDelay: 2 }}
          >
            <AlertTriangle size={48} className="text-white" />
          </motion.div>

          <h2 className="text-2xl font-bold text-white">Error</h2>
          <p className="text-white/90 text-center">{errorMessage}</p>

          {onDismiss && (
            <motion.button
              onClick={onDismiss}
              className="mt-4 px-6 py-2 bg-white text-red-500 rounded-lg font-semibold"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              Dismiss
            </motion.button>
          )}
        </div>
      </motion.div>
    </motion.div>
  );
};
