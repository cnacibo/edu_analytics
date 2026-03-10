import './styles/DashboardPage.css';
import BarChartDashboard from '../components/dashboard/BarChartDashboard';
import PieChartDashboard from '../components/dashboard/PieChartDashboard';
import SortedProgramsList from '../components/dashboard/SortedProgramsList';
import StatisticsCard from '../components/dashboard/StatisticsCard';
import MapDashboard from '../components/dashboard/MapDashboard';
import React from 'react';

const DashboardPage = () => {
  const stats = {
    totalPrograms: 8526,
    avgCost: 550000,
    minScore: 120,
    maxScore: 390,
  };

  return (
    <div className="dashboard-page">
      <div className="stats-grid">
        <StatisticsCard
          label="Всего программ"
          value={stats.totalPrograms}
          cardStyleName="total-programs"
        ></StatisticsCard>
        <StatisticsCard
          label="Средняя стоимость"
          value={stats.avgCost}
          cardStyleName="avg-cost"
          suffix=" ₽"
        ></StatisticsCard>
        <StatisticsCard
          label="Минимальный балл на платку"
          value={stats.minScore}
          cardStyleName="min-score"
        ></StatisticsCard>
        <StatisticsCard
          label="Максимальный балл на бюджет"
          value={stats.maxScore}
          cardStyleName="max-score"
        ></StatisticsCard>
      </div>
      <div className="graphics-row">
        <div className="graphics-card chart-card">
          <h3 className="graphics-title">Средняя стоимость по сферам и уровням образования</h3>
          <BarChartDashboard></BarChartDashboard>
        </div>
        <div className="graphics-card">
          <h3 className="graphics-title">Распределение программ по сферам</h3>
          <PieChartDashboard></PieChartDashboard>
        </div>

        <div className="graphics-card">
          <h3 className="graphics-title">Самые дорогие программы</h3>
          <SortedProgramsList></SortedProgramsList>
        </div>
      </div>
      <div className="graphics-row">
        <div className="graphics-card">
          <h3 className="graphics-title">Кем стать после</h3>
        </div>
        <div className="graphics-card">
          <h3 className="graphics-title">Распределение программ по стране</h3>
          <MapDashboard></MapDashboard>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
