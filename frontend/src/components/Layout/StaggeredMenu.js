import React from "react";
import "./StaggeredMenu.css";
import { AnimatedGradientText } from "../UI/AnimatedGradientText";

const StaggeredMenu = ({
  isFixed = false,
  items = [],
  socialItems = [],
  onMenuOpen,
  onMenuClose,
}) => {
  // Lightweight interactive menu placeholder using the user's visuals
  return (
    <div
      className={`staggered-menu-placeholder ${isFixed ? "fixed" : ""}`}
      aria-hidden={!items.length}
    >
      <div className="sm-header">Menu</div>
      <aside className="sm-panel">
        <ul>
          {items.map((it, i) => (
            <li key={i}>
              <a href={it.link}>{it.label}</a>
            </li>
          ))}
        </ul>
        <div style={{ marginTop: 16 }}>
          <AnimatedGradientText>Introducing Magic UI</AnimatedGradientText>
        </div>
      </aside>
    </div>
  );
};

export default StaggeredMenu;
