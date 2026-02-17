import './styles/ProgramList.css';
import ProgramCard from './ProgramCard';
import EmptyResult from '../common/EmptyResult';

const ProgramList = ({ programs }) => {
  return (
    <div className="program-list-container">
      {programs.length === 0 ? (
        <EmptyResult message="Попробуйте изменить запрос или фильтры"></EmptyResult>
      ) : (
        <>
          <div className="programs-grid">
            {programs.map((program) => (
              <ProgramCard key={program.id} program={program} />
            ))}
          </div>
        </>
      )}
    </div>
  );
};
export default ProgramList;
