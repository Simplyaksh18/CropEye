import React from "react";

export function AnimatedThemeToggler() {
  // simple toggle button that animates
  return (
    <button
      aria-label="Animated theme toggle"
      className="animated-theme-toggler"
      style={{ padding: "6px 8px", borderRadius: 8 }}
    >
      🌗
    </button>
  );
}
