// src/components/animations/ParticlesBackground.tsx
// Interactive particle background with mouse interaction
// Light Mode: rgb(41, 255, 44), Dark Mode: rgb(46, 185, 255)
// Count: 700, Speed: 0.2, Spread: 10, BaseSize: 100

import React, { useEffect, useRef } from "react";
import { useMousePosition } from "../../hooks/useMousePosition";

interface ParticlesBackgroundProps {
  color?: string;
  count?: number;
  speed?: number;
  spread?: number;
  baseSize?: number;
  mouseInteraction?: boolean;
  className?: string;
}

// A standalone particle class that does not close over React props so it
// can be safely used inside effects without causing dependency issues.
class ParticleInstance {
  x: number;
  y: number;
  vx: number;
  vy: number;
  size: number;
  baseX: number;
  baseY: number;

  constructor(canvasWidth: number, canvasHeight: number, speed: number) {
    this.baseX = Math.random() * canvasWidth;
    this.baseY = Math.random() * canvasHeight;
    this.x = this.baseX;
    this.y = this.baseY;
    this.vx = (Math.random() - 0.5) * speed;
    this.vy = (Math.random() - 0.5) * speed;
    this.size = Math.random() * 2 + 1;
  }

  update(
    mouseX: number,
    mouseY: number,
    canvas: HTMLCanvasElement,
    opts: {
      mouseInteraction: boolean;
      spread: number;
      baseSize: number;
    }
  ) {
    const { mouseInteraction, spread, baseSize } = opts;

    if (mouseInteraction) {
      const dx = mouseX - this.x;
      const dy = mouseY - this.y;
      const distance = Math.sqrt(dx * dx + dy * dy);
      const maxDistance = baseSize;

      if (distance < maxDistance) {
        const force = (maxDistance - distance) / maxDistance;
        const angle = Math.atan2(dy, dx);
        this.vx -= Math.cos(angle) * force * spread * 0.1;
        this.vy -= Math.sin(angle) * force * spread * 0.1;
      }
    }

    // Return to base position
    this.vx += (this.baseX - this.x) * 0.01;
    this.vy += (this.baseY - this.y) * 0.01;

    // Apply velocity
    this.x += this.vx;
    this.y += this.vy;

    // Friction
    this.vx *= 0.95;
    this.vy *= 0.95;

    // Boundary check
    if (this.x < 0 || this.x > canvas.width) this.vx *= -1;
    if (this.y < 0 || this.y > canvas.height) this.vy *= -1;
  }

  draw(ctx: CanvasRenderingContext2D, color: string) {
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
    ctx.fillStyle = color;
    ctx.fill();
  }
}

export const ParticlesBackground: React.FC<ParticlesBackgroundProps> = ({
  color,
  count = 700,
  speed = 0.2,
  spread = 10,
  baseSize = 100,
  mouseInteraction = true,
  className = "",
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const mousePosition = useMousePosition();
  // Keep a ref to the latest mouse position so the animation loop doesn't
  // re-create the whole canvas on every mouse move (avoid re-running effect)
  const mousePosRef = useRef(mousePosition);

  // Auto-detect theme color (guard for SSR environments)
  const isDark =
    typeof document !== "undefined" &&
    document.documentElement.classList.contains("dark");
  const particleColor =
    color || (isDark ? "rgb(46, 185, 255)" : "rgb(41, 255, 44)");

  // Particle refs must be created after the class is defined so TypeScript
  // recognizes the type `Particle`.
  const particlesRef = useRef<ParticleInstance[]>([]);

  // Update mouse position ref when mousePosition changes
  useEffect(() => {
    mousePosRef.current = mousePosition;
  }, [mousePosition]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    // Set canvas size
    const resizeCanvas = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    resizeCanvas();
    window.addEventListener("resize", resizeCanvas);

    // Initialize particles (pass speed into constructor)
    particlesRef.current = Array.from(
      { length: count },
      () => new ParticleInstance(canvas.width, canvas.height, speed)
    );

    // Animation loop
    let animationId: number;
    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      const mp = mousePosRef.current || {
        x: canvas.width / 2,
        y: canvas.height / 2,
      };
      particlesRef.current.forEach((particle) => {
        particle.update(mp.x, mp.y, canvas, {
          mouseInteraction,
          spread,
          baseSize,
        });
        particle.draw(ctx, particleColor);
      });

      animationId = requestAnimationFrame(animate);
    };
    animate();

    return () => {
      cancelAnimationFrame(animationId);
      window.removeEventListener("resize", resizeCanvas);
    };
  }, [
    mousePosition,
    count,
    speed,
    spread,
    baseSize,
    particleColor,
    mouseInteraction,
  ]);

  return (
    <canvas
      ref={canvasRef}
      className={`fixed inset-0 pointer-events-none ${className}`}
      style={{ zIndex: 1 }}
    />
  );
};

// Usage Example:
// Light mode
// <ParticlesBackground color="rgb(41, 255, 44)" count={700} speed={0.2} spread={10} baseSize={100} />
//
// Dark mode
// <ParticlesBackground color="rgb(46, 185, 255)" count={700} speed={0.2} spread={10} baseSize={100} />
