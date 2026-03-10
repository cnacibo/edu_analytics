import './styles/PieChartDashboard.css';
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import React from 'react';

const PieChartDashboard = () => {
  const stats = {
    spheres: {
      it: 5134,
      economics: 1876,
      humanities: 1643,
      engineering: 1542,
      science: 1331,
    },
  };
  const sphereData = [
    { name: 'IT', value: stats.spheres.it },
    { name: 'Экономика', value: stats.spheres.economics },
    { name: 'Гуманитарные', value: stats.spheres.humanities },
    { name: 'Инженерия', value: stats.spheres.engineering },
    { name: 'Естественные науки', value: stats.spheres.science },
  ];

  const COLORS = ['#f39cbb', '#f16a8c', '#870e1d', '#dd2d4a', '#457b9d'];

  return (
    <div className="pie-chart-container">
      <ResponsiveContainer>
        <PieChart margin={{ top: 0, right: 20, left: 20, bottom: 30 }}>
          <Pie
            data={sphereData}
            cx="50%"
            cy="50%"
            innerRadius={55}
            outerRadius={95}
            dataKey="value"
            nameKey="name"
            label
          >
            {sphereData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index]} />
            ))}
          </Pie>

          <Tooltip
            contentStyle={{
              backgroundColor: 'rgba(255, 255, 255, 0.95)',
              border: '1px solid #dee2e6',
              borderRadius: '8px',
              padding: '5px 10px',
              boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
            }}
            labelStyle={{
              fontWeight: 600,
              marginBottom: '0',
            }}
            itemStyle={{
              color: 'black',
              fontWeight: 700,
              fontSize: '14px',
            }}
            formatter={(value) => (
              <span style={{ color: '#495057', fontWeight: 600 }}>{value}</span>
            )}
          />
          <Legend
            wrapperStyle={{
              fontSize: '13px',
              fontWeight: 600,
              marginTop: '20px',
            }}
            formatter={(value) => <span style={{ color: '#495057' }}>{value}</span>}
            iconSize={12}
            iconType="circle"
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
};
export default PieChartDashboard;
