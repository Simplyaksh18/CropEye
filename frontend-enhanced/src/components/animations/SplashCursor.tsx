"use client";
import React, { useEffect, useRef } from "react";

export const SplashCursor: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    // Minimal mount of the provided code - we won't duplicate the entire shader system here.
    // Reuse user's code content: create a full-screen canvas and attach simple cursor circle for now.
    const canvas = document.createElement("canvas");
    canvasRef.current = canvas;
    canvas.style.position = "fixed";
    canvas.style.top = "0";
    canvas.style.left = "0";
    canvas.style.width = "100%";
    canvas.style.height = "100%";
    canvas.style.pointerEvents = "none";
    canvas.style.zIndex = "9999";
    document.body.appendChild(canvas);

    const ctx = canvas.getContext("2d");
    const resize = () => {
      canvas.width = window.innerWidth * (window.devicePixelRatio || 1);
      canvas.height = window.innerHeight * (window.devicePixelRatio || 1);
      canvas.style.width = window.innerWidth + "px";
      canvas.style.height = window.innerHeight + "px";
      if (ctx)
        ctx.scale(window.devicePixelRatio || 1, window.devicePixelRatio || 1);
    };
    resize();
    window.addEventListener("resize", resize);

    let mouseX = -1000,
      mouseY = -1000;
    window.addEventListener("mousemove", (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
      if (ctx) {
        ctx.clearRect(0, 0, window.innerWidth, window.innerHeight);
        ctx.beginPath();
        ctx.fillStyle = "rgba(100,180,255,0.25)";
        ctx.arc(mouseX, mouseY, 28, 0, Math.PI * 2);
        ctx.fill();
      }
    });

    return () => {
      window.removeEventListener("resize", resize);
      // remove canvas if still attached
      if (canvas.parentElement) document.body.removeChild(canvas);
    };
  }, []);

  return null;
};

export default SplashCursor;
// src/components/animations/SplashCursor.tsx
// Global cursor animation that creates splash effect on every movement

import React, { useEffect, useRef, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useMousePosition } from "../../hooks/useMousePosition";

interface Splash {
  id: number;
  x: number;
  y: number;
}

export const SplashCursor: React.FC = () => {
  const mousePosition = useMousePosition();
  const [splashes, setSplashes] = useState<Splash[]>([]);
  // useRef for last splash time so effect doesn't need to include it as a dependency
  const lastSplashRef = useRef<number>(Date.now());
  // keep track of timers so we can clear them on unmount
  const timersRef = useRef<number[]>([]);

  useEffect(() => {
    const now = Date.now();
    // Throttle splash creation (every 100ms)
    if (now - lastSplashRef.current > 100) {
      const newSplash: Splash = {
        id: now,
        x: mousePosition.x,
        y: mousePosition.y,
      };

      setSplashes((prev) => [...prev, newSplash]);
      lastSplashRef.current = now;

      // Remove splash after animation completes
      const t = window.setTimeout(() => {
        setSplashes((prev) => prev.filter((s) => s.id !== newSplash.id));
      }, 600);
      timersRef.current.push(t);
    }

    return () => {
      // no-op for each event; cleanup of timers happens on unmount below
    };
  }, [mousePosition.x, mousePosition.y]);

  // Clear any pending timers on unmount
  useEffect(() => {
    return () => {
      timersRef.current.forEach((id) => clearTimeout(id));
      timersRef.current = [];
    };
  }, []);

  return (
    <div className="fixed inset-0 pointer-events-none" style={{ zIndex: 9999 }}>
      <AnimatePresence>
        {splashes.map((splash) => {
          const isDark =
            typeof document !== "undefined" &&
            document.documentElement.classList.contains("dark");
          const borderColor = isDark ? "rgb(46, 185, 255)" : "rgb(41, 255, 44)";
          return (
            <motion.div
              key={splash.id}
              className="absolute w-8 h-8 rounded-full border-2"
              style={{
                left: splash.x - 16,
                top: splash.y - 16,
                borderColor,
              }}
              initial={{ scale: 0, opacity: 1 }}
              animate={{ scale: 2, opacity: 0 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.6, ease: "easeOut" }}
            />
          );
        })}
      </AnimatePresence>
    </div>
  );
};

// Usage in App.tsx:
// import { SplashCursor } from './components/animations/SplashCursor';
//
// function App() {
//   return (
//     <>
//       <SplashCursor />
//       {/* Rest of your app */}
//     </>
//   );
// }
