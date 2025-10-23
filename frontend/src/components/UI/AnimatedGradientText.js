import React from "react";

export function AnimatedGradientText({ children, className = "" }) {
  return (
    <span
      className={`animated-gradient-text ${className}`}
      style={{
        background: "linear-gradient(90deg,#ffaa40,#9c40ff,#ffaa40)",
        WebkitBackgroundClip: "text",
        color: "transparent",
        display: "inline-block",
      }}
    >
      {children}
    </span>
  );
}
