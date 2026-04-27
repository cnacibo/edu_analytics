import React from 'react';
import './styles/GraphAnalysis.css';

const GraphAnalysis = ({ graphStats, nodeDegreeMap, TYPE_LABELS, onClose }) => {
  if (!graphStats) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Статистика графа</h2>
          <button className="modal-close" onClick={onClose}>
            ×
          </button>
        </div>

        <div className="modal-body">
          <div className="analysis-grid">
            <div className="analysis-grid-stats">
              <div className="analysis-card">
                <span className="analysis-label">Средняя степень</span>
                <div className="analysis-values">
                  {Object.entries(graphStats.typeStats).map(([type, avg]) => (
                    <div key={type} className="analysis-row">
                      <span>➖ {TYPE_LABELS[type]}</span>
                      <strong>{avg}</strong>
                    </div>
                  ))}
                </div>
              </div>

              <div className="analysis-card">
                <span className="analysis-label">Показано узлов</span>
                <div className="analysis-values">
                  {Object.entries(graphStats.typeCounts).map(([type, count]) => (
                    <div key={type} className="analysis-row">
                      <span>➖ {TYPE_LABELS[type]}</span>
                      <strong>{count}</strong>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            <div className="analysis-card">
              <span className="analysis-label">Топ-5 по связям (предметы)</span>
              <ol className="top-list">
                {graphStats.topNodes.map((node, idx) => (
                  <li key={idx}>
                    <span>{node.label}</span>
                    <span className="degree-badge">{nodeDegreeMap[node.label]}</span>
                  </li>
                ))}
              </ol>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default GraphAnalysis;
