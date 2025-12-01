import React from "react";

interface ModuleCardProps {
  title: string;
  description: string;
  icon: string;
  color: string;
  onClick: () => void;
}

export const ModuleCard: React.FC<ModuleCardProps> = ({
  title,
  description,
  icon,
  color,
  onClick,
}) => {
  return (
    <div
      onClick={onClick}
      className="bg-white rounded-2xl shadow-lg border border-gray-200 p-8 hover:shadow-2xl hover:-translate-y-2 transition-all duration-300 cursor-pointer group overflow-hidden relative"
    >
      {/* Gradient overlay on hover */}
      <div className="absolute inset-0 bg-linear-to-br from-transparent to-gray-50 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>

      <div className="relative z-10">
        <div className="flex items-center mb-6">
          <div
            className={`w-16 h-16 ${color} rounded-xl flex items-center justify-center text-4xl mr-6 group-hover:scale-125 group-hover:rotate-12 transition-all duration-300 shadow-lg`}
          >
            {icon}
          </div>
          <h3 className="text-2xl font-bold text-gray-900 group-hover:text-gray-800 transition-colors">
            {title}
          </h3>
        </div>
        <p className="text-gray-600 leading-relaxed text-lg group-hover:text-gray-700 transition-colors">
          {description}
        </p>

        {/* Action indicator */}
        <div className="mt-6 flex items-center text-sm text-gray-500 group-hover:text-gray-700 transition-colors">
          <span>Explore Module</span>
          <svg
            className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 5l7 7-7 7"
            />
          </svg>
        </div>
      </div>
    </div>
  );
};

export default ModuleCard;
