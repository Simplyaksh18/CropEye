import React, { useMemo } from "react";
import { CloudLightning, CloudRainWind } from "lucide-react";
import PageSection from "./components/PageSection";
import { useLocation } from "../../context/LocationContext";

const formatMeasure = (value, digits = 1, suffix = "") =>
  typeof value === "number" ? `${value.toFixed(digits)}${suffix}` : "--";

const WeatherPage = () => {
  const { analysisData } = useLocation();
  const weather = analysisData?.weather_forecast;
  const headlineDay = weather?.days?.[0];
  const secondaryDay = weather?.days?.[1];

  const snapshotCards = useMemo(() => {
    if (!weather?.days?.length) {
      return [];
    }

    return [
      {
        key: "field-window",
        meta: "Operations tip",
        title: "Field workability",
        copy: headlineDay
          ? `Start operations before ${formatMeasure(
              headlineDay.temperature?.max,
              1,
              "°C"
            )} highs; humidity near ${formatMeasure(
              headlineDay.humidity,
              0,
              "%"
            )} keeps foliar sprays effective.`
          : "Analyze a field to unlock operations timing guidance.",
        footer: headlineDay
          ? `Outlook: ${headlineDay.outlook || "stable skies"}.`
          : null,
        image:
          "https://images.unsplash.com/photo-1514996937319-344454492b37?auto=format&fit=crop&w=600&q=60",
      },
      {
        key: "rain-signal",
        meta: "Moisture watch",
        title: "Rain gauge signal",
        copy: headlineDay
          ? `Rain next 24 h sits at ${formatMeasure(
              headlineDay.precipitation,
              1,
              " mm"
            )}. ${
              headlineDay.precipitation > 3
                ? "Delay irrigation passes and fortify drainage."
                : "Window open for top-up irrigation towards dusk."
            }`
          : "Moisture insights appear after we process a field polygon.",
        footer: secondaryDay
          ? `Day 2 outlook: ${secondaryDay.outlook} · ${formatMeasure(
              secondaryDay.precipitation,
              1,
              " mm"
            )}`
          : null,
        image:
          "https://images.unsplash.com/photo-1501004318641-b39e6451bec6?auto=format&fit=crop&w=600&q=60",
      },
      {
        key: "wind-line",
        meta: "Wind corridor",
        title: "Spray drift guard",
        copy: headlineDay
          ? `Average wind ${formatMeasure(
              headlineDay.wind?.avg_speed,
              1,
              " m/s"
            )} with gusts up to ${formatMeasure(
              headlineDay.wind?.gust_max,
              1,
              " m/s"
            )}. Slot spraying when gusts stay under 9 m/s.`
          : "Wind advisories will unlock once weather analytics are ready.",
        footer:
          weather.summary || "Stable conditions expected across the block.",
        image:
          "https://images.unsplash.com/photo-1469474968028-56623f02e42e?auto=format&fit=crop&w=600&q=60",
      },
    ];
  }, [weather, headlineDay, secondaryDay]);

  return (
    <div className="page-stack">
      <PageSection
        title="Agro-meteorological window"
        subtitle="Seven-day polygon-specific forecast generated via AgroMonitoring forecast endpoint. Values shown in °C with precipitation totals in mm."
        badge="Weather"
        icon={<CloudLightning size={24} />}
        mediaUrl="https://images.unsplash.com/photo-1504274066651-8d31a536b11a?auto=format&fit=crop&w=1200&q=60"
      >
        {weather?.days?.length ? (
          <div className="forecast-grid">
            {weather.days.map((day) => (
              <article key={day.date} className="forecast-card">
                <span className="forecast-date">
                  {new Date(day.date).toLocaleDateString(undefined, {
                    weekday: "short",
                    day: "numeric",
                    month: "short",
                  })}
                </span>
                <div className="forecast-temp">
                  <span>{formatMeasure(day.temperature?.max, 1, "°C")}</span>
                  <small>max</small>
                </div>
                <div className="forecast-temp">
                  <span>{formatMeasure(day.temperature?.min, 1, "°C")}</span>
                  <small>min</small>
                </div>
                <p className="forecast-outlook">{day.outlook}</p>
                <p className="forecast-rain">
                  Rain: {formatMeasure(day.precipitation, 1, " mm")}
                </p>
                <p className="forecast-humidity">
                  Humidity: {formatMeasure(day.humidity, 0, "%")}
                </p>
                <p className="forecast-wind">
                  Wind {formatMeasure(day.wind?.avg_speed, 1, " m/s")} (gust{" "}
                  {formatMeasure(day.wind?.gust_max, 1, " m/s")})
                </p>
              </article>
            ))}
          </div>
        ) : (
          <div className="empty-state">
            No forecast yet. Analyze a location first.
          </div>
        )}

        {snapshotCards.length > 0 && (
          <div className="fact-grid">
            {snapshotCards.map((card) => (
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

      {weather?.summary && (
        <PageSection
          title="Field impact assessment"
          subtitle={weather.summary}
          icon={<CloudRainWind size={24} />}
          mediaUrl="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1200&q=60"
        >
          <ul className="bullet-list">
            <li>
              Monitor soil moisture if rainfall stays below 1 mm – pivot to
              deficit irrigation scheduling.
            </li>
            <li>
              Gust values above 12 m/s warrant lodging protection in cereals –
              plan growth regulators.
            </li>
            <li>
              Relative humidity over 80% for 2+ days may trigger foliar
              diseases; prepare prophylactic spray.
            </li>
          </ul>
        </PageSection>
      )}
    </div>
  );
};

export default WeatherPage;
