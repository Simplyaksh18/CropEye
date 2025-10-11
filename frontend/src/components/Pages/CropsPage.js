import React from "react";
import { Sprout, Wheat } from "lucide-react";
import { useLocation } from "../../context/LocationContext";
import PageSection from "./components/PageSection";

const CropsPage = () => {
  const { analysisData } = useLocation();
  const recommendations = analysisData?.crop_recommendations || [];
  const soil = analysisData?.soil_fertility;

  return (
    <div className="page-stack">
      <PageSection
        title="Crop positioning"
        subtitle="Recommendations leverage NDVI vigor, soil fertility simulation and short-term weather forecast."
        badge="Advisory"
        icon={<Sprout size={22} />}
        mediaUrl="https://images.unsplash.com/photo-1582719478100-3460f3d3a3b3?auto=format&fit=crop&w=1200&q=60"
      >
        {soil ? (
          <div className="soil-grid">
            <div>
              <h4>Soil chemistry snapshot</h4>
              <ul className="soil-list">
                <li>pH: {soil.ph_level}</li>
                <li>Nitrogen: {soil.nitrogen} kg/ha</li>
                <li>Phosphorus: {soil.phosphorus} kg/ha</li>
                <li>Potassium: {soil.potassium} kg/ha</li>
                <li>Organic matter: {soil.organic_matter}%</li>
                <li>Fertility score: {soil.fertility_score}</li>
              </ul>
            </div>
            <div>
              <p className="muted">
                Values are estimated baselines; validate via soil testing to
                fine-tune fertilizer plans. We match these metrics to
                region-specific agronomy trials.
              </p>
            </div>
          </div>
        ) : (
          <div className="empty-state">
            Run an analysis to compute soil model.
          </div>
        )}
      </PageSection>

      {recommendations.length > 0 && (
        <PageSection
          title="Why we recommend these crops"
          icon={<Wheat size={22} />}
          subtitle="Each option captures rationale, success probability and actionable practices."
          mediaUrl="https://images.unsplash.com/photo-1495107334309-fcf20504a5ab?auto=format&fit=crop&w=1000&q=60"
        >
          <div className="crop-cards">
            {recommendations.map((rec) => (
              <article key={rec.crop} className="crop-card">
                <header>
                  <h3>{rec.crop}</h3>
                  <span
                    className={`chip chip-${rec.suitability
                      .toLowerCase()
                      .replace(/[^a-z]/g, "")}`}
                  >
                    {rec.suitability} suitability
                  </span>
                </header>
                <p className="reason">{rec.reason}</p>
                <p className="success">
                  Expected harvest success: {rec.expectedHarvestSuccessRate}
                </p>
                <ul>
                  {rec.recommendedPractices.map((line) => (
                    <li key={line}>{line}</li>
                  ))}
                </ul>
              </article>
            ))}
          </div>
        </PageSection>
      )}
    </div>
  );
};

export default CropsPage;
