// src/components/layout/Footer.tsx
import React from "react";

const Footer: React.FC = () => {
  return (
    <footer className="bg-gray-100 dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 py-6">
      <div className="container mx-auto px-4 text-center">
        <p className="text-sm text-gray-600 dark:text-gray-400">
          © {new Date().getFullYear()} CropEye GIS Dashboard. All rights
          reserved.
        </p>
        <p className="text-xs text-gray-500 dark:text-gray-500 mt-2">
          Powered by satellite imagery and AI-driven analysis
        </p>
      </div>
    </footer>
  );
};

export default Footer;
