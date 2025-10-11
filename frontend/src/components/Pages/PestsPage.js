import React from "react";
import { ShieldAlert, Bug } from "lucide-react";
import PageSection from "./components/PageSection";
import { useLocation } from "../../context/LocationContext";

const PestsPage = () => {
  const { analysisData } = useLocation();
  const pests = analysisData?.pest_alerts || [];

  return (
    <div className="page-stack">
      <PageSection
        title="Integrated pest management watch"
        subtitle="Stay ahead of regional pest pressures. Alerts can be synced with your scouting calendar."
        badge="Protection"
        icon={<ShieldAlert size={22} />}
        mediaUrl="https://images.unsplash.com/photo-1472145246862-b24cf25c4a36?auto=format&fit=crop&w=1000&q=60"
      >
        {pests.length ? (
          <div className="pest-grid">
            {pests.map((alert) => (
              <article
                key={alert.pest}
                className={`pest-card severity-${alert.severity.toLowerCase()}`}
              >
                <header>
                  <Bug size={18} />
                  <h3>{alert.pest}</h3>
                  <span className="severity-chip">{alert.severity}</span>
                </header>
                <p>{alert.description}</p>
                <p className="muted">Recommendation: {alert.recommendation}</p>
                <small>
                  Last updated {new Date(alert.last_updated).toLocaleString()}
                </small>
              </article>
            ))}
          </div>
        ) : (
          <div className="empty-state">No pest alerts yet. Run analysis.</div>
        )}
      </PageSection>
    </div>
  );
};

export default PestsPage;
