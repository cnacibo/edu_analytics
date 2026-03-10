import './styles/StatisticsCard.css';

const StatisticsCard = ({ label, value, cardStyleName, suffix = '' }) => {
  return (
    <div className={`stat-card ${cardStyleName}`}>
      <div className="stat-content">
        <span className="stat-label">{label}</span>
        <span className="stat-value">
          {value.toLocaleString()}
          {suffix}
        </span>
      </div>
    </div>
  );
};

export default StatisticsCard;
