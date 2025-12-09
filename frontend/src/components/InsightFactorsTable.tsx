import React from "react";

interface Factor {
  label: string;
  value: string | number | null;
}

interface Props {
  title: string;
  factors: Factor[];
}

const InsightFactorsTable: React.FC<Props> = ({ title, factors }) => {
  return (
    <div className="bg-white rounded-xl p-4 shadow-md border border-gray-200 space-y-3">
      <h3 className="text-lg font-semibold">{title}</h3>
      <div className="space-y-2">
        {factors.map((f, index) => (
          <div
            key={index}
            className="flex justify-between border-b border-gray-100 pb-1"
          >
            <span className="text-gray-600">{f.label}</span>
            <span className="font-medium">{f.value ?? "N/A"}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default InsightFactorsTable;
