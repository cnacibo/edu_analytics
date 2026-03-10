import './styles/BarChartDashboard.css';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import React from 'react';

const stats = {
  costByLevelAndSphere: {
    it: {
      bachelor: 600000,
      master: 700000,
      specialist: 650000,
    },
    economics: {
      bachelor: 450000,
      master: 550000,
      specialist: 500000,
    },
    humanities: {
      bachelor: 380000,
      master: 450000,
      specialist: 400000,
    },
    engineering: {
      bachelor: 550000,
      master: 650000,
      specialist: 600000,
    },
    science: {
      bachelor: 500000,
      master: 600000,
      specialist: 550000,
    },
    medicine: {
      bachelor: 480000,
      master: 580000,
      specialist: 530000,
    },
    creative: {
      bachelor: 350000,
      master: 420000,
      specialist: 380000,
    },
  },
};
const spheresOrder = [
  { key: 'it', name: 'IT' },
  { key: 'economics', name: 'Экономика' },
  { key: 'humanities', name: 'Гуманитарные' },
  { key: 'engineering', name: 'Инженерия' },
  { key: 'science', name: 'Естественные науки' },
  { key: 'medicine', name: 'Медицина' },
  { key: 'creative', name: 'Творческие' },
];

// Prepare data for Recharts
const chartData = spheresOrder.map((sphere) => ({
  name: sphere.name,
  bachelor: stats.costByLevelAndSphere[sphere.key].bachelor,
  master: stats.costByLevelAndSphere[sphere.key].master,
  specialist: stats.costByLevelAndSphere[sphere.key].specialist,
}));

const BarChartDashboard = () => {
  return (
    <div className="bar-chart-container">
      <ResponsiveContainer>
        <BarChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" horizontal={true} vertical={false} />
          <XAxis
            dataKey="name"
            tick={{ fill: '#495057', fontSize: 12 }}
            axisLine={{ stroke: '#dee2e6' }}
            tickLine={{ stroke: '#dee2e6' }}
            interval={0}
            angle={-45}
            textAnchor="end"
            height={100}
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
          <Legend
            wrapperStyle={{
              fontSize: '13px',
              fontWeight: 600,
            }}
            formatter={(value) => <span style={{ color: '#495057' }}>{value}</span>}
            iconSize={12}
            iconType="circle"
          />
          <Bar dataKey="bachelor" fill="#f39cbb" name="Бакалавриат" radius={[4, 4, 0, 0]} />
          <Bar dataKey="master" fill="#cbeef3" name="Магистратура" radius={[4, 4, 0, 0]} />
          <Bar dataKey="specialist" fill="#870e1d" name="Специалитет" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default BarChartDashboard;
