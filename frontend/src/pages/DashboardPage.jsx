import './styles/DashboardPage.css';
import BarChartDashboard from '../components/dashboard/BarChartDashboard';
import PieChartDashboard from '../components/dashboard/PieChartDashboard';
import SortedProgramsList from '../components/dashboard/SortedProgramsList';
import StatisticsCard from '../components/dashboard/StatisticsCard';
import MapDashboard from '../components/dashboard/MapDashboard';
import React, { useEffect, useState } from 'react';
import { vuzopediaApi } from '../api';

const DashboardPage = () => {
  const [stats, setStats] = useState({
    totalPrograms: 0,
    avgCost: 0,
    minScore: 0,
    maxScore: 0,
  });

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const totalProgramsResponse = await vuzopediaApi.getTotalPrograms();
      const avgCostResponse = await vuzopediaApi.getAvgCost();
      const minScoreResponse = await vuzopediaApi.getMinScore();
      const maxScoreResponse = await vuzopediaApi.getMaxScore();

      setStats({
        totalPrograms: totalProgramsResponse.data.total_programs,
        avgCost: avgCostResponse.data.average_cost,
        minScore: minScoreResponse.data.min_paid_score,
        maxScore: maxScoreResponse.data.max_budget_score,
      });
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  return (
    <div className="dashboard-page">
      <div className="stats-grid">
        <StatisticsCard
          label="Всего программ"
          value={stats.totalPrograms === 0 ? '-' : stats.totalPrograms.toLocaleString()}
          cardStyleName="total-programs"
        ></StatisticsCard>
        <StatisticsCard
          label="Средняя стоимость"
          value={stats.avgCost === 0 ? '-' : stats.avgCost.toLocaleString()}
          cardStyleName="avg-cost"
          suffix=" ₽"
        ></StatisticsCard>
        <StatisticsCard
          label="Минимальный балл на платку"
          value={stats.minScore === 0 ? '-' : stats.minScore.toLocaleString()}
          cardStyleName="min-score"
        ></StatisticsCard>
        <StatisticsCard
          label="Максимальный балл на бюджет"
          value={stats.maxScore === 0 ? '-' : stats.maxScore.toLocaleString()}
          cardStyleName="max-score"
        ></StatisticsCard>
      </div>
      <div className="graphics-row">
        <div className="graphics-card chart-card">
          <h3 className="graphics-title">Средняя стоимость по сферам и уровням образования</h3>
          <BarChartDashboard></BarChartDashboard>
        </div>
        <div className="graphics-card">
          <h3 className="graphics-title">Самые популярные сферы</h3>
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
          <p
            style={{
              fontSize: '25px',
              fontWeight: '500',
              color: '#6c757d',
              margin: '230px 0',
              textAlign: 'center',
            }}
          >
            В разработке...
          </p>
        </div>
        <div className="graphics-card">
          <h3 className="graphics-title">
            Распределение программ по стране (средняя стоимость:{' '}
            {stats.avgCost === 0 ? '-' : stats.avgCost.toLocaleString()} ₽)
          </h3>
          <MapDashboard></MapDashboard>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
