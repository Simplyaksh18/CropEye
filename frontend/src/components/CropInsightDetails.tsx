import React from "react";

interface Props {
  ph: number;
  ndvi: number;
  rainfall: number;
  temp: number;
}

const CropInsightDetails: React.FC<Props> = ({ ph, ndvi, rainfall, temp }) => {
  const getPHInsight = () => {
    if (ph >= 6 && ph <= 7.5)
      return "Soil pH is optimal for plant nutrient uptake.";
    if (ph > 7.5)
      return "Slightly alkaline pH — may reduce nutrient absorption.";
    return "Soil is acidic — lime may be required.";
  };

  const getNDVIInsight = () => {
    if (ndvi >= 0.55) return "Strong vegetation health detected.";
    if (ndvi >= 0.4) return "Moderate vegetation — monitor crop conditions.";
    return "Vegetation stress — soil/water issues likely.";
  };

  const getRainInsight = () => {
    if (rainfall >= 500) return "Good rainfall to support healthy growth.";
    if (rainfall >= 200) return "Low rainfall — irrigation required.";
    return "Very low rainfall — strong crop limitations.";
  };

  const getTempInsight = () => {
    if (temp >= 20 && temp <= 34) return "Ideal temperature for crop growth.";
    if (temp < 20) return "Temperature too low — slow growth expected.";
    return "High heat — crop stress risk.";
  };

  return (
    <div className="bg-green-100 p-4 rounded-xl mt-4 shadow-md">
      <h2 className="text-green-900 font-bold text-lg mb-3">
        🌱 Why this recommendation?
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        <div className="bg-white p-3 rounded-lg shadow">
          <h3 className="font-semibold text-green-800">📌 Soil pH Insight</h3>
          <p className="text-sm text-gray-700 mt-1">{getPHInsight()}</p>
        </div>

        <div className="bg-white p-3 rounded-lg shadow">
          <h3 className="font-semibold text-green-800">🍃 Vegetation (NDVI)</h3>
          <p className="text-sm text-gray-700 mt-1">{getNDVIInsight()}</p>
        </div>

        <div className="bg-white p-3 rounded-lg shadow">
          <h3 className="font-semibold text-green-800">🌧 Rainfall</h3>
          <p className="text-sm text-gray-700 mt-1">{getRainInsight()}</p>
        </div>

        <div className="bg-white p-3 rounded-lg shadow">
          <h3 className="font-semibold text-green-800">🌡 Temperature</h3>
          <p className="text-sm text-gray-700 mt-1">{getTempInsight()}</p>
        </div>
      </div>
    </div>
  );
};

export default CropInsightDetails;
