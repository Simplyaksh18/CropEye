import React, { useMemo } from "react";
import { LineChart, TrendingUp } from "lucide-react";
import PageSection from "./components/PageSection";
import { useLocation } from "../../context/LocationContext";

const NdviPage = () => {
  const { analysisData } = useLocation();
  // Prefer legacy-shaped ndvi_report, fall back to backend ndvi payload
  const ndvi =
    analysisData?.ndvi_report ||
    (analysisData?.ndvi
      ? {
          latestValue: analysisData.ndvi.mean,
          latestDate: analysisData.analysis_date,
          status: analysisData.health_analysis?.status,
          trend:
            analysisData.trend_analysis?.summary ||
            analysisData.trend_analysis?.trend,
          change:
            analysisData.ndvi.mean && analysisData.ndvi.median
              ? Number(
                  (analysisData.ndvi.mean - analysisData.ndvi.median).toFixed(3)
                )
              : null,
          seasonalAverage: analysisData.ndvi.mean,
          history: Array.isArray(analysisData.ndvi_history)
            ? analysisData.ndvi_history
            : [],
        }
      : null);
  const vegetationCover =
    typeof analysisData?.vegetation_coverage === "number"
      ? analysisData.vegetation_coverage
      : typeof analysisData?.vegetation_percentage === "number"
      ? analysisData.vegetation_percentage
      : null;

  const ndviSpotlights = useMemo(() => {
    if (!ndvi) {
      return [];
    }

    const history = Array.isArray(ndvi.history) ? ndvi.history : [];
    const lastEntry = history.length ? history[history.length - 1] : null;
    const weekAgoIndex = history.length - 4 >= 0 ? history.length - 4 : 0;
    const weekAgoEntry = history.length ? history[weekAgoIndex] : null;
    const weekDelta =
      lastEntry && weekAgoEntry
        ? (lastEntry.value - weekAgoEntry.value).toFixed(3)
        : null;

    return [
      {
        key: "latest-pass",
        meta: lastEntry
          ? new Date(lastEntry.date).toLocaleDateString(undefined, {
              month: "short",
              day: "numeric",
            })
          : "Latest pass",
        title: "Latest Sentinel capture",
        copy: lastEntry
          ? `NDVI ${lastEntry.value.toFixed(3)} signals ${
              ndvi.status?.toLowerCase() || "stable canopy"
            }.`
          : "Analyze a field to pull the newest satellite composite.",
        footer: ndvi.trend
          ? `Trend: ${ndvi.trend}${
              ndvi.change
                ? ` (${ndvi.change > 0 ? "+" : ""}${ndvi.change})`
                : ""
            }`
          : null,
        image:
          "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=600&q=60",
      },
      {
        key: "canopy-cover",
        meta: "Canopy cover",
        title:
          vegetationCover !== null
            ? `${vegetationCover.toFixed(1)}% cover`
            : "Canopy density",
        copy:
          vegetationCover !== null
            ? "Green biomass holds steady against the district benchmark."
            : "We estimate cover once the first analysis completes.",
        footer: weekDelta ? `1-week delta ${weekDelta}` : null,
        image:
          "https://images.unsplash.com/photo-1533488765986-dfa2a9939acd?auto=format&fit=crop&w=600&q=60",
      },
      {
        key: "seasonal-band",
        meta: "Seasonal track",
        title: ndvi.seasonalAverage
          ? `Seasonal avg ${ndvi.seasonalAverage}`
          : "Seasonal average",
        copy: "Rolling six-pass average to benchmark vigor against historical performance.",
        footer: ndvi.status ? `Status: ${ndvi.status}` : null,
        image:
          "https://images.unsplash.com/photo-1477414348463-c0eb7f1359b6?auto=format&fit=crop&w=600&q=60",
      },
    ];
  }, [ndvi, vegetationCover]);

  return (
    <div className="page-stack">
      <PageSection
        title="Vegetation vigor (NDVI)"
        subtitle="Normalized Difference Vegetation Index derived from AgroMonitoring polygon imagery. We summarise temporal behavior and classify canopy health."
        badge="Satellite"
        icon={<LineChart size={22} />}
        mediaUrl="https://images.unsplash.com/photo-1471194402529-8e0f5ed81b86?auto=format&fit=crop&w=1200&q=60"
      >
        {ndvi ? (
          <div className="ndvi-metrics">
            <div className="ndvi-highlight">
              <p className="metric">{ndvi.latestValue?.toFixed(3) ?? "--"}</p>
              <p className="muted">
                Latest composite (
                {ndvi.latestDate
                  ? new Date(ndvi.latestDate).toLocaleDateString()
                  : "--"}
                )
              </p>
            </div>
            <div className="ndvi-highlight">
              <p className="metric">{ndvi.status}</p>
              <p className="muted">Classification driven by canopy greenness</p>
            </div>
            <div className="ndvi-highlight">
              <p className="metric">{ndvi.trend}</p>
              <p className="muted">
                Trend change {ndvi.change > 0 ? "+" : ""}
                {ndvi.change}
              </p>
            </div>
            <div className="ndvi-highlight">
              <p className="metric">{ndvi.seasonalAverage}</p>
              <p className="muted">Seasonal rolling average</p>
            </div>
          </div>
        ) : (
          <div className="empty-state">
            Analyze a location to compute NDVI timeline.
          </div>
        )}

        {ndviSpotlights.length > 0 && (
          <div className="fact-grid">
            {ndviSpotlights.map((card) => (
              <article key={card.key} className="fact-card">
                <img src={card.image} alt={card.title} loading="lazy" />
                <div className="fact-card__body">
                  <span className="fact-card__meta">{card.meta}</span>
                  <h4>{card.title}</h4>
                  <p className="fact-card__text">{card.copy}</p>
                  {card.footer && (
                    <span className="fact-card__footer">{card.footer}</span>
                  )}
                </div>
              </article>
            ))}
          </div>
        )}
      </PageSection>

      {ndvi?.history?.length > 0 && (
        <PageSection
          title="NDVI trail"
          subtitle="Latest 30 acquisitions ordered chronologically."
          icon={<TrendingUp size={22} />}
          mediaUrl="https://images.unsplash.com/photo-1489515217757-5fd1be406fef?auto=format&fit=crop&w=600&q=60"
        >
          <div className="ndvi-timeline">
            {ndvi.history.map((point) => (
              <div key={point.date} className="ndvi-point">
                <div>
                  <strong>{new Date(point.date).toLocaleDateString()}</strong>
                  <span>
                    {new Date(point.date).toLocaleTimeString([], {
                      hour: "2-digit",
                      minute: "2-digit",
                    })}
                  </span>
                </div>
                <div className="ndvi-point__values">
                  <span className="ndvi-value">{point.value}</span>
                  {point.max && (
                    <span className="ndvi-minmax">max {point.max}</span>
                  )}
                  {point.min && (
                    <span className="ndvi-minmax">min {point.min}</span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </PageSection>
      )}
    </div>
  );
};

export default NdviPage;
