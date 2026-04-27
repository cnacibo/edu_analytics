import './styles/BarChartDashboard.css';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import React, { useEffect, useState } from 'react';
import { chartsApi } from '../../api';
import LoadingSpinner from '../common/LoadingSpinner';
import Error from '../common/Error';

const BarChartDashboard = () => {
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  const [barChartData, setBarChartData] = useState([]);

  useEffect(() => {
    fetchBarChartData();
  }, []);

  const fetchBarChartData = async () => {
    setLoading(true);
    setError(null);
    try {
      const sphereCostResponse = await chartsApi.getSphereCostData();
      const rawData = sphereCostResponse.data.spheres_level_cost_dist;
      const charData = Object.entries(rawData).map(([sphere, costs]) => ({
        name: sphere,
        bachelor: costs.bachelor,
        master: costs.master,
      }));
      setBarChartData(charData);
    } catch (error) {
      setError(error.message);
      console.error('Error fetching stats:', error);
    } finally {
      setLoading(false);
    }
  };

  const CustomXAxisTick = (props) => {
    const { x, y, payload } = props;
    const words = payload.value.split(' ');
    const maxCharsPerLine = 15;

    const lines = [];
    let currentLine = words[0];
    for (let i = 1; i < words.length; i++) {
      if ((currentLine + ' ' + words[i]).length > maxCharsPerLine) {
        lines.push(currentLine);
        currentLine = words[i];
      } else {
        currentLine += ' ' + words[i];
      }
    }
    lines.push(currentLine);

    const offsetY = 5;

    return (
      <g transform={`translate(${x},${y + offsetY})`}>
        {lines.map((line, index) => (
          <text
            key={index}
            x={0}
            y={index * 14}
            textAnchor="end"
            fill="#495057"
            fontSize={12}
            transform="rotate(-45)"
          >
            {line}
          </text>
        ))}
      </g>
    );
  };

  if (loading) {
    return <LoadingSpinner input="графика"></LoadingSpinner>;
  }

  if (error || barChartData.length === 0) {
    return (
      <Error onRetry={fetchBarChartData} message="Не удалось загрузить данные для графика"></Error>
    );
  }

  return (
    <div className="bar-chart-container">
      <ResponsiveContainer width="100%" height={400}>
        <BarChart
          data={barChartData}
          margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
          barSize={25}
        >
          <CartesianGrid strokeDasharray="3 3" horizontal={true} vertical={false} />
          <XAxis
            dataKey="name"
            tick={<CustomXAxisTick />}
            interval={0}
            height={100}
            axisLine={false}
          />
          <YAxis
            tick={{ fill: '#6c757d', fontSize: 11 }}
            axisLine={{ stroke: '#dee2e6' }}
            tickLine={{ stroke: '#dee2e6' }}
            tickFormatter={(value) => `${value / 1000} K`}
          />
          <Tooltip
            formatter={(value) => `${value.toLocaleString()} ₽`}
            contentStyle={{
              backgroundColor: 'rgba(255, 255, 255, 0.95)',
              border: '1px solid #dee2e6',
              borderRadius: '8px',
              padding: '10px',
              boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
            }}
            labelStyle={{
              color: '#212529',
              fontWeight: 600,
              marginBottom: '5px',
            }}
            itemStyle={{
              color: '#495057',
              fontSize: '12px',
            }}
          />
          <Bar dataKey="bachelor" fill="#f39cbb" name="Бакалавриат" radius={[4, 4, 0, 0]} />
          <Bar dataKey="master" fill="#dd2d4a" name="Магистратура" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>

      <div className="custom-legend">
        <span className="legend-item">
          <span className="legend-color" style={{ backgroundColor: '#f39cbb' }} />
          Бакалавриат
        </span>
        <span className="legend-item">
          <span className="legend-color" style={{ backgroundColor: '#dd2d4a' }} />
          Магистратура
        </span>
      </div>
    </div>
  );
};

export default BarChartDashboard;
