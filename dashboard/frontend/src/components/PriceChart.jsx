import { 
  LineChart, Line, XAxis, YAxis, Tooltip, 
  ResponsiveContainer, ReferenceLine, CartesianGrid,
  AreaChart, Area
} from "recharts";
import { useEffect, useState } from "react";
import API from "../services/api";

const PriceChart = ({ changePoint = null, highlightedDate = null, showVolatility = false }) => {
  const [data, setData] = useState([]);
  const [volatilityData, setVolatilityData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        
        // Fetch price data
        const response = await API.get("/prices");
        setData(response.data.data || []);
        
        // Fetch volatility data if needed
        if (showVolatility) {
          try {
            const volRes = await API.get("/prices/volatility?window=30");
            setVolatilityData(volRes.data.data || []);
          } catch (volErr) {
            console.warn("Volatility data unavailable:", volErr);
          }
        }
        
        setError(null);
      } catch (err) {
        console.error("Error fetching price data:", err);
        setError("Failed to load price data");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [showVolatility]);

  if (loading) {
    return (
      <ResponsiveContainer width="100%" height={350}>
        <div className="loading-card skeleton" style={{ height: 350 }}></div>
      </ResponsiveContainer>
    );
  }

  if (error) {
    return (
      <div className="error-state" style={{ height: 350 }}>
        <div className="error-icon">⚠️</div>
        <p>{error}</p>
      </div>
    );
  }

  const formatDate = (dateStr) => {
    if (!dateStr) return '';
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'short',
      day: 'numeric'
    });
  };

  // Merge volatility data with price data if showing volatility
  const chartData = showVolatility && volatilityData.length > 0
    ? data.map(item => {
        const volItem = volatilityData.find(v => v.Date === item.Date);
        return {
          ...item,
          Volatility: volItem?.Volatility || null
        };
      })
    : data;

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="custom-tooltip">
          <p style={{ fontWeight: 600, marginBottom: 4 }}>{formatDate(label)}</p>
          <p style={{ color: '#1e3a5f' }}>
            Price: <strong>${Number(data.Price).toFixed(2)}</strong>
          </p>
          {showVolatility && data.Volatility != null && (
            <p style={{ color: '#6c757d', fontSize: '0.85rem' }}>
              Volatility: <strong>{data.Volatility.toFixed(4)}</strong>
            </p>
          )}
        </div>
      );
    }
    return null;
  };

  // Create reference lines for change point and highlighted date
  const referenceLines = [];
  
  if (changePoint) {
    referenceLines.push(
      <ReferenceLine
        key="change-point"
        x={changePoint}
        stroke="#ef4444"
        strokeDasharray="5 5"
        label={{
          value: 'Change Point',
          position: 'top',
          fill: '#ef4444',
          fontSize: 11,
          fontWeight: 500
        }}
      />
    );
  }
  
  if (highlightedDate && highlightedDate !== changePoint) {
    referenceLines.push(
      <ReferenceLine
        key="highlighted"
        x={highlightedDate}
        stroke="#d4a373"
        strokeDasharray="3 3"
        label={{
          value: 'Event',
          position: 'top',
          fill: '#d4a373',
          fontSize: 11,
          fontWeight: 500
        }}
      />
    );
  }

  if (showVolatility) {
    return (
      <ResponsiveContainer width="100%" height={350}>
        <AreaChart data={chartData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e9ecef" />
          <XAxis 
            dataKey="Date" 
            tickFormatter={formatDate}
            tick={{ fill: '#6c757d', fontSize: 11 }}
            axisLine={{ stroke: '#e9ecef' }}
          />
          <YAxis 
            yAxisId="volatility"
            tick={{ fill: '#6c757d', fontSize: 11 }}
            orientation="right"
          />
          <Tooltip content={<CustomTooltip />} />
          <Area
            yAxisId="volatility"
            type="monotone"
            dataKey="Volatility"
            stroke="#10b981"
            fill="rgba(16, 185, 129, 0.1)"
            strokeWidth={2}
          />
          {referenceLines}
        </AreaChart>
      </ResponsiveContainer>
    );
  }

  return (
    <ResponsiveContainer width="100%" height={350}>
      <LineChart data={data} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#e9ecef" />
        <XAxis 
          dataKey="Date" 
          tickFormatter={formatDate}
          tick={{ fill: '#6c757d', fontSize: 11 }}
          axisLine={{ stroke: '#e9ecef' }}
        />
        <YAxis 
          tick={{ fill: '#6c757d', fontSize: 11 }}
          axisLine={{ stroke: '#e9ecef' }}
          tickFormatter={(value) => `$${value}`}
        />
        <Tooltip content={<CustomTooltip />} />
        <Line
          type="monotone"
          dataKey="Price"
          stroke="#1e3a5f"
          strokeWidth={2}
          dot={false}
          activeDot={{ r: 6, fill: '#1e3a5f' }}
        />
        {referenceLines}
      </LineChart>
    </ResponsiveContainer>
  );
};

export default PriceChart;
