import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
  CartesianGrid
} from "recharts";
import { useEffect, useMemo, useState } from "react";
import API from "../services/api";

const PriceChart = ({
  changePoints = [],
  highlightedDate = null,
  showVolatility = false,
  macroToggles = { GDP: false, Inflation: false, ExchangeRate: false, Causes: false },
  closestEventDate = null,
  onDateClick = null
}) => {
  const [data, setData] = useState([]);
  const [macroData, setMacroData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [pricesRes, macroRes] = await Promise.all([
          API.get("/prices"),
          API.get("/prices/macro-overlay")
        ]);
        setData(pricesRes.data.data || []);
        setMacroData(macroRes.data.data || []);
      } catch (err) {
        setError("Failed to load chart data");
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const chartData = useMemo(() => {
    const macroMap = new Map(macroData.map((d) => [d.Date, d]));
    return data.map((point) => ({
      ...point,
      ...(macroMap.get(point.Date) || {})
    }));
  }, [data, macroData]);

  if (loading) {
    return <div className="skeleton" style={{ height: 350 }} />;
  }
  if (error) {
    return <div className="error-state">{error}</div>;
  }

  const formatDate = (dateStr) => {
    if (!dateStr) return "";
    return new Date(dateStr).toLocaleDateString("en-US", {
      year: "numeric",
      month: "short"
    });
  };

  return (
    <ResponsiveContainer width="100%" height={350}>
      <LineChart
        data={chartData}
        onClick={(state) => {
          if (onDateClick && state?.activeLabel) {
            onDateClick(state.activeLabel);
          }
        }}
      >
        <CartesianGrid strokeDasharray="3 3" stroke="#e9ecef" />
        <XAxis dataKey="Date" tickFormatter={formatDate} />
        <YAxis yAxisId="left" tickFormatter={(value) => `$${value}`} />
        <YAxis yAxisId="right" orientation="right" />
        <Tooltip />
        <Line yAxisId="left" type="monotone" dataKey="Price" stroke="#1e3a5f" dot={false} strokeWidth={2} />

        {showVolatility && (
          <Line yAxisId="right" type="monotone" dataKey="Volatility" stroke="#10b981" dot={false} />
        )}
        {macroToggles.GDP && <Line yAxisId="right" dataKey="GDP" stroke="#2d6a4f" dot={false} />}
        {macroToggles.Inflation && <Line yAxisId="right" dataKey="Inflation" stroke="#d4a373" dot={false} />}
        {macroToggles.ExchangeRate && <Line yAxisId="right" dataKey="ExchangeRate" stroke="#8b5cf6" dot={false} />}

        {changePoints.map((cp, idx) => (
          <ReferenceLine
            key={`${cp.tau_date}-${idx}`}
            x={cp.tau_date}
            yAxisId="left"
            stroke="#ef4444"
            strokeDasharray="4 4"
            label={{ value: `CP${idx + 1}`, position: "top", fill: "#ef4444" }}
          />
        ))}
        {highlightedDate && (
          <ReferenceLine x={highlightedDate} yAxisId="left" stroke="#f59e0b" strokeDasharray="2 2" />
        )}
        {macroToggles.Causes && closestEventDate && (
          <ReferenceLine
            x={closestEventDate}
            yAxisId="left"
            stroke="#0ea5e9"
            strokeDasharray="6 3"
            label={{ value: "Closest Event", position: "top", fill: "#0ea5e9" }}
          />
        )}
      </LineChart>
    </ResponsiveContainer>
  );
};

export default PriceChart;
