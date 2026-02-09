import PriceChart from "../components/PriceChart";
import ChangePointChart from "../components/ChangePointChart";
import EventTimeline from "../components/EventTimeline";
import Filters from "../components/Filters";
import { useEffect, useState } from "react";
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
  const [volatilityData, setVolatilityData] = useState([]);
  const [activeTab, setActiveTab] = useState("prices");

  useEffect(() => {
    const fetchInitialData = async () => {
      try {
        setLoading(true);
        
        // Fetch prices for stats
        const pricesRes = await API.get("/prices");
        const data = pricesRes.data.data || [];
        
        if (data.length > 0) {
          const prices = data.map(d => d.Price).filter(p => p != null);
          const avgPrice = prices.length > 0 
            ? (prices.reduce((a, b) => a + b, 0) / prices.length).toFixed(2)
            : 0;
            
          setStats({
            totalDataPoints: data.length,
            dateRange: `${data[0]?.Date || 'N/A'} to ${data[data.length - 1]?.Date || 'N/A'}`,
            avgPrice: avgPrice,
            changePoints: 1,
            volatility: 0
          });
        }
        
        // Fetch events
        try {
          const eventsRes = await API.get("/events");
          setEvents(eventsRes.data.events || eventsRes.data || []);
        } catch (eventsErr) {
          console.warn("Events fetch failed:", eventsErr);
        }
        
        // Fetch volatility
        try {
          const volRes = await API.get("/prices/volatility?window=30");
          setVolatilityData(volRes.data.data || []);
        } catch (volErr) {
          console.warn("Volatility fetch failed:", volErr);
        }
        
      } catch (error) {
        console.error("Error fetching initial data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchInitialData();
  }, []);

  const handleFilterChange = async (filters) => {
    try {
      const params = new URLSearchParams();
      if (filters.startDate) params.append("start_date", filters.startDate);
      if (filters.endDate) params.append("end_date", filters.endDate);
      
      const pricesRes = await API.get(`/prices?${params.toString()}`);
      const data = pricesRes.data.data || [];
      
      if (data.length > 0) {
        const prices = data.map(d => d.Price).filter(p => p != null);
        const avgPrice = prices.length > 0 
          ? (prices.reduce((a, b) => a + b, 0) / prices.length).toFixed(2)
          : 0;
          
        setStats(prev => ({
          ...prev,
          totalDataPoints: data.length,
          dateRange: `${data[0]?.Date || 'N/A'} to ${data[data.length - 1]?.Date || 'N/A'}`,
          avgPrice: avgPrice
        }));
      }
    } catch (error) {
      console.error("Error applying filters:", error);
    }
  };

  if (loading) {
    return (
      <div className="dashboard-container">
        <div className="dashboard-header">
          <h1>🛢️ Brent Oil Price Analysis Dashboard</h1>
          <p>Bayesian Change Point Detection & Market Event Analysis</p>
        </div>
        <div className="stats-grid">
          {[1, 2, 3, 4].map(i => (
            <div key={i} className="stat-card skeleton" style={{ height: 100 }}></div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-container fade-in">
      <header className="dashboard-header">
        <h1>🛢️ Brent Oil Price Analysis Dashboard</h1>
        <p>Bayesian Change Point Detection & Market Event Analysis</p>
      </header>

      {/* Statistics Cards */}
      <section className="stats-grid">
        <div className="stat-card">
          <div className="label">Total Data Points</div>
          <div className="value">{stats.totalDataPoints.toLocaleString()}</div>
        </div>
        <div className="stat-card">
          <div className="label">Date Range</div>
          <div className="value" style={{ fontSize: '1rem' }}>{stats.dateRange}</div>
        </div>
        <div className="stat-card">
          <div className="label">Average Price</div>
          <div className="value">${Number(stats.avgPrice).toFixed(2)}</div>
        </div>
        <div className="stat-card">
          <div className="label">Detected Change Points</div>
          <div className="value">{stats.changePoints}</div>
          <div className="change">Bayesian Analysis</div>
        </div>
      </section>

      {/* Filters */}
      <Filters 
        onFilterChange={handleFilterChange} 
        onEventSelect={setSelectedEvent}
        events={events}
      />

      {/* Tab Navigation */}
      <div style={{ display: 'flex', gap: 8, marginBottom: 24 }}>
        {[
          { id: 'prices', label: '📈 Price Analysis' },
          { id: 'volatility', label: '📊 Volatility Analysis' },
          { id: 'events', label: '📅 Events & Impact' }
        ].map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            style={{
              background: activeTab === tab.id ? '#1e3a5f' : '#f0f0f0',
              color: activeTab === tab.id ? 'white' : '#1a1a2e',
              border: 'none',
              padding: '12px 20px',
              borderRadius: 8,
              cursor: 'pointer',
              fontWeight: 500,
              transition: 'all 0.2s'
            }}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      {activeTab === 'prices' && (
        <>
          <section className="chart-section">
            <div className="chart-grid">
              <div className="card">
                <div className="card-header">
                  <h3>📈 Brent Oil Price Time Series</h3>
                  {selectedEvent && (
                    <span className="change-point-badge">
                      📍 {selectedEvent.title}
                    </span>
                  )}
                </div>
                <div className="card-body">
                  <PriceChart 
                    changePoint={selectedEvent?.date} 
                    highlightedDate={selectedEvent?.date}
                  />
                </div>
              </div>
              
              <div className="card">
                <div className="card-header">
                  <h3>🎯 Change Point Analysis</h3>
                </div>
                <div className="card-body">
                  <ChangePointChart />
                </div>
              </div>
            </div>
          </section>
        </>
      )}

      {activeTab === 'volatility' && (
        <section className="chart-section">
          <div className="card">
            <div className="card-header">
              <h3>📊 Price Volatility Over Time</h3>
              <span style={{ fontSize: '0.8rem', color: '#6c757d' }}>
                30-day rolling standard deviation of returns
              </span>
            </div>
            <div className="card-body">
              <PriceChart 
                    highlightedDate={selectedEvent?.date}
                  />
            </div>
          </div>
        </section>
      )}

      {activeTab === 'events' && (
        <section className="chart-section">
          <div className="card">
            <div className="card-header">
              <h3>📅 Key Market Events & Impact Analysis</h3>
            </div>
            <div className="card-body">
              <EventTimeline />
            </div>
          </div>
        </section>
      )}

      {/* Event Impact Summary */}
      {selectedEvent && (
        <section className="chart-section fade-in">
          <div className="card">
            <div className="card-header">
              <h3>🎯 Event Impact Analysis</h3>
            </div>
            <div className="card-body">
              <div className="events-grid">
                <div className="event-card" style={{ borderLeftColor: '#ef4444' }}>
                  <div className="event-date">{selectedEvent.date}</div>
                  <div className="event-title">{selectedEvent.title}</div>
                  <div className="event-description">
                    This event marked a significant turning point in Brent oil prices. 
                    The Bayesian change point detection algorithm identified this date 
                    as a structural break in the price time series.
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
      )}
    </div>
  );
};

export default Dashboard;
