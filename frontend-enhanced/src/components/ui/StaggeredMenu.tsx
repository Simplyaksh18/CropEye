import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Menu, X } from "lucide-react";
import { cn } from "../../utils/cn";

interface MenuItem {
  label: string;
  onClick: () => void;
  icon?: React.ReactNode;
}

interface StaggeredMenuProps {
  items: MenuItem[];
  className?: string;
}

export const StaggeredMenu: React.FC<StaggeredMenuProps> = ({
  items,
  className = "",
}) => {
  const [isOpen, setIsOpen] = useState(false);
  // Guard document access for SSR
  const isDark =
    typeof document !== "undefined" &&
    document.documentElement.classList.contains("dark");

  const menuButtonColor = isDark ? "rgb(46, 185, 255)" : "rgb(41, 255, 44)";

  // Helper to convert `rgb(r, g, b)` to `rgba(r, g, b, alpha)` safely.
  const rgbToRgba = (rgb: string, alpha = 0.125) => {
    const m = rgb.match(/rgb\((\d+),\s*(\d+),\s*(\d+)\)/);
    if (!m) return rgb;
    const [, r, g, b] = m;
    return `rgba(${r}, ${g}, ${b}, ${alpha})`;
  };

  const menuVariants = {
    closed: {
      opacity: 0,
      transition: {
        staggerChildren: 0.05,
        staggerDirection: -1,
      },
    },
    open: {
      opacity: 1,
      transition: {
        staggerChildren: 0.07,
        delayChildren: 0.2,
      },
    },
  };

  const itemVariants = {
    closed: {
      opacity: 0,
      y: -20,
      transition: {
        duration: 0.2,
      },
    },
    open: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.3,
      },
    },
  };

  return (
    <div className={cn("relative", className)}>
      <motion.button
        onClick={() => setIsOpen(!isOpen)}
        className="relative p-3 rounded-full backdrop-blur-sm"
        style={{
          backgroundColor: rgbToRgba(menuButtonColor, 0.12),
          border: `2px solid ${menuButtonColor}`,
        }}
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.95 }}
      >
        <motion.div
          animate={{ rotate: isOpen ? 90 : 0 }}
          transition={{ duration: 0.3 }}
        >
          {isOpen ? (
            <X size={24} style={{ color: menuButtonColor }} />
          ) : (
            <Menu size={24} style={{ color: menuButtonColor }} />
          )}
        </motion.div>
      </motion.button>

      <AnimatePresence>
        {isOpen && (
          <motion.div
            className="absolute right-0 top-16 w-64 bg-white/10 dark:bg-black/30 backdrop-blur-lg rounded-2xl p-2 border border-white/20"
            variants={menuVariants}
            initial="closed"
            animate="open"
            exit="closed"
          >
            {items.map((item, index) => (
              <motion.button
                key={index}
                variants={itemVariants}
                onClick={() => {
                  item.onClick();
                  setIsOpen(false);
                }}
                className="w-full flex items-center gap-3 px-4 py-3 rounded-xl hover:bg-white/10 transition-colors"
                whileHover={{ x: 5 }}
              >
                {item.icon && (
                  <span style={{ color: menuButtonColor }}>{item.icon}</span>
                )}
                <span className="text-white font-medium">{item.label}</span>
              </motion.button>
            ))}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default StaggeredMenu;
