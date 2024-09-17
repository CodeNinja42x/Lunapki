import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';

function ProfitGraph() {
  const [chartData, setChartData] = useState({});

  const fetchData = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/data');
      const data = await response.json();

      setChartData({
        labels: ['BTC'],
        datasets: [
          {
            label: 'BTC Price',
            data: [parseFloat(data.price)], // Fiyatı grafiğe yerleştir
            backgroundColor: 'rgba(75, 192, 192, 0.6)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1,
          },
        ],
      });
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <div>
      <h2>BTC Price Graph</h2>
      <Line data={chartData} />
    </div>
  );
}

export default ProfitGraph;
