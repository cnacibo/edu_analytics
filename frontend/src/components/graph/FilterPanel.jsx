import './styles/FilterPanel.css';
import React from 'react';
const FilterPanel = ({
  activeTypes,
  onTypeToggle,
  TYPE_COLORS,
  TYPE_LABELS,
  nodeDegreeMap,
  minDegree,
  onMinDegreeChange,
}) => {
  return (
    <div className="filter-group">
      <div className="node-type-filter">
        <span className="node-type-filter-label">Тип узла:</span>
        {['direction', 'subject', 'tag'].map((type) => (
          <label key={type} className="checkbox-label">
            <input
              type="checkbox"
              checked={activeTypes[type] || false}
              onChange={() => onTypeToggle(type)}
              className="custom-checkbox"
            />
            <span
              className="checkbox-mark"
              style={{ backgroundColor: TYPE_COLORS[type], opacity: 0.7 }}
            />
            <span className="checkbox-text">{TYPE_LABELS[type] || type}</span>
          </label>
        ))}
      </div>
      <div className="degree-number-filter">
        <label className="degree-number-filter-label">
          <span>Мин. связей:</span>
        </label>
        <input
          type="number"
          min={0}
          max={Math.max(...Object.values(nodeDegreeMap), 1) || 50}
          value={minDegree}
          onChange={(e) => onMinDegreeChange(parseInt(e.target.value, 10) || 0)}
          className="degree-input"
        />
      </div>
    </div>
  );
};

export default FilterPanel;
