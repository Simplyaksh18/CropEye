import React from "react";

interface Props {
  title: string;
  value: string | number;
  emoji?: string;
  color?: string; // tailwind color for score badge
  description?: string;
}

const InsightCard: React.FC<Props> = ({
  title,
  value,
  emoji,
  color = "bg-green-600",
  description,
}) => {
  return (
    <div className="rounded-xl bg-white p-4 shadow-md space-y-2 border border-gray-200">
      <div className="flex justify-between items-center">
        <h3 className="font-semibold text-lg">{title}</h3>
        {emoji && <span className="text-2xl">{emoji}</span>}
      </div>

      <span
        className={`inline-flex px-3 py-1 rounded-full text-white font-semibold ${color}`}
      >
        {value}
      </span>

      {description && (
        <p className="text-gray-600 text-sm leading-tight">{description}</p>
      )}
    </div>
  );
};

export default InsightCard;
