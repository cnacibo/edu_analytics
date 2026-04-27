import './styles/SortedProgramsList.css';
import React, { useEffect, useState } from 'react';
import { vuzopediaApi } from '../../api';
import LoadingSpinner from '../common/LoadingSpinner';
import Error from '../common/Error';

const SortedProgramsList = () => {
  const [avgCostTopTen, setAvgCostTopTen] = useState(0);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  const [topPrograms, setTopPrograms] = useState([]);

  useEffect(() => {
    fetchAvgCostTopTen();
    fetchTopPrograms();
  }, []);

  const fetchAvgCostTopTen = async () => {
    try {
      const avgCostTopTenResponse = await vuzopediaApi.getAvgCostTopTen();
      setAvgCostTopTen(avgCostTopTenResponse.data.avg_cost_top10);
    } catch (error) {
      console.error('Error fetching avg cost for top ten:', error);
    }
  };

  const fetchTopPrograms = async () => {
    setLoading(true);
    setError(false);
    try {
      const avgCostTopTenResponse = await vuzopediaApi.getTopProgramsByCost();
      setTopPrograms(avgCostTopTenResponse.data.top_programs);
    } catch (error) {
      console.error('Error fetching top ten programs:', error);
    } finally {
      setLoading(false);
    }
  };

  const getLevelInfo = (level) => {
    const colors = {
      bachelor: {
        background: '#cceff1',
        text: 'black',
        name: 'Бакалавр',
      },
      master: {
        background: '#f39dbc',
        text: 'white',
        name: 'Магистр',
      },
    };
    return (
      colors[level] || {
        background: '#6c757d',
        text: 'white',
        name: 'Нет информации',
      }
    );
  };

  if (loading) {
    return <LoadingSpinner input="списка"></LoadingSpinner>;
  }

  if (error || topPrograms.length === 0) {
    return (
      <Error onRetry={fetchTopPrograms} message="Не удалось загрузить данные для списка"></Error>
    );
  }

  return (
    <div className="top-programs-container">
      <div className="top-programs-list">
        {topPrograms.map((program, index) => (
          <div key={index} className="top-program-item">
            <div className="top-program-rank">
              <span className={`top-rank-badge top-rank-${index + 1}`}>{index + 1}</span>
            </div>

            <div className="top-program-info">
              <div className="top-program-header">
                <h4 className="top-program-name">{program.name}</h4>
              </div>

              <div className="top-program-details">
                <div className="top-main-details">
                  <span className="top-program-cost">{program.cost.toLocaleString()} ₽</span>
                </div>
                <div className="top-extra-details">
                  {program.min_budget_score && (
                    <span className="top-program-score">Баллы: {program.min_budget_score}</span>
                  )}
                  {program.level && (
                    <span
                      className="top-program-level"
                      style={{
                        backgroundColor: getLevelInfo(program.level).background,
                        color: getLevelInfo(program.level).text,
                      }}
                    >
                      {getLevelInfo(program.level).name}
                    </span>
                  )}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="top-programs-footer">
        <span className="top-avg-cost">
          Средняя стоимость в топ-10: {avgCostTopTen === 0 ? '-' : avgCostTopTen.toLocaleString()} ₽
        </span>
      </div>
    </div>
  );
};

export default SortedProgramsList;
