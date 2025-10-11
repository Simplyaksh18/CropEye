import React from "react";
import {
  Leaf,
  Droplets,
  Thermometer,
  Sprout,
  TrendingUp,
  BarChart3,
} from "lucide-react";
import "./AnalysisResults.css";

const MetricCard = ({
  icon: Icon,
  title,
  value,
  unit,
  status,
  description,
}) => (
  <div className={`metric-card ${status}`}>
    <div className="metric-icon">
      <Icon size={24} />
    </div>
    <div className="metric-content">
      <h4>{title}</h4>
      <div className="metric-value">
        {value} <span className="unit">{unit}</span>
      </div>
      <p className="metric-description">{description}</p>
    </div>
  </div>
);

const CropRecommendation = ({ crop, suitability, reasoning }) => (
  <div className="crop-recommendation">
    <div className="crop-info">
      <h4>{crop}</h4>
      <div className="suitability-bar">
        <div
          className="suitability-fill"
          style={{ width: `${suitability * 100}%` }}
        ></div>
      </div>
      <span className="suitability-score">
        {(suitability * 100).toFixed(0)}% suitable
      </span>
    </div>
    <p className="crop-reasoning">{reasoning}</p>
  </div>
);

const AnalysisResults = ({ data, location }) => {
  const {
    ndvi_analysis,
    soil_moisture_analysis,
    weather_data,
    crop_recommendations,
    analysis_metadata,
  } = data;

  // Normalize NDVI fields so component works with both legacy and new backend payloads.
  const normalizedNdvi = (() => {
    // prefer explicit normalized object (legacy/front-side), otherwise fall back to backend fields
    const avg_ndvi =
      ndvi_analysis?.avg_ndvi ??
      data?.ndvi?.mean ??
      data?.ndvi_report?.latestValue ??
      null;
    const vegetation_percentage =
      ndvi_analysis?.vegetation_percentage ??
      data?.vegetation_coverage ??
      data?.vegetation_percentage ??
      null;
    const status =
      ndvi_analysis?.status ??
      data?.health_analysis?.status ??
      data?.ndvi_report?.status ??
      null;
    const healthy_vegetation_percentage =
      ndvi_analysis?.healthy_vegetation_percentage ??
      data?.health_analysis?.healthy_percentage ??
      null;
    const source =
      ndvi_analysis?.source ?? (data?.ndvi ? "satellite" : "unknown");

    return {
      avg_ndvi,
      vegetation_percentage,
      status,
      healthy_vegetation_percentage,
      source,
    };
  })();

  const getStatusClass = (value, thresholds) => {
    if (value >= thresholds.good) return "good";
    if (value >= thresholds.moderate) return "moderate";
    return "poor";
  };

  return (
    <div className="analysis-results">
      {/* Key Metrics Grid */}
      <div className="metrics-grid">
        <MetricCard
          icon={Leaf}
          title="Vegetation Health (NDVI)"
          value={
            normalizedNdvi?.avg_ndvi !== null &&
            normalizedNdvi?.avg_ndvi !== undefined
              ? Number(normalizedNdvi.avg_ndvi).toFixed(3)
              : "N/A"
          }
          unit=""
          status={getStatusClass(normalizedNdvi?.avg_ndvi || 0, {
            good: 0.6,
            moderate: 0.3,
          })}
          description={`${
            normalizedNdvi?.status || "Unknown"
          } vegetation condition`}
        />

        <MetricCard
          icon={Droplets}
          title="Soil Moisture"
          value={soil_moisture_analysis?.soil_moisture?.toFixed(3) || "N/A"}
          unit="fraction"
          status={getStatusClass(soil_moisture_analysis?.soil_moisture || 0, {
            good: 0.4,
            moderate: 0.25,
          })}
          description={`${
            soil_moisture_analysis?.dry_percentage?.toFixed(1) || 0
          }% area is dry`}
        />

        <MetricCard
          icon={Thermometer}
          title="Temperature"
          value={weather_data?.temperature?.toFixed(1) || "N/A"}
          unit="°C"
          status={getStatusClass(weather_data?.temperature || 0, {
            good: 25,
            moderate: 20,
          })}
          description={`${weather_data?.humidity?.toFixed(0) || 0}% humidity`}
        />

        <MetricCard
          icon={Sprout}
          title="Recommended Crops"
          value={crop_recommendations?.recommended_crops?.length || 0}
          unit="options"
          status="good"
          description={`${
            (crop_recommendations?.confidence * 100)?.toFixed(0) || 0
          }% confidence`}
        />
      </div>

      {/* Detailed Analysis Sections */}
      <div className="analysis-sections">
        {/* NDVI Analysis */}
        {ndvi_analysis && (
          <div className="analysis-section">
            <h3>
              <Leaf size={20} />
              Vegetation Analysis
            </h3>
            <div className="section-content">
              <div className="analysis-summary">
                <p>
                  <strong>Average NDVI:</strong>{" "}
                  {normalizedNdvi.avg_ndvi !== null &&
                  normalizedNdvi.avg_ndvi !== undefined
                    ? Number(normalizedNdvi.avg_ndvi).toFixed(3)
                    : "N/A"}{" "}
                  ({normalizedNdvi.status || "N/A"})
                </p>
                <p>
                  <strong>Vegetation Coverage:</strong>{" "}
                  {normalizedNdvi.vegetation_percentage !== null &&
                  normalizedNdvi.vegetation_percentage !== undefined
                    ? Number(normalizedNdvi.vegetation_percentage).toFixed(1)
                    : "N/A"}
                  % of analyzed area
                </p>
                <p>
                  <strong>Healthy Vegetation:</strong>{" "}
                  {normalizedNdvi.healthy_vegetation_percentage !== null &&
                  normalizedNdvi.healthy_vegetation_percentage !== undefined
                    ? Number(
                        normalizedNdvi.healthy_vegetation_percentage
                      ).toFixed(1)
                    : "N/A"}
                  % in good condition
                </p>
              </div>

              {ndvi_analysis.source === "satellite" && (
                <div className="data-source">
                  <small>📡 Data from Sentinel-2 satellite imagery</small>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Soil Moisture Analysis */}
        {soil_moisture_analysis && (
          <div className="analysis-section">
            <h3>
              <Droplets size={20} />
              Soil Moisture Analysis
            </h3>
            <div className="section-content">
              <div className="moisture-breakdown">
                <div className="moisture-stats">
                  <div className="stat">
                    <span className="label">Dry Areas:</span>
                    <span className="value dry">
                      {soil_moisture_analysis.dry_percentage?.toFixed(1)}%
                    </span>
                  </div>
                  <div className="stat">
                    <span className="label">Moderate:</span>
                    <span className="value moderate">
                      {(
                        100 -
                        (soil_moisture_analysis.dry_percentage || 0) -
                        (soil_moisture_analysis.wet_percentage || 0)
                      ).toFixed(1)}
                      %
                    </span>
                  </div>
                  <div className="stat">
                    <span className="label">Wet Areas:</span>
                    <span className="value wet">
                      {soil_moisture_analysis.wet_percentage?.toFixed(1)}%
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Weather Information */}
        {weather_data && (
          <div className="analysis-section">
            <h3>
              <Thermometer size={20} />
              Weather Conditions
            </h3>
            <div className="section-content">
              <div className="weather-grid">
                <div className="weather-item">
                  <span className="weather-label">Temperature:</span>
                  <span className="weather-value">
                    {weather_data.temperature?.toFixed(1)}°C
                  </span>
                </div>
                <div className="weather-item">
                  <span className="weather-label">Humidity:</span>
                  <span className="weather-value">
                    {weather_data.humidity?.toFixed(0)}%
                  </span>
                </div>
                <div className="weather-item">
                  <span className="weather-label">Rainfall:</span>
                  <span className="weather-value">
                    {weather_data.rainfall?.toFixed(1)}mm
                  </span>
                </div>
                <div className="weather-item">
                  <span className="weather-label">Conditions:</span>
                  <span className="weather-value">
                    {weather_data.conditions}
                  </span>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Crop Recommendations */}
        {crop_recommendations && (
          <div className="analysis-section">
            <h3>
              <Sprout size={20} />
              Crop Recommendations
            </h3>
            <div className="section-content">
              <div className="recommendations-list">
                {crop_recommendations.detailed_recommendations?.map(
                  (rec, index) => (
                    <CropRecommendation
                      key={index}
                      crop={rec.crop}
                      suitability={rec.suitability}
                      reasoning={rec.reason}
                    />
                  )
                ) ||
                  crop_recommendations.recommended_crops?.map((crop, index) => (
                    <CropRecommendation
                      key={index}
                      crop={crop}
                      suitability={0.8}
                      reasoning="Based on current soil and weather conditions"
                    />
                  ))}
              </div>

              <div className="soil-type">
                <p>
                  <strong>Detected Soil Type:</strong>{" "}
                  {crop_recommendations.soil_type}
                </p>
                <p>
                  <strong>Recommendation Confidence:</strong>{" "}
                  {(crop_recommendations.confidence * 100)?.toFixed(0)}%
                </p>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Analysis Metadata */}
      {analysis_metadata && (
        <div className="analysis-metadata">
          <h4>Analysis Details</h4>
          <div className="metadata-grid">
            <div className="metadata-item">
              <span>Analysis ID:</span>
              <span>{analysis_metadata.analysis_id}</span>
            </div>
            <div className="metadata-item">
              <span>Processing Time:</span>
              <span>
                {new Date(analysis_metadata.timestamp).toLocaleString()}
              </span>
            </div>
            <div className="metadata-item">
              <span>Data Sources:</span>
              <span>
                {analysis_metadata.data_sources?.satellite
                  ? "📡 Satellite"
                  : "🔬 Simulated"}{" "}
                + Weather
              </span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AnalysisResults;
