import PriceChart from "./PriceChart";
import { useEffect, useState } from "react";
import API from "../services/api";

const ChangePointChart = () => {
  const [changePoint, setChangePoint] = useState(null);
  const [changePointInfo, setChangePointInfo] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchChangePoint = async () => {
      try {
        setLoading(true);
        const response = await API.get("/change-points");
        const data = response.data;
        
        // Handle both object and array responses
        const tauDate = data?.tau_date || (data[0]?.tau_date) || null;
        const muBefore = data?.mu_before || (data[0]?.mu_before) || null;
        const muAfter = data?.mu_after || (data[0]?.mu_after) || null;
        
        setChangePoint(tauDate);
        setChangePointInfo({
          tauDate,
          muBefore,
          muAfter
        });
        setError(null);
      } catch (err) {
        console.error("Error fetching change point:", err);
        setError("Failed to load change point data");
      } finally {
        setLoading(false);
      }
    };

    fetchChangePoint();
  }, []);

  if (loading) {
    return (
      <div>
        <div className="skeleton" style={{ height: 350, marginBottom: 16 }}></div>
        <div className="events-grid">
          {[1, 2].map(i => (
            <div key={i} className="stat-card skeleton" style={{ height: 80 }}></div>
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div>
        <div className="error-state" style={{ height: 350 }}>
          <div className="error-icon">⚠️</div>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  const priceChange = changePointInfo?.muBefore && changePointInfo?.muAfter
    ? ((changePointInfo.muAfter - changePointInfo.muBefore) / changePointInfo.muBefore * 100).toFixed(1)
    : null;

  return (
    <div>
      <PriceChart changePoint={changePoint} />
      
      {changePoint && (
        <div style={{ marginTop: 16 }}>
          <div className="change-point-badge" style={{ marginBottom: 16 }}>
            <span>🎯</span>
            <span>Bayesian Change Point Detected: {changePoint}</span>
          </div>
          
          <div className="events-grid">
            <div className="stat-card">
              <div className="label">Mean Price Before</div>
              <div className="value">${changePointInfo?.muBefore?.toFixed(2) || 'N/A'}</div>
            </div>
            <div className="stat-card">
              <div className="label">Mean Price After</div>
              <div className="value">${changePointInfo?.muAfter?.toFixed(2) || 'N/A'}</div>
            </div>
            <div className="stat-card">
              <div className="label">Price Change</div>
              <div className={`value ${priceChange >= 0 ? 'price-up' : 'price-down'}`}>
                {priceChange ? `${priceChange >= 0 ? '+' : ''}${priceChange}%` : 'N/A'}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChangePointChart;
