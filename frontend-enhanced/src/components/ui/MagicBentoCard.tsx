import React, { useRef, useEffect } from "react";
import clsx from "clsx";

interface Props {
  children?: React.ReactNode;
  className?: string;
  spotlightRadius?: number;
  enableTilt?: boolean;
  onClick?: () => void;
}

export const MagicBentoCard: React.FC<Props> = ({
  children,
  className = "",
  spotlightRadius = 400,
  enableTilt = true,
  onClick,
}) => {
  const ref = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    const el = ref.current;
    if (!el || !enableTilt) return;

    const handleMove = (e: MouseEvent) => {
      const rect = el.getBoundingClientRect();
      const x = ((e.clientX - rect.left) / rect.width - 0.5) * 2;
      const y = ((e.clientY - rect.top) / rect.height - 0.5) * 2;
      el.style.transform = `perspective(800px) rotateX(${-y * 6}deg) rotateY(${
        x * 8
      }deg) translateZ(0)`;
      // spotlight via CSS variables
      el.style.setProperty("--spot-x", String(e.clientX - rect.left));
      el.style.setProperty("--spot-y", String(e.clientY - rect.top));
    };

    const handleLeave = () => {
      if (!el) return;
      el.style.transform = "";
    };

    el.addEventListener("mousemove", handleMove);
    el.addEventListener("mouseleave", handleLeave);
    return () => {
      el.removeEventListener("mousemove", handleMove);
      el.removeEventListener("mouseleave", handleLeave);
    };
  }, [enableTilt]);

  return (
    <div
      ref={ref}
      onClick={onClick}
      className={clsx(
        "relative rounded-2xl p-6 bg-gradient-to-br from-white/5 to-white/3 border border-white/10 shadow-xl overflow-hidden",
        // dark mode subtle color tweak
        "dark:from-black/30 dark:to-black/20 dark:border-black/25",
        className
      )}
      style={
        {
          transition: "transform 180ms ease",
          "--spotlight-radius": `${spotlightRadius}px`,
        } as React.CSSProperties
      }
    >
      {/* spotlight layer */}
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0 opacity-60"
        style={
          {
            background:
              "radial-gradient(closest-side, rgba(255,255,255,0.08), transparent)",
            maskImage:
              "radial-gradient(circle at var(--spot-x,50%) var(--spot-y,50%), rgba(0,0,0,1), rgba(0,0,0,0))",
          } as React.CSSProperties
        }
      />

      {children}
    </div>
  );
};

export default MagicBentoCard;
