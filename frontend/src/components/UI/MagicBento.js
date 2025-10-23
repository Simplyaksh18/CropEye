import React from "react";
import "./MagicBento.css";

export default function MagicBento({ children, className = "" }) {
  return (
    <div className={`magic-bento ${className}`} data-magicbento>
      <div className="magic-bento-inner">{children}</div>
    </div>
  );
}
