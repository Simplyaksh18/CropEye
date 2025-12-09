import { useState, useEffect, useCallback } from "react";
import { useLocation } from "../hooks/useLocation";
import api from "../services/api";
import Navbar from "../components/Navbar";
import LoadingSpinner from "../components/LoadingSpinner";
import ErrorMessage from "../components/ErrorMessage";

interface SoilResponse {
  soil_properties?: {
    ph?: { value: number; classification: string };
    organic_carbon?: { value: number; classification: string };
    texture?: { value: string };
    moisture?: { value: number };
  };
  ndvi_correlation?: {
    ndvi_value?: number;
    health_analysis?: {
      category?: string;
      health_score?: number;
      description?: string;
    };
  };
  confidence_score?: number;
  management_recommendations?: {
    immediate?: string[];
    seasonal?: string[];
    long_term?: string[];
  };
}

export default function SoilPage() {
  const { location } = useLocation();
  const [data, setData] = useState<SoilResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const fetchData = useCallback(async () => {
    if (!location || location.lat == null || location.lng == null) return;
    setLoading(true);
    setError("");
    try {
      const result = await api.soil.analyze(location.lat, location.lng, {
        coordinate_source: "manual",
        include_ndvi: true,
        analysis_depth: "comprehensive",
      });
      setData(result);
    } catch (error) {
      console.error("Soil API error:", error);
      setError("Failed to fetch soil data. Please check backend connection.");
      setData(null);
    } finally {
      setLoading(false);
    }
  }, [location]);

  useEffect(() => {
    fetchData();
  }, [location, fetchData]);

  const getPHRecommendations = (ph: number) => {
    if (ph < 6) {
      return [
        "Apply agricultural lime to raise soil pH gradually",
        "Use acid-tolerant crops like potatoes, blueberries, or rhododendrons",
        "Test soil pH annually to monitor changes",
        "Avoid over-liming which can cause nutrient imbalances",
      ];
    } else if (ph > 7.5) {
      return [
        "Apply elemental sulfur to lower soil pH gradually",
        "Use alkaline-tolerant crops like asparagus, cabbage, or clover",
        "Consider using acidifying fertilizers if needed",
        "Monitor pH regularly as alkaline soils can fluctuate",
      ];
    } else {
      return [
        "Maintain current pH level with balanced fertilization",
        "Most crops will thrive in this optimal pH range",
        "Continue regular soil testing to ensure stability",
        "Focus on organic matter addition for soil health",
      ];
    }
  };

  if (!location) return <ErrorMessage message="Set location first" />;

  const soil = data?.soil_properties;
  const ndvi = data?.ndvi_correlation;
  const confidence = data?.confidence_score;
  const allRecommendations = soil?.ph
    ? getPHRecommendations(soil.ph.value)
    : [];

  return (
    <div className="min-h-screen bg-linear-to-br from-amber-50 to-yellow-50">
      <Navbar />
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <h1 className="text-3xl font-bold text-green-700 mb-3">
          🌱 Soil Analysis
        </h1>
        <p className="text-gray-600 mb-6">
          Comprehensive soil health analysis powered by Copernicus data.
        </p>

        {loading && <LoadingSpinner message="Analyzing soil properties..." />}
        {error && <ErrorMessage message={error} />}

        {!loading && !error && data && (
          <div className="space-y-6">
            {/* Main Soil Properties Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* pH */}
              {soil?.ph && (
                <div className="bg-white p-6 rounded-lg shadow border">
                  <h2 className="text-lg font-semibold mb-4">Soil pH</h2>
                  <p className="text-4xl font-bold text-purple-600">
                    {soil.ph.value.toFixed(1)}
                  </p>
                  <p className="text-sm text-gray-600 mt-2">
                    {soil.ph.value < 6
                      ? "Acidic"
                      : soil.ph.value > 7.5
                      ? "Alkaline"
                      : "Neutral (Ideal)"}
                  </p>
                </div>
              )}

              {/* Organic Carbon */}
              {soil?.organic_carbon && (
                <div className="bg-white p-6 rounded-lg shadow border">
                  <h3 className="text-sm text-gray-600 mb-2">Organic Carbon</h3>
                  <p className="text-3xl font-bold text-green-600">
                    {soil.organic_carbon.value.toFixed(2)}
                  </p>
                  <p className="text-sm text-gray-600 mt-1">%</p>
                  <p className="text-sm font-medium text-green-600 mt-2">
                    {soil.organic_carbon.classification}
                  </p>
                </div>
              )}

              {/* Texture */}
              {soil?.texture && (
                <div className="bg-white p-6 rounded-lg shadow border">
                  <h3 className="text-sm text-gray-600 mb-2">Soil Texture</h3>
                  <p className="text-2xl font-bold text-gray-800">
                    {soil.texture.value}
                  </p>
                </div>
              )}

              {/* Confidence */}
              {confidence !== undefined && (
                <div className="bg-white p-6 rounded-lg shadow border">
                  <h3 className="text-sm text-gray-600 mb-2">
                    Data Confidence
                  </h3>
                  <p className="text-2xl font-bold text-green-600">
                    {(confidence * 100).toFixed(0)}%
                  </p>
                  <p className="text-xs text-gray-500 mt-1">
                    Source: Copernicus Soil Repository
                  </p>
                </div>
              )}
            </div>

            {/* NDVI Health - Full Width */}
            {ndvi?.ndvi_value !== undefined && (
              <div className="bg-white p-6 rounded-lg shadow border">
                <h3 className="text-sm text-gray-600 mb-2">
                  Vegetation Health (NDVI)
                </h3>
                <p className="text-2xl font-bold text-blue-600">
                  {ndvi.ndvi_value.toFixed(3)}
                </p>
                <p className="text-sm text-gray-600 mt-2">
                  {ndvi.health_analysis?.category || "Unknown"}
                </p>
              </div>
            )}

            {/* Recommendations */}
            {allRecommendations.length > 0 && (
              <div className="bg-blue-50 border border-blue-200 p-6 rounded-lg">
                <h3 className="font-semibold text-blue-900 mb-3">
                  Recommendations
                </h3>
                <ul className="space-y-2">
                  {allRecommendations.map((rec, idx) => (
                    <li key={idx} className="flex items-start text-blue-800">
                      <span className="mr-2">✓</span>
                      <span>{rec}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Educational Insights - Always visible */}
            <div className="bg-linear-to-r from-amber-50 to-orange-50 border border-amber-200 rounded-xl p-6 shadow-lg">
              <h3 className="text-xl font-bold text-amber-800 mb-4">
                🌱 Understanding Soil Analysis Calculations
              </h3>
              <p className="text-amber-700 leading-relaxed mb-4">
                Our soil analysis system employs advanced spectroscopic
                techniques and machine learning algorithms to provide
                comprehensive nutrient profiling. The pH measurement uses
                electrochemical sensors calibrated against standard buffers,
                while organic carbon analysis combines chemical extraction
                methods with optical spectroscopy for precise quantification.
                Soil texture classification integrates particle size
                distribution data with pedological databases, enabling accurate
                water retention and drainage predictions. This detailed analysis
                supports precision fertilization strategies that optimize crop
                nutrition while minimizing environmental impact.
              </p>
              <div className="grid md:grid-cols-2 gap-6">
                <div className="bg-white/70 backdrop-blur-sm rounded-lg p-4">
                  <h4 className="font-semibold text-amber-800 mb-2">
                    🧪 pH Measurement
                  </h4>
                  <p className="text-sm text-gray-700">
                    <strong>pH = -log[H⁺]</strong>
                    <br />
                    Measured using calibrated electrodes in soil-water slurry
                    (1:2.5 ratio). Values 6.0-7.0 are optimal for most crops,
                    affecting nutrient availability and microbial activity.
                  </p>
                </div>
                <div className="bg-white/70 backdrop-blur-sm rounded-lg p-4">
                  <h4 className="font-semibold text-amber-800 mb-2">
                    🧪 Organic Carbon Analysis
                  </h4>
                  <p className="text-sm text-gray-700">
                    <strong>Walkley-Black method</strong>
                    <br />
                    Wet oxidation with potassium dichromate and sulfuric acid.
                    Results expressed as percentage of soil organic matter.
                    Essential for soil fertility and structure assessment.
                  </p>
                </div>
                <div className="bg-white/70 backdrop-blur-sm rounded-lg p-4">
                  <h4 className="font-semibold text-amber-800 mb-2">
                    🏞️ Soil Texture
                  </h4>
                  <p className="text-sm text-gray-700">
                    Determined by hydrometer method measuring particle size
                    distribution: Sand (2.0-0.05mm), Silt (0.05-0.002mm), Clay (
                    {"<"}0.002mm). Texture affects water holding capacity and
                    nutrient retention.
                  </p>
                </div>
                <div className="bg-white/70 backdrop-blur-sm rounded-lg p-4">
                  <h4 className="font-semibold text-amber-800 mb-2">
                    📊 Vegetation Health (NDVI)
                  </h4>
                  <p className="text-sm text-gray-700">
                    <strong>NDVI = (NIR - Red) / (NIR + Red)</strong>
                    <br />
                    Normalized Difference Vegetation Index measures plant health
                    and biomass. Values range from -1 to 1, with higher values
                    indicating healthier vegetation.
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
