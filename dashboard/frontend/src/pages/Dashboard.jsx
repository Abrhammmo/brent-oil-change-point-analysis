import { useEffect, useMemo, useState } from "react";
import ChangePointChart from "../components/ChangePointChart";
import EventTimeline from "../components/EventTimeline";
import Filters from "../components/Filters";
import PriceChart from "../components/PriceChart";
import API from "../services/api";

const Dashboard = () => {
  const [stats, setStats] = useState({
    totalDataPoints: 0,
    dateRange: "",
    avgPrice: 0,
    changePoints: 0,
    volatility: 0
  });
  const [loading, setLoading] = useState(true);
  const [events, setEvents] = useState([]);
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [clickedDate, setClickedDate] = useState(null);
  const [activeTab, setActiveTab] = useState("prices");
  const [macroToggles, setMacroToggles] = useState({
    GDP: true,
    Inflation: false,
    ExchangeRate: false,
    Causes: false
  });
  const [shapData, setShapData] = useState({ global_plot_b64: null, local_plot_b64: null });

  useEffect(() => {
    const fetchInitialData = async () => {
      try {
        setLoading(true);
        const [pricesRes, eventsRes, cpRes, volRes] = await Promise.all([
          API.get("/prices"),
          API.get("/events"),
          API.get("/change-points"),
          API.get("/prices/volatility?window=30")
        ]);
        const data = pricesRes.data.data || [];
        const prices = data.map((d) => d.Price).filter((p) => p != null);
        const avgPrice = prices.length ? prices.reduce((a, b) => a + b, 0) / prices.length : 0;
        const volatilityRows = volRes.data.data || [];
        const avgVol = volatilityRows.length
          ? volatilityRows.reduce((acc, row) => acc + Number(row.Volatility || 0), 0) / volatilityRows.length
          : 0;
        setStats({
          totalDataPoints: data.length,
          dateRange: `${data[0]?.Date || "N/A"} to ${data[data.length - 1]?.Date || "N/A"}`,
          avgPrice: avgPrice,
          changePoints: (cpRes.data?.change_points || []).length,
          volatility: avgVol
        });
        setEvents(eventsRes.data.events || []);
      } finally {
        setLoading(false);
      }
    };
    fetchInitialData();
  }, []);

  useEffect(() => {
    const selectedDate = selectedEvent?.date || clickedDate;
    const fetchShap = async () => {
      const query = selectedDate ? `?selected_date=${encodeURIComponent(selectedDate)}` : "";
      const shapRes = await API.get(`/change-points/shap${query}`);
      setShapData(shapRes.data || {});
    };
    fetchShap().catch(() => {
      setShapData({ global_plot_b64: null, local_plot_b64: null });
    });
  }, [selectedEvent, clickedDate]);

  const handleFilterChange = async (filters) => {
    const params = new URLSearchParams();
    if (filters.startDate) params.append("start_date", filters.startDate);
    if (filters.endDate) params.append("end_date", filters.endDate);
    const pricesRes = await API.get(`/prices?${params.toString()}`);
    const data = pricesRes.data.data || [];
    const prices = data.map((d) => d.Price).filter((p) => p != null);
    setStats((prev) => ({
      ...prev,
      totalDataPoints: data.length,
      dateRange: `${data[0]?.Date || "N/A"} to ${data[data.length - 1]?.Date || "N/A"}`,
      avgPrice: prices.length ? prices.reduce((a, b) => a + b, 0) / prices.length : 0
    }));
  };

  const macroToggleButtons = useMemo(
    () => ["GDP", "Inflation", "ExchangeRate", "Causes"],
    []
  );

  const closestClickedEvent = useMemo(() => {
    if (!macroToggles.Causes || !clickedDate || !events.length) return null;
    const clickedTs = new Date(clickedDate).getTime();
    if (Number.isNaN(clickedTs)) return null;

    let best = null;
    let bestDiff = Number.POSITIVE_INFINITY;
    for (const event of events) {
      const eventTs = new Date(event.date).getTime();
      if (Number.isNaN(eventTs)) continue;
      const diff = Math.abs(eventTs - clickedTs);
      if (diff < bestDiff) {
        best = event;
        bestDiff = diff;
      }
    }
    return best;
  }, [events, clickedDate, macroToggles.Causes]);

  if (loading) return <div className="dashboard-container"><div className="skeleton" style={{ height: 260 }} /></div>;

  return (
    <div className="dashboard-container fade-in">
      <header className="dashboard-header">
        <h1>Brent Oil Regime Intelligence Dashboard</h1>
        <p>Multi-change-point Bayesian analysis, macro overlays, and explainability.</p>
      </header>

      <section className="stats-grid">
        <div className="stat-card"><div className="label">Data Points</div><div className="value">{stats.totalDataPoints}</div></div>
        <div className="stat-card"><div className="label">Date Range</div><div className="value" style={{ fontSize: "0.95rem" }}>{stats.dateRange}</div></div>
        <div className="stat-card"><div className="label">Average Price</div><div className="value">${Number(stats.avgPrice).toFixed(2)}</div></div>
        <div className="stat-card"><div className="label">Change Points</div><div className="value">{stats.changePoints}</div></div>
        <div className="stat-card"><div className="label">Avg Volatility</div><div className="value">{Number(stats.volatility).toFixed(4)}</div></div>
      </section>

      <Filters onFilterChange={handleFilterChange} onEventSelect={setSelectedEvent} events={events} />

      <div className="tab-nav">
        {["prices", "regimes", "events", "shap"].map((tab) => (
          <button key={tab} className={`tab-btn ${activeTab === tab ? "active" : ""}`} onClick={() => setActiveTab(tab)}>
            {tab.toUpperCase()}
          </button>
        ))}
      </div>

      <div style={{ display: "flex", gap: 8, marginBottom: 16, flexWrap: "wrap" }}>
        {macroToggleButtons.map((feature) => (
          <button
            key={feature}
            className={`tab-btn ${macroToggles[feature] ? "active" : ""}`}
            onClick={() => setMacroToggles((prev) => ({ ...prev, [feature]: !prev[feature] }))}
          >
            {feature}
          </button>
        ))}
      </div>

      {macroToggles.Causes && closestClickedEvent && (
        <div className="card" style={{ marginBottom: 16 }}>
          <div className="card-header"><h3>Closest Cause To Clicked Date</h3></div>
          <div className="card-body">
            <p style={{ marginBottom: 6 }}>
              <strong>{closestClickedEvent.date}</strong> - {closestClickedEvent.title}
            </p>
            {closestClickedEvent.description && (
              <p style={{ color: "#6c757d" }}>{closestClickedEvent.description}</p>
            )}
          </div>
        </div>
      )}

      {selectedEvent && (
        <div className="card" style={{ marginBottom: 16 }}>
          <div className="card-header"><h3>Selected Event Description</h3></div>
          <div className="card-body">
            <p style={{ marginBottom: 6 }}>
              <strong>{selectedEvent.date}</strong> - {selectedEvent.title}
            </p>
            <p style={{ color: "#6c757d" }}>
              {selectedEvent.description || "No description available for this event."}
            </p>
          </div>
        </div>
      )}

      {activeTab === "prices" && (
        <div className="card">
          <div className="card-header"><h3>Price + Macro Overlay</h3></div>
          <div className="card-body">
            <PriceChart
              highlightedDate={selectedEvent?.date}
              macroToggles={macroToggles}
              closestEventDate={closestClickedEvent?.date}
              onDateClick={setClickedDate}
            />
          </div>
        </div>
      )}

      {activeTab === "regimes" && (
        <div className="card">
          <div className="card-header"><h3>Regime Visualization</h3></div>
          <div className="card-body"><ChangePointChart macroToggles={macroToggles} events={events} /></div>
        </div>
      )}

      {activeTab === "events" && (
        <div className="card">
          <div className="card-header"><h3>Business Event Timeline</h3></div>
          <div className="card-body"><EventTimeline /></div>
        </div>
      )}

      {activeTab === "shap" && (
        <div className="chart-grid-equal">
          <div className="card">
            <div className="card-header"><h3>SHAP Summary</h3></div>
            <div className="card-body">
              {shapData.global_plot_b64 ? (
                <img alt="SHAP global" style={{ width: "100%" }} src={`data:image/png;base64,${shapData.global_plot_b64}`} />
              ) : <p>No global SHAP artifact found.</p>}
            </div>
          </div>
          <div className="card">
            <div className="card-header"><h3>Why this prediction?</h3></div>
            <div className="card-body">
              {shapData.local_plot_b64 ? (
                <img alt="SHAP local" style={{ width: "100%" }} src={`data:image/png;base64,${shapData.local_plot_b64}`} />
              ) : <p>No local SHAP artifact found.</p>}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
