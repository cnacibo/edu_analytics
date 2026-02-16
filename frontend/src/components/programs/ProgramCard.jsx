import './styles/ProgramCard.css'
import { useNavigate } from 'react-router-dom';
import ProgramDetailsPage from "../../pages/ProgramDetailsPage";
const ProgramCard = ({program}) => {
    const navigate = useNavigate();

    const openDetailsPage = (program) => {
        const source = program.source || 'hse';
        const basePath = source === 'hse' ? '/programs/hse' : '/programs/vuz';

        navigate(`${basePath}/${program.id}`, { state: { program } })
    }

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
            <button className="card-actions" onClick= {() => openDetailsPage(program)}>
                <div className="view-details">
                  View Details
                </div>
            </button>
        </div>
    );
}

export default ProgramCard;
