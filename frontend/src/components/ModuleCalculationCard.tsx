import React from "react";

interface ModuleCalculationCardProps {
  title: string;
  description: string;
  className?: string;
}

export const ModuleCalculationCard: React.FC<ModuleCalculationCardProps> = ({
  title,
  description,
  className = "",
}) => {
  return (
    <div
      className={`bg-linear-to-br from-blue-50 to-indigo-50 border border-blue-200 rounded-xl p-6 shadow-lg max-w-4xl mx-auto ${className}`}
    >
      <div className="flex items-center mb-4">
        <span className="text-3xl mr-3">🧮</span>
        <h3 className="text-xl font-bold text-blue-800">{title}</h3>
      </div>
      <div className="prose prose-sm max-w-none text-gray-700">
        <p className="leading-relaxed">{description}</p>
      </div>
    </div>
  );
};

export default ModuleCalculationCard;
