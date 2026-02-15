import { useEffect, useState } from "react";
import API from "../services/api";
import PriceChart from "./PriceChart";

const ChangePointChart = ({ macroToggles, events = [] }) => {
  const [results, setResults] = useState(null);
  const [posterior, setPosterior] = useState({});
  const [impact, setImpact] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [cpRes, postRes, impactRes] = await Promise.all([
          API.get("/change-points"),
          API.get("/change-points/posterior"),
          API.get("/change-points/business-impact")
        ]);
        setResults(cpRes.data || {});
        setPosterior(postRes.data || {});
        setImpact(impactRes.data?.business_impact || []);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) return <div className="skeleton" style={{ height: 350 }} />;
  const changePoints = results?.change_points || [];

  const nearestEventForDate = (dateStr) => {
    const cpTs = new Date(dateStr).getTime();
    if (!events.length || Number.isNaN(cpTs)) return null;
    let best = null;
    let bestDiff = Number.POSITIVE_INFINITY;
    for (const event of events) {
      const evTs = new Date(event.date).getTime();
      if (Number.isNaN(evTs)) continue;
      const diff = Math.abs(evTs - cpTs);
      if (diff < bestDiff) {
        best = event;
        bestDiff = diff;
      }
    }
    return best;
  };

  return (
    <div>
      <PriceChart changePoints={changePoints} macroToggles={macroToggles} />
      <div className="events-grid" style={{ marginTop: 16 }}>
        <div className="stat-card">
          <div className="label">Detected Regimes</div>
          <div className="value">{(results?.regimes || []).length}</div>
        </div>
        <div className="stat-card">
          <div className="label">Change Points</div>
          <div className="value">{changePoints.length}</div>
        </div>
      </div>

      <div className="card" style={{ marginTop: 16 }}>
        <div className="card-header">
          <h3>Detected Change Point Years</h3>
        </div>
        <div className="card-body">
          {changePoints.length === 0 && <p>No change points available.</p>}
          {changePoints.map((cp, idx) => {
            const nearestEvent = nearestEventForDate(cp.tau_date);
            return (
              <div key={`${cp.tau_date}-${idx}`} className="event-card" style={{ marginBottom: 8 }}>
                <div className="event-title">
                  {idx === 0 ? "First" : idx === 1 ? "Second" : `${idx + 1}th`} change point: {cp.tau_date}
                </div>
                {nearestEvent && (
                  <div className="event-description">
                    Related event: {nearestEvent.date} - {nearestEvent.title}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      <div className="card" style={{ marginTop: 16 }}>
        <div className="card-header">
          <h3>Posterior Distributions</h3>
        </div>
        <div className="card-body">
          {Object.keys(posterior).length === 0 && <p>No posterior samples available.</p>}
          {Object.entries(posterior).map(([key, value]) => (
            <div key={key} style={{ marginBottom: 10 }}>
              <strong>{key}</strong>: mean={Number(value.posterior_mean || 0).toFixed(2)} hdi=(
              {Number(value.hdi_lower || 0).toFixed(2)}, {Number(value.hdi_upper || 0).toFixed(2)})
            </div>
          ))}
        </div>
      </div>

      <div className="card" style={{ marginTop: 16 }}>
        <div className="card-header">
          <h3>Business Impact Panel</h3>
        </div>
        <div className="card-body">
          {(impact || []).length === 0 && <p>No business impact metrics available.</p>}
          {(impact || []).map((item, idx) => (
            <div key={idx} className="event-card" style={{ marginBottom: 8 }}>
              <div className="event-title">{item.transition}</div>
              <div className="event-description">
                % change: {item.mean_shift_percent?.toFixed?.(2) ?? "N/A"} | Volatility shift:{" "}
                {item.volatility_shift?.toFixed?.(4) ?? "N/A"} | Durations: {item.duration_before} /{" "}
                {item.duration_after}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ChangePointChart;
