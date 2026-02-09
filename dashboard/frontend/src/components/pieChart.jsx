import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import { useEffect, useState } from "react";
import API from "../services/api";

const PriceChart = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get("/prices")
      .then(res => setData(res.data.data))
      .catch(err => console.error(err));
  }, []);

  return (
    <ResponsiveContainer width="100%" height={350}>
      <LineChart data={data}>
        <XAxis dataKey="Date" />
        <YAxis />
        <Tooltip />
        <Line
          type="monotone"
          dataKey="Price"
          stroke="#1f77b4"
          dot={false}
        />
      </LineChart>
    </ResponsiveContainer>
  );
};

export default PriceChart;
