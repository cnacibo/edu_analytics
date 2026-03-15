import './styles/ProgramCard.css';
import { useNavigate } from 'react-router-dom';
const ProgramCard = ({ program }) => {
  const navigate = useNavigate();

  const openDetailsPage = (program) => {
    const source = program.source || 'hse';
    const basePath = source === 'hse' ? '/programs/hse' : '/programs/vuz';

    navigate(`${basePath}/${program.id}`, { state: { program } });
  };
  const source = program.source || 'hse';

  return (
    <div className="program-card">
      <div className="card-header">
        <div className="card-avatar">📚</div>
        <div className="card-title">
          <h3 className="program-name">{program.name}</h3>
          {source === 'hse' && (
            <p className="program-header-info">{program.study_type || 'No information'}</p>
          )}
          {source === 'vuz' && (
            <p className="program-header-info">{program.sphere || 'No information'}</p>
          )}
        </div>
      </div>
      <div className="card-content">
        <div className="info-row">
          <span className="info-label">Код:</span>
          <span className="info-value">{program.code || 'No information'}</span>
        </div>
        <div className="info-row">
          <span className="info-label">Стоимость:</span>
          <span className="info-value">
            {program.cost ? `${program.cost} ₽` : 'No information'}
          </span>
        </div>
      </div>
      <button className="card-actions" onClick={() => openDetailsPage(program)}>
        <div className="view-details">View Details</div>
      </button>
    </div>
  );
};

export default ProgramCard;
