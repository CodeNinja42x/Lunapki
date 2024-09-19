// src/components/ProfitGraph.js
import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS } from 'chart.js/auto';

const ProfitGraph = () => {
  const [chartData, setChartData] = useState({});
  const [error, setError] = useState(null);

  const fetchChartData = async () => {
    try {
      const response = await fetch(process.env.REACT_APP_API_URL || 'http://localhost:5000/api/data');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const result = await response.json();

      const labels = result.map((dataPoint) => dataPoint.date);
      const data = result.map((dataPoint) => dataPoint.profit);

      setChartData({
        labels: labels,
        datasets: [
          {
            label: 'Profit Over Time',
            data: data,
            borderColor: 'rgba(75,192,192,1)',
            fill: false,
          },
        ],
      });
    } catch (error) {
      console.error('Error fetching data:', error);
      setError(error);
    }
  };

  useEffect(() => {
    fetchChartData();
  }, []);

  if (error) {
    return <div>Error fetching data: {error.message}</div>;
  }

  return (
    <div>
      {chartData.labels ? (
        <Line data={chartData} />
      ) : (
        <div>Loading chart data...</div>
      )}
    </div>
  );
};

export default ProfitGraph;
