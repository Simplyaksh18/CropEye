import React, { useMemo } from "react";
import { Sparkles, ClipboardCheck } from "lucide-react";
import PageSection from "./components/PageSection";
import { useLocation } from "../../context/LocationContext";

const InsightsPage = () => {
  const { analysisData } = useLocation();

  const insights = useMemo(() => {
    if (!analysisData) {
      return [];
    }

    const notes = [];
    const ndvi = analysisData.ndvi_report;
    const weather = analysisData.weather_forecast;

    if (ndvi?.trend === "declining") {
      notes.push(
        "Vegetation trend is declining. Schedule field scouting to inspect for nutrient deficiency or pest onset within 48 hours."
      );
    } else if (ndvi?.trend === "improving") {
      notes.push(
        "NDVI is trending upward – maintain current irrigation regimen to sustain vigor."
      );
    }

    const highRain = weather?.days?.find((day) => day.precipitation > 15);
    if (highRain) {
      notes.push(
        `Heavy precipitation (~${
          highRain.precipitation
        } mm) forecast for ${new Date(
          highRain.date
        ).toLocaleDateString()}. Plan drainage checks and reschedule spray windows.`
      );
    }

    const lowHumidity = weather?.days?.every((day) => (day.humidity ?? 0) < 45);
    if (lowHumidity) {
      notes.push(
        "Low humidity week detected – prioritize irrigation scheduling and mulch retention."
      );
    }

    if (analysisData.crop_recommendations?.length) {
      notes.push(
        `Top agronomic fit: ${analysisData.crop_recommendations[0].crop}. Adoption success ${analysisData.crop_recommendations[0].expectedHarvestSuccessRate}.`
      );
    }

    return notes;
  }, [analysisData]);

  return (
    <div className="page-stack">
      <PageSection
        title="Actionable playbook"
        subtitle="We condense telemetry streams into next best actions for the field team."
        badge="Insights"
        icon={<Sparkles size={22} />}
        mediaUrl="https://images.unsplash.com/photo-1601004890684-d8cbf643f5f2?auto=format&fit=crop&w=1200&q=60"
      >
        {insights.length ? (
          <ol className="insights-list">
            {insights.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ol>
        ) : (
          <div className="empty-state">
            Generate an analysis to view insights.
          </div>
        )}
      </PageSection>

      {analysisData && (
        <PageSection
          title="Next visits checklist"
          icon={<ClipboardCheck size={22} />}
          subtitle="Use this list with your field teams or agronomists during weekly rounds."
          mediaUrl="https://images.unsplash.com/photo-1499529112087-3cb3b73cec0c?auto=format&fit=crop&w=1000&q=60"
        >
          <ul className="bullet-list">
            <li>
              Capture geo-tagged photos to validate satellite NDVI readings.
            </li>
            <li>
              Deploy pheromone traps if pest severity is medium or higher.
            </li>
            <li>
              Update irrigation scheduler with forecast rainfall to avoid
              waterlogging.
            </li>
            <li>
              Collect soil samples post-harvest to recalibrate fertility
              simulation.
            </li>
          </ul>
        </PageSection>
      )}
    </div>
  );
};

export default InsightsPage;
