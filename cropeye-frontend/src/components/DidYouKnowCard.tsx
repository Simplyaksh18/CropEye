import React from "react";

interface DidYouKnowCardProps {
  facts: string[];
  className?: string;
}

export const DidYouKnowCard: React.FC<DidYouKnowCardProps> = ({
  facts,
  className = "",
}) => {
  return (
    <div
      className={`fixed right-4 top-1/2 transform -translate-y-1/2 bg-linear-to-br from-green-50 to-amber-50 border border-green-200 rounded-xl p-4 shadow-lg max-w-xs z-50 ${className}`}
    >
      <div className="flex items-center mb-3">
        <span className="text-xl mr-2">💡</span>
        <h3 className="text-sm font-bold text-green-800">Did You Know</h3>
      </div>
      <div className="space-y-2">
        {facts.map((fact, index) => (
          <div
            key={index}
            className="bg-white/70 backdrop-blur-sm rounded-lg p-2 border border-green-100"
          >
            <p className="text-xs text-gray-700 leading-relaxed">{fact}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default DidYouKnowCard;
