// React NDVI Analysis Component
import React, { useState, useEffect } from "react";
import axios from "axios";

const NDVIAnalysisComponent = () => {
  const [coordinates, setCoordinates] = useState({
    lat: 30.3398,
    lng: 76.3869,
  });
  const [ndviData, setNdviData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const analyzeNDVI = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await axios.post(
        "http://localhost:5001/api/ndvi/analyze",
        {
          latitude: parseFloat(coordinates.lat),
          longitude: parseFloat(coordinates.lng),
          use_real_data: false, // Set to true when you have Copernicus credentials
          days_back: 30,
          cloud_cover_max: 30,
        }
      );

      setNdviData(response.data);
    } catch (err) {
      setError(err.response?.data?.error || "Analysis failed");
    } finally {
      setLoading(false);
    }
  };

  const getLocation = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setCoordinates({
            lat: position.coords.latitude,
            lng: position.coords.longitude,
          });
        },
        (error) => {
          console.error("Error getting location:", error);
        }
      );
    }
  };

  return (
    <div className="ndvi-analysis-container">
      <div className="analysis-header">
        <h2>🛰️ NDVI Satellite Analysis</h2>
        <p>
          Real-time vegetation health analysis using Sentinel-2 satellite data
        </p>
      </div>

      <div className="coordinates-input">
        <div className="input-group">
          <label>Latitude:</label>
          <input
            type="number"
            value={coordinates.lat}
            onChange={(e) =>
              setCoordinates({ ...coordinates, lat: e.target.value })
            }
            step="0.0001"
            placeholder="e.g., 30.3398"
          />
        </div>
        <div className="input-group">
          <label>Longitude:</label>
          <input
            type="number"
            value={coordinates.lng}
            onChange={(e) =>
              setCoordinates({ ...coordinates, lng: e.target.value })
            }
            step="0.0001"
            placeholder="e.g., 76.3869"
          />
        </div>
        <button onClick={getLocation} className="btn-location">
          📍 Use My Location
        </button>
      </div>

      <div className="analysis-controls">
        <button
          onClick={analyzeNDVI}
          disabled={loading}
          className="btn-analyze"
        >
          {loading ? "🔄 Analyzing..." : "🚀 Analyze NDVI"}
        </button>
      </div>

      {error && <div className="error-message">❌ Error: {error}</div>}

      {ndviData && (
        <div className="ndvi-results">
          <div className="results-header">
            <h3>📊 NDVI Analysis Results</h3>
            <p>
              Location: {ndviData.coordinates.latitude}°,{" "}
              {ndviData.coordinates.longitude}°
            </p>
            <p>Data Source: {ndviData.data_source}</p>
          </div>

          <div className="ndvi-metrics">
            <div className="metric-card">
              <div
                className="metric-value"
                style={{ color: ndviData.health_analysis.color }}
              >
                {ndviData.ndvi.mean.toFixed(3)}
              </div>
              <div className="metric-label">Mean NDVI</div>
            </div>

            <div className="metric-card">
              <div className="metric-value health-score">
                {ndviData.health_analysis.health_score}
              </div>
              <div className="metric-label">Health Score</div>
            </div>

            <div className="metric-card">
              <div className="metric-value">
                {ndviData.health_analysis.category}
              </div>
              <div className="metric-label">Health Status</div>
            </div>
          </div>

          <div className="vegetation-coverage">
            <h4>🌱 Vegetation Coverage Analysis</h4>
            <div className="coverage-bars">
              <div className="coverage-item">
                <span>Dense Vegetation:</span>
                <div className="progress-bar">
                  <div
                    className="progress-fill dense"
                    style={{
                      width: `${ndviData.vegetation_coverage.dense_vegetation}%`,
                    }}
                  ></div>
                </div>
                <span>{ndviData.vegetation_coverage.dense_vegetation}%</span>
              </div>

              <div className="coverage-item">
                <span>Moderate Vegetation:</span>
                <div className="progress-bar">
                  <div
                    className="progress-fill moderate"
                    style={{
                      width: `${ndviData.vegetation_coverage.moderate_vegetation}%`,
                    }}
                  ></div>
                </div>
                <span>{ndviData.vegetation_coverage.moderate_vegetation}%</span>
              </div>

              <div className="coverage-item">
                <span>Sparse Vegetation:</span>
                <div className="progress-bar">
                  <div
                    className="progress-fill sparse"
                    style={{
                      width: `${ndviData.vegetation_coverage.sparse_vegetation}%`,
                    }}
                  ></div>
                </div>
                <span>{ndviData.vegetation_coverage.sparse_vegetation}%</span>
              </div>
            </div>
          </div>

          <div className="recommendations">
            <h4>💡 Recommendations</h4>
            <ul>
              {ndviData.recommendations.map((rec, index) => (
                <li key={index}>{rec}</li>
              ))}
            </ul>
          </div>

          <div className="detailed-stats">
            <h4>📈 Detailed Statistics</h4>
            <div className="stats-grid">
              <div className="stat-item">
                <span className="stat-label">Minimum NDVI:</span>
                <span className="stat-value">
                  {ndviData.ndvi.min.toFixed(3)}
                </span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Maximum NDVI:</span>
                <span className="stat-value">
                  {ndviData.ndvi.max.toFixed(3)}
                </span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Standard Deviation:</span>
                <span className="stat-value">
                  {ndviData.ndvi.std.toFixed(3)}
                </span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Valid Pixels:</span>
                <span className="stat-value">
                  {ndviData.ndvi.valid_pixels.toLocaleString()}
                </span>
              </div>
            </div>
          </div>

          <div className="visualization-section">
            <h4>🗺️ NDVI Visualization</h4>
            <img
              src={`http://localhost:5001/api/ndvi/visualization/${ndviData.coordinates.latitude}/${ndviData.coordinates.longitude}`}
              alt="NDVI Visualization"
              className="ndvi-visualization"
              onError={(e) => {
                e.target.style.display = "none";
              }}
            />
          </div>
        </div>
      )}

      <style jsx>{`
        .ndvi-analysis-container {
          max-width: 1200px;
          margin: 0 auto;
          padding: 20px;
          font-family: "Inter", sans-serif;
        }

        .analysis-header {
          text-align: center;
          margin-bottom: 30px;
        }

        .analysis-header h2 {
          color: #2d5a3d;
          font-size: 2.5rem;
          margin-bottom: 10px;
        }

        .coordinates-input {
          display: flex;
          gap: 20px;
          justify-content: center;
          align-items: end;
          margin-bottom: 20px;
          flex-wrap: wrap;
        }

        .input-group {
          display: flex;
          flex-direction: column;
          gap: 5px;
        }

        .input-group label {
          font-weight: 600;
          color: #374151;
        }

        .input-group input {
          padding: 12px;
          border: 2px solid #d1d5db;
          border-radius: 8px;
          font-size: 16px;
          width: 150px;
        }

        .btn-location {
          padding: 12px 20px;
          background: #6b7280;
          color: white;
          border: none;
          border-radius: 8px;
          cursor: pointer;
          font-size: 14px;
          transition: background 0.3s;
        }

        .btn-location:hover {
          background: #4b5563;
        }

        .btn-analyze {
          display: block;
          margin: 20px auto;
          padding: 15px 30px;
          background: #059669;
          color: white;
          border: none;
          border-radius: 12px;
          font-size: 18px;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.3s;
        }

        .btn-analyze:hover:not(:disabled) {
          background: #047857;
          transform: translateY(-2px);
        }

        .btn-analyze:disabled {
          background: #9ca3af;
          cursor: not-allowed;
          transform: none;
        }

        .error-message {
          background: #fef2f2;
          color: #dc2626;
          padding: 15px;
          border-radius: 8px;
          margin: 20px 0;
          border: 1px solid #fecaca;
        }

        .ndvi-results {
          background: white;
          border-radius: 16px;
          padding: 30px;
          margin-top: 30px;
          box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }

        .results-header {
          text-align: center;
          margin-bottom: 30px;
          padding-bottom: 20px;
          border-bottom: 2px solid #f3f4f6;
        }

        .ndvi-metrics {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
          gap: 20px;
          margin-bottom: 30px;
        }

        .metric-card {
          text-align: center;
          padding: 20px;
          background: #f8fafc;
          border-radius: 12px;
          border: 2px solid #e2e8f0;
        }

        .metric-value {
          font-size: 2.5rem;
          font-weight: 800;
          margin-bottom: 8px;
        }

        .metric-label {
          color: #64748b;
          font-weight: 500;
        }

        .vegetation-coverage {
          margin-bottom: 30px;
        }

        .coverage-item {
          display: flex;
          align-items: center;
          gap: 15px;
          margin-bottom: 15px;
        }

        .progress-bar {
          flex: 1;
          height: 20px;
          background: #e5e7eb;
          border-radius: 10px;
          overflow: hidden;
        }

        .progress-fill {
          height: 100%;
          transition: width 0.8s ease;
        }

        .progress-fill.dense {
          background: #059669;
        }
        .progress-fill.moderate {
          background: #84cc16;
        }
        .progress-fill.sparse {
          background: #eab308;
        }

        .recommendations ul {
          list-style: none;
          padding: 0;
        }

        .recommendations li {
          padding: 10px;
          margin-bottom: 8px;
          background: #f0fdf4;
          border-left: 4px solid #059669;
          border-radius: 6px;
        }

        .stats-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
          gap: 15px;
        }

        .stat-item {
          display: flex;
          justify-content: space-between;
          padding: 12px;
          background: #f8fafc;
          border-radius: 8px;
        }

        .stat-label {
          font-weight: 600;
          color: #374151;
        }

        .stat-value {
          font-weight: 700;
          color: #059669;
        }

        .ndvi-visualization {
          max-width: 100%;
          height: auto;
          border-radius: 12px;
          box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }

        h4 {
          color: #2d5a3d;
          margin-bottom: 15px;
          font-size: 1.25rem;
        }

        @media (max-width: 768px) {
          .coordinates-input {
            flex-direction: column;
            align-items: center;
          }

          .ndvi-metrics {
            grid-template-columns: 1fr;
          }

          .stats-grid {
            grid-template-columns: 1fr;
          }
        }
      `}</style>
    </div>
  );
};

export default NDVIAnalysisComponent;
