import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { useLocation } from "../hooks/useLocation";
import { api } from "../services/api";
import type { PestResponse } from "../types";
import LoadingSpinner from "../components/LoadingSpinner";
import ErrorMessage from "../components/ErrorMessage";
import Navbar from "../components/Navbar";

export const PestsPage: React.FC = () => {
  const navigate = useNavigate();
  const { logout } = useAuth();
  const { location } = useLocation();
  const [data, setData] = useState<PestResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [cropType, setCropType] = useState("wheat");

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  useEffect(() => {
    if (!location) return;

    const fetchData = async () => {
      setLoading(true);
      setError("");
      try {
        const result = await api.pests.assess({
          temp: 28,
          humidity: 65,
          crop_type: cropType,
        });
        setData(result);
      } catch (error) {
        console.error("Pests API error:", error);
        setError(
          "Failed to fetch pest and disease data. Please check backend connection."
        );
        setData(null);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [location, cropType]);

  if (!location) return <ErrorMessage message="Set location first" />;
  if (loading) return <LoadingSpinner />;

  const getRiskColor = (level: string) => {
    const colors = {
      Critical: "bg-red-100 border-red-500 text-red-800",
      High: "bg-orange-100 border-orange-500 text-orange-800",
      Medium: "bg-yellow-100 border-yellow-500 text-yellow-800",
      Low: "bg-green-100 border-green-500 text-green-800",
    };
    return colors[level as keyof typeof colors] || colors.Low;
  };

  const getRiskIcon = (level: string) => {
    const icons = { Critical: "🚨", High: "⚠️", Medium: "⚡", Low: "✅" };
    return icons[level as keyof typeof icons] || "✅";
  };

  return (
    <div className="min-h-screen bg-linear-to-br from-green-100 to-amber-100">
      <Navbar onLogout={handleLogout} />
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <h1 className="text-3xl font-bold mb-6">Pest & Disease Detection</h1>

        {error && <ErrorMessage message={error} />}

        {/* Crop Selection */}
        <div className="bg-white p-4 rounded-lg shadow mb-6">
          <label className="block text-sm font-medium mb-2">Select Crop</label>
          <select
            value={cropType}
            onChange={(e) => setCropType(e.target.value)}
            className="w-full md:w-64 p-2 border rounded"
          >
            <option value="wheat">Wheat</option>
            <option value="rice">Rice</option>
            <option value="corn">Corn</option>
            <option value="cotton">Cotton</option>
          </select>
        </div>

        {data && (
          <div className="space-y-6">
            {/* Pests */}
            <div>
              <h2 className="text-2xl font-bold mb-4">🐛 Detected Pests</h2>
              <div className="space-y-4">
                {data.pests.map((pest) => (
                  <div
                    key={pest.pest}
                    className={`p-6 rounded-lg border-2 ${getRiskColor(
                      pest.risk_level
                    )}`}
                  >
                    <div className="flex items-center justify-between mb-3">
                      <h3 className="text-xl font-bold">{pest.pest}</h3>
                      <div className="flex items-center gap-2">
                        <span className="text-2xl">
                          {getRiskIcon(pest.risk_level)}
                        </span>
                        <span className="font-bold">
                          {pest.risk_level} Risk
                        </span>
                      </div>
                    </div>

                    <div className="mb-3">
                      <p className="text-sm mb-1">Risk Score</p>
                      <div className="w-full bg-gray-200 rounded-full h-3">
                        <div
                          className={`h-3 rounded-full ${
                            pest.risk_score >= 0.7
                              ? "bg-red-600"
                              : pest.risk_score >= 0.4
                              ? "bg-yellow-600"
                              : "bg-green-600"
                          }`}
                          style={{ width: `${pest.risk_score * 100}%` }}
                        />
                      </div>
                      <p className="text-xs mt-1">
                        {(pest.risk_score * 100).toFixed(0)}%
                      </p>
                    </div>

                    <div className="grid md:grid-cols-2 gap-4">
                      <div>
                        <h4 className="font-semibold mb-2">Symptoms</h4>
                        <ul className="text-sm space-y-1">
                          {pest.symptoms.map((symptom, idx) => (
                            <li key={idx}>• {symptom}</li>
                          ))}
                        </ul>
                      </div>
                      <div>
                        <h4 className="font-semibold mb-2">Control Measures</h4>
                        <ul className="text-sm space-y-1">
                          {pest.control_measures.map((measure, idx) => (
                            <li key={idx}>✓ {measure}</li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Diseases */}
            <div>
              <h2 className="text-2xl font-bold mb-4">🦠 Detected Diseases</h2>
              <div className="space-y-4">
                {data.diseases.map((disease) => (
                  <div
                    key={disease.disease}
                    className={`p-6 rounded-lg border-2 ${getRiskColor(
                      disease.risk_level
                    )}`}
                  >
                    <div className="flex items-center justify-between mb-3">
                      <h3 className="text-xl font-bold">{disease.disease}</h3>
                      <div className="flex items-center gap-2">
                        <span className="text-2xl">
                          {getRiskIcon(disease.risk_level)}
                        </span>
                        <span className="font-bold">
                          {disease.risk_level} Risk
                        </span>
                      </div>
                    </div>

                    <div className="mb-3">
                      <p className="text-sm mb-1">Risk Score</p>
                      <div className="w-full bg-gray-200 rounded-full h-3">
                        <div
                          className={`h-3 rounded-full ${
                            disease.risk_score >= 0.7
                              ? "bg-red-600"
                              : disease.risk_score >= 0.4
                              ? "bg-yellow-600"
                              : "bg-green-600"
                          }`}
                          style={{ width: `${disease.risk_score * 100}%` }}
                        />
                      </div>
                      <p className="text-xs mt-1">
                        {(disease.risk_score * 100).toFixed(0)}%
                      </p>
                    </div>

                    <div className="grid md:grid-cols-2 gap-4">
                      <div>
                        <h4 className="font-semibold mb-2">Symptoms</h4>
                        <ul className="text-sm space-y-1">
                          {disease.symptoms.map((symptom, idx) => (
                            <li key={idx}>• {symptom}</li>
                          ))}
                        </ul>
                      </div>
                      <div>
                        <h4 className="font-semibold mb-2">Control Measures</h4>
                        <ul className="text-sm space-y-1">
                          {disease.control_measures.map((measure, idx) => (
                            <li key={idx}>✓ {measure}</li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Educational Insights - Always visible */}
            <div className="bg-linear-to-r from-red-50 to-pink-50 border border-red-200 rounded-xl p-6 shadow-lg">
              <h3 className="text-xl font-bold text-red-800 mb-4">
                🐛 Understanding Pest & Disease Risk Calculations
              </h3>
              <p className="text-red-700 leading-relaxed mb-4">
                Pest and disease risk assessment combines environmental
                monitoring, crop physiology, and epidemiological modeling to
                predict potential threats. The system integrates weather data,
                crop growth stages, and historical patterns to provide proactive
                management recommendations.
              </p>
              <div className="grid md:grid-cols-2 gap-6">
                <div className="bg-white/70 backdrop-blur-sm rounded-lg p-4">
                  <h4 className="font-semibold text-red-800 mb-2">
                    📊 Risk Score Calculation
                  </h4>
                  <p className="text-sm text-gray-700">
                    <strong>
                      Risk Score = (Environmental × 0.4) + (Host Susceptibility
                      × 0.3) + (Historical × 0.2) + (Current × 0.1)
                    </strong>
                    <br />
                    Environmental factors include temperature, humidity, and
                    rainfall patterns. Host susceptibility considers crop
                    variety resistance and growth stage.
                  </p>
                </div>
                <div className="bg-white/70 backdrop-blur-sm rounded-lg p-4">
                  <h4 className="font-semibold text-red-800 mb-2">
                    🐛 Pest Risk Assessment
                  </h4>
                  <p className="text-sm text-gray-700">
                    Based on pest biology models considering
                    temperature-dependent development rates, humidity
                    requirements for egg hatching, and crop phenology matching.
                    Risk levels: Low (&lt;30%), Medium (30-60%), High (60-80%),
                    Critical (&gt;80%).
                  </p>
                </div>
                <div className="bg-white/70 backdrop-blur-sm rounded-lg p-4">
                  <h4 className="font-semibold text-red-800 mb-2">
                    🦠 Disease Risk Modeling
                  </h4>
                  <p className="text-sm text-gray-700">
                    Uses epidemiological models incorporating infection cycles,
                    latent periods, and environmental suitability. Considers
                    leaf wetness duration, temperature optima for pathogen
                    growth, and crop stress factors that increase
                    susceptibility.
                  </p>
                </div>
                <div className="bg-white/70 backdrop-blur-sm rounded-lg p-4">
                  <h4 className="font-semibold text-red-800 mb-2">
                    🌿 Integrated Pest Management
                  </h4>
                  <p className="text-sm text-gray-700">
                    Combines biological, cultural, and chemical control methods
                    based on economic thresholds. Action recommended when pest
                    populations exceed 10-20% of economic injury levels,
                    considering natural enemy populations and crop value.
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
