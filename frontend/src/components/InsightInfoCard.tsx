import React from "react";

interface Props {
  title: string;
  facts: string[];
}

const InsightInfoCard: React.FC<Props> = ({ title, facts }) => {
  return (
    <div className="bg-green-50 border border-green-300 rounded-xl p-4 shadow-sm space-y-2">
      <h4 className="text-lg font-semibold text-green-700 mb-1">{title}</h4>
      <ul className="space-y-1 text-green-900 text-sm leading-tight">
        {facts.map((fact, index) => (
          <li key={index} className="flex items-start gap-1">
            <span>{fact}</span>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default InsightInfoCard;
