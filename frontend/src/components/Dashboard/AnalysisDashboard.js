import React, { useState } from "react";
import { useLocation } from "../../context/LocationContext";
import {
  Leaf,
  Thermometer,
  Droplets,
  Wind,
  Bug,
  TrendingUp,
  Clock,
  ChevronDown,
  ChevronUp,
  AlertTriangle,
} from "lucide-react";
import "./AnalysisResults.css";

const AnalysisDashboard = () => {
  const { userLocation, analysisData, loading } = useLocation();
  const [expandedSections, setExpandedSections] = useState({
    weather: false,
    soil: false,
    crops: false,
    pests: false,
  });

  const toggleSection = (section) => {
    setExpandedSections((prev) => ({
      ...prev,
      [section]: !prev[section],
    }));
  };

  if (!userLocation) {
    return (
      <div className="analysis-card">
        <div className="no-data">
          <Leaf className="no-data-icon" />
          <h3>No Location Selected</h3>
          <p>Please select your location above to get analysis results.</p>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="analysis-card">
        <div className="loading-analysis">
          <div className="loading-spinner"></div>
          <h3>Analyzing Location...</h3>
          <p>Processing satellite data and generating insights...</p>
        </div>
      </div>
    );
  }

  if (!analysisData) {
    return (
      <div className="analysis-card">
        <div className="no-data">
          <TrendingUp className="no-data-icon" />
          <h3>Ready for Analysis</h3>
          <p>Your location is set. Analysis will start automatically.</p>
        </div>
      </div>
    );
  }

  const {
    ndvi_analysis: legacy_ndvi_analysis,
    weather_data,
    soil_fertility,
    crop_recommendations,
    pest_alerts,
  } = analysisData;

  // Provide normalized ndvi_analysis for UI: prefer new backend `ndvi` + `vegetation_coverage`
  const ndvi_analysis = legacy_ndvi_analysis || {
    vegetation_percentage:
      analysisData?.vegetation_coverage ??
      analysisData?.vegetation_percentage ??
      null,
    status: analysisData?.health_analysis?.status ?? null,
    value: analysisData?.ndvi?.mean ?? null,
  };

  return (
    <div className="analysis-dashboard">
      <div className="analysis-header">
        <h2>Crop Analysis Results</h2>
        <p className="analysis-timestamp">
          Last updated:{" "}
          {analysisData.analysis_timestamp
            ? new Date(analysisData.analysis_timestamp).toLocaleString()
            : "Just now"}
        </p>
      </div>

      {/* NDVI Analysis */}
      <div className="analysis-section ndvi-section">
        <div className="section-header">
          <Leaf className="section-icon" />
          <h3>Vegetation Health (NDVI)</h3>
        </div>
        <div className="ndvi-content">
          <div className="ndvi-main">
            <div className="ndvi-value">
              {ndvi_analysis?.vegetation_percentage ?? 0}%
            </div>
            <div className="ndvi-status">
              {ndvi_analysis?.status || "Unknown"}
            </div>
          </div>
          <div className="ndvi-details">
            <span>
              NDVI Value:{" "}
              {ndvi_analysis?.value ? ndvi_analysis.value.toFixed(3) : "N/A"}
            </span>
          </div>
        </div>
      </div>

      {/* Soil Fertility */}
      <div className="analysis-section">
        <div className="section-header" onClick={() => toggleSection("soil")}>
          <TrendingUp className="section-icon" />
          <h3>Soil Fertility</h3>
          {expandedSections.soil ? <ChevronUp /> : <ChevronDown />}
        </div>

        {soil_fertility && (
          <div className="soil-summary">
            <div className="fertility-score">
              <span className="score-value">
                {soil_fertility.fertility_score}%
              </span>
              <span className="score-label">Fertility Score</span>
            </div>
          </div>
        )}

        {expandedSections.soil && soil_fertility && (
          <div className="section-content">
            <div className="soil-grid">
              <div className="soil-metric">
                <span className="metric-label">pH Level</span>
                <span className="metric-value">{soil_fertility.ph_level}</span>
              </div>
              <div className="soil-metric">
                <span className="metric-label">Nitrogen</span>
                <span className="metric-value">
                  {soil_fertility.nitrogen} ppm
                </span>
              </div>
              <div className="soil-metric">
                <span className="metric-label">Phosphorus</span>
                <span className="metric-value">
                  {soil_fertility.phosphorus} ppm
                </span>
              </div>
              <div className="soil-metric">
                <span className="metric-label">Potassium</span>
                <span className="metric-value">
                  {soil_fertility.potassium} ppm
                </span>
              </div>
              <div className="soil-metric">
                <span className="metric-label">Organic Matter</span>
                <span className="metric-value">
                  {soil_fertility.organic_matter}%
                </span>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Weather Data */}
      <div className="analysis-section">
        <div
          className="section-header"
          onClick={() => toggleSection("weather")}
        >
          <Thermometer className="section-icon" />
          <h3>Hourly Weather Forecast</h3>
          {expandedSections.weather ? <ChevronUp /> : <ChevronDown />}
        </div>

        {weather_data?.hourly && weather_data.hourly.length > 0 && (
          <div className="weather-summary">
            <div className="current-weather">
              <Thermometer className="weather-icon" />
              <span>{weather_data.hourly[0].temperature}°C</span>
              <Droplets className="weather-icon" />
              <span>{weather_data.hourly[0].humidity}%</span>
              <Wind className="weather-icon" />
              <span>{weather_data.hourly[0].wind_speed} m/s</span>
            </div>
          </div>
        )}

        {expandedSections.weather && weather_data?.hourly && (
          <div className="section-content">
            <div className="weather-hourly">
              {weather_data.hourly.slice(0, 12).map((hour, index) => (
                <div key={index} className="weather-hour">
                  <div className="hour-time">
                    <Clock size={14} />
                    {new Date(hour.datetime).toLocaleTimeString([], {
                      hour: "2-digit",
                      minute: "2-digit",
                    })}
                  </div>
                  <div className="hour-temp">{hour.temperature}°C</div>
                  <div className="hour-details">
                    <span>💧 {hour.precipitation}mm</span>
                    <span>🌧️ {hour.rain_probability}%</span>
                    <span>💨 {hour.wind_speed}m/s</span>
                    <span>💧 {hour.dew_point?.toFixed(1)}°C</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Crop Recommendations */}
      <div className="analysis-section">
        <div className="section-header" onClick={() => toggleSection("crops")}>
          <Leaf className="section-icon" />
          <h3>Crop Recommendations</h3>
          {expandedSections.crops ? <ChevronUp /> : <ChevronDown />}
        </div>

        {crop_recommendations && crop_recommendations.length > 0 && (
          <div className="crops-summary">
            <span>
              Top Recommendation:{" "}
              <strong>{crop_recommendations[0].crop}</strong>
            </span>
          </div>
        )}

        {expandedSections.crops && crop_recommendations && (
          <div className="section-content">
            <div className="crops-list">
              {crop_recommendations.map((crop, index) => (
                <div key={index} className="crop-item">
                  <div className="crop-header">
                    <h4>{crop.crop}</h4>
                    <span
                      className={`suitability ${crop.suitability
                        .toLowerCase()
                        .replace("-", "")}`}
                    >
                      {crop.suitability}
                    </span>
                  </div>
                  <div className="crop-details">
                    <span>🌾 Yield: {crop.yield_potential}</span>
                    <span>📅 Season: {crop.growing_season}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Pest Alerts */}
      <div className="analysis-section">
        <div className="section-header" onClick={() => toggleSection("pests")}>
          <Bug className="section-icon" />
          <h3>Pest Alerts</h3>
          {expandedSections.pests ? <ChevronUp /> : <ChevronDown />}
        </div>

        {pest_alerts && pest_alerts.length > 0 && (
          <div className="pests-summary">
            <AlertTriangle className="alert-icon" />
            <span>{pest_alerts.length} alert(s) for your area</span>
          </div>
        )}

        {expandedSections.pests && pest_alerts && (
          <div className="section-content">
            <div className="pests-list">
              {pest_alerts.map((alert, index) => (
                <div key={index} className="pest-item">
                  <div className="pest-header">
                    <h4>{alert.pest}</h4>
                    <span
                      className={`severity ${alert.severity.toLowerCase()}`}
                    >
                      {alert.severity}
                    </span>
                  </div>
                  <p className="pest-description">{alert.description}</p>
                  <p className="pest-recommendation">
                    <strong>Recommendation:</strong> {alert.recommendation}
                  </p>
                  <span className="pest-updated">
                    Updated: {new Date(alert.last_updated).toLocaleDateString()}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AnalysisDashboard;
