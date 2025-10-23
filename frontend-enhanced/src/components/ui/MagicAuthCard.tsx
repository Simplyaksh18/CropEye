// src/components/ui/MagicAuthCard.tsx
// Magic Bento Card Animation for Auth Pages with GSAP

import React, { useRef, useEffect, useState } from "react";
import { gsap } from "gsap";

interface MagicAuthCardProps {
  children: React.ReactNode;
  className?: string;
}

export const MagicAuthCard: React.FC<MagicAuthCardProps> = ({
  children,
  className = "",
}) => {
  const cardRef = useRef<HTMLDivElement>(null);
  const particlesRef = useRef<HTMLDivElement[]>([]);
  const [isHovered, setIsHovered] = useState(false);

  useEffect(() => {
    if (!cardRef.current) return;

    const card = cardRef.current;

    const handleMouseMove = (e: MouseEvent) => {
      if (!cardRef.current) return;

      const rect = cardRef.current.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const centerX = rect.width / 2;
      const centerY = rect.height / 2;

      // Tilt effect
      const rotateX = ((y - centerY) / centerY) * -5;
      const rotateY = ((x - centerX) / centerX) * 5;

      gsap.to(cardRef.current, {
        rotateX,
        rotateY,
        duration: 0.3,
        ease: "power2.out",
        transformPerspective: 1000,
      });

      // Update spotlight position
      const relativeX = (x / rect.width) * 100;
      const relativeY = (y / rect.height) * 100;
      card.style.setProperty("--spotlight-x", `${relativeX}%`);
      card.style.setProperty("--spotlight-y", `${relativeY}%`);
    };

    const handleMouseEnter = () => {
      setIsHovered(true);

      // Create particles
      if (particlesRef.current.length === 0) {
        for (let i = 0; i < 20; i++) {
          const particle = document.createElement("div");
          particle.className = "particle";
          particle.style.cssText = `
            position: absolute;
            width: 3px;
            height: 3px;
            border-radius: 50%;
            background: rgba(16, 185, 129, 0.6);
            box-shadow: 0 0 10px rgba(16, 185, 129, 0.8);
            pointer-events: none;
            left: ${Math.random() * 100}%;
            top: ${Math.random() * 100}%;
          `;
          cardRef.current?.appendChild(particle);
          particlesRef.current.push(particle);

          // Animate particle
          gsap.fromTo(
            particle,
            { scale: 0, opacity: 0 },
            {
              scale: 1,
              opacity: 1,
              duration: 0.3,
              ease: "back.out(1.7)",
            }
          );

          gsap.to(particle, {
            x: (Math.random() - 0.5) * 50,
            y: (Math.random() - 0.5) * 50,
            rotation: Math.random() * 360,
            duration: 2 + Math.random() * 2,
            ease: "none",
            repeat: -1,
            yoyo: true,
          });

          gsap.to(particle, {
            opacity: 0.3,
            duration: 1.5,
            ease: "power2.inOut",
            repeat: -1,
            yoyo: true,
          });
        }
      }
    };

    const handleMouseLeave = () => {
      setIsHovered(false);

      // Remove particles
      particlesRef.current.forEach((particle) => {
        gsap.to(particle, {
          scale: 0,
          opacity: 0,
          duration: 0.3,
          onComplete: () => particle.remove(),
        });
      });
      particlesRef.current = [];

      // Reset tilt
      gsap.to(cardRef.current, {
        rotateX: 0,
        rotateY: 0,
        duration: 0.3,
        ease: "power2.out",
      });
    };

    card.addEventListener("mouseenter", handleMouseEnter);
    card.addEventListener("mouseleave", handleMouseLeave);
    card.addEventListener("mousemove", handleMouseMove);

    return () => {
      card.removeEventListener("mouseenter", handleMouseEnter);
      card.removeEventListener("mouseleave", handleMouseLeave);
      card.removeEventListener("mousemove", handleMouseMove);
    };
  }, []);

  return (
    <div
      ref={cardRef}
      className={`relative bg-white dark:bg-gray-800 rounded-2xl shadow-2xl p-8 border border-gray-200 dark:border-gray-700 overflow-hidden ${className}`}
      // CSS custom properties are provided via a typed object to satisfy TS
      style={{
        transformStyle: "preserve-3d",
        ...({
          ["--spotlight-x"]: "50%",
          ["--spotlight-y"]: "50%",
        } as React.CSSProperties),
      }}
    >
      {/* Spotlight Effect */}
      <div
        className="absolute inset-0 opacity-0 hover:opacity-100 transition-opacity duration-300 pointer-events-none"
        style={{
          background: `radial-gradient(600px circle at var(--spotlight-x) var(--spotlight-y), rgba(16, 185, 129, 0.1), transparent 40%)`,
        }}
      />

      {/* Border Glow */}
      <div
        className={`absolute inset-0 rounded-2xl transition-opacity duration-300 pointer-events-none ${
          isHovered ? "opacity-100" : "opacity-0"
        }`}
        style={{
          background: `radial-gradient(600px circle at var(--spotlight-x) var(--spotlight-y), rgba(16, 185, 129, 0.3), transparent 40%)`,
          padding: "2px",
          WebkitMask:
            "linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0)",
          WebkitMaskComposite: "xor",
          maskComposite: "exclude",
        }}
      />

      {/* Content */}
      <div className="relative z-10">{children}</div>
    </div>
  );
};
