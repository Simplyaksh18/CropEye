import React from "react";

interface Props {
  title?: string;
  steps?: string[];
}

const defaultSteps = [
  "Fetching satellite NDVI…",
  "Analyzing soil health…",
  "Checking weather conditions…",
  "Detecting pest threats…",
  "Calculating irrigation requirements…",
];

const DetailedMultiLoader: React.FC<Props> = ({ title, steps }) => {
  const s = steps && steps.length > 0 ? steps : defaultSteps;
  return (
    <div className="flex flex-col items-center p-6 space-y-3">
      {title && (
        <div className="text-lg font-semibold text-gray-700">{title}</div>
      )}
      <div className="loader border-t-green-600 border-4 w-12 h-12 rounded-full animate-spin"></div>

      {s.map((step, i) => (
        <p
          key={i}
          className={`text-sm ${
            i === 0 ? "font-semibold text-green-700" : "text-gray-600"
          } animate-pulse`}
        >
          {step}
        </p>
      ))}
    </div>
  );
};

export default DetailedMultiLoader;
