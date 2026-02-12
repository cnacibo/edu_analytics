import './styles/ProgramCard.css'
const ProgramCard = ({program}) => {

    return (
        <div className="program-card">
            <div className="card-header">
                <div className="card-avatar">
                  📚
                </div>
                <div className="card-title">
                  <h3 className="program-name">{program.name}</h3>
                  <p className="program-study-type">
                    {program.study_type || 'No information'}
                  </p>
                </div>
            </div>
            <div className="card-content">
                <div className="info-row">
                    <span className="info-label">Код:</span>
                    <span className="info-value">{program.code || 'No information'}</span>
                </div>
                <div className="info-row">
                    <span className="info-label">Стоимость:</span>
                    <span className="info-value">{program.cost ? `${program.cost} ₽` : 'No information'}</span>
                </div>
            </div>
            <button className="card-actions">
                <div className="view-details">
                  View Details
                </div>
            </button>
        </div>
    );
}

export default ProgramCard;
