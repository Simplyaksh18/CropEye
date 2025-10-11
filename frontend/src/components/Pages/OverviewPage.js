import React from "react";
import { useLocation } from "../../context/LocationContext";
import { useAuth } from "../../context/AuthContext";
import { Compass, MapPin } from "lucide-react";
import PageSection from "./components/PageSection";

const OverviewPage = () => {
  const { analysisData, userLocation, referenceFarms } = useLocation();
  const { user } = useAuth();

  const selectedFarm = referenceFarms.find((farm) => {
    if (!userLocation) return false;
    return (
      Math.abs(farm.coordinates.lat - userLocation.lat) < 0.0001 &&
      Math.abs(farm.coordinates.lng - userLocation.lng) < 0.0001
    );
  });

  return (
    <div className="page-stack">
      <PageSection
        title={
          analysisData
            ? `${user?.firstName || "Farmer"}, here’s your growing outlook`
            : "Run an analysis to unlock your dashboard"
        }
        subtitle="We stitch together satellite vegetation, agro-meteorology, soil fertility and agronomic heuristics so you can take timely field decisions."
        mediaUrl="https://images.unsplash.com/photo-1589924744724-924337c0b284?auto=format&fit=crop&w=1200&q=60"
        badge="Executive Summary"
      >
        {analysisData ? (
          <div className="stats-grid">
            <article>
              <h4>Vegetation health</h4>
              <p className="metric">
                {analysisData.ndvi_report?.status ||
                  analysisData.health_analysis?.status ||
                  "Pending"}
              </p>
              <p className="muted">
                Latest NDVI{" "}
                {analysisData.ndvi_report?.latestValue !== undefined &&
                analysisData.ndvi_report?.latestValue !== null
                  ? Number(analysisData.ndvi_report.latestValue).toFixed(2)
                  : analysisData.ndvi?.mean !== undefined &&
                    analysisData.ndvi?.mean !== null
                  ? Number(analysisData.ndvi.mean).toFixed(2)
                  : "--"}{" "}
                (trend{" "}
                <strong>
                  {analysisData.ndvi_report?.trend ??
                    analysisData.trend_analysis?.summary ??
                    analysisData.trend_analysis?.trend}
                </strong>
                )
              </p>
            </article>
            <article>
              <h4>Field cover</h4>
              <p className="metric">
                {analysisData.vegetation_percentage ??
                  analysisData.vegetation_coverage ??
                  analysisData.ndvi_analysis?.vegetation_percentage ??
                  "--"}
                %
              </p>
              <p className="muted">Green biomass relative to ideal canopies.</p>
            </article>
            <article>
              <h4>Weather outlook</h4>
              <p className="metric">
                {analysisData.weather_forecast?.summary || "Awaiting forecast"}
              </p>
              <p className="muted">
                Powered by AgroMonitoring forecast polygons.
              </p>
            </article>
            <article>
              <h4>Soil vitality</h4>
              <p className="metric">
                Fertility score{" "}
                {analysisData.soil_fertility?.fertility_score ?? "--"}
              </p>
              <p className="muted">
                Estimated from region-specific reference models.
              </p>
            </article>
          </div>
        ) : (
          <div className="empty-state">
            <p>
              Start with GPS or choose a reference farm to populate insights.
            </p>
          </div>
        )}
      </PageSection>

      {analysisData && (
        <PageSection
          title="Where are we analyzing?"
          subtitle="We provide lat/long transparency so agronomists can validate the exact polygon analysed."
          icon={<Compass size={22} />}
          mediaUrl="https://images.unsplash.com/photo-1527152831-4c03e05a6caa?auto=format&fit=crop&w=1000&q=60"
        >
          <div className="location-summary">
            <div>
              <p>
                <strong>Coordinates:</strong> {userLocation?.lat.toFixed(4)},{" "}
                {userLocation?.lng.toFixed(4)}
              </p>
              {analysisData.analysis_timestamp && (
                <p>
                  <strong>Generated at:</strong>{" "}
                  {new Date(analysisData.analysis_timestamp).toLocaleString()}
                </p>
              )}
              {selectedFarm ? (
                <p>
                  <strong>Reference farm:</strong> {selectedFarm.name} (
                  {selectedFarm.country})
                </p>
              ) : (
                <p>
                  <strong>Reference farm:</strong> Custom field
                </p>
              )}
            </div>
            <div className="map-preview">
              <MapPin size={42} />
              <span>Polygon drawn via AgroMonitoring API</span>
            </div>
          </div>
        </PageSection>
      )}
    </div>
  );
};

export default OverviewPage;
