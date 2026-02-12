import './styles/ProgramList.css'
import ProgramCard from "./ProgramCard";

const ProgramList = ({programs}) => {

    return (
        <div className="program-list-container">
            {programs.length === 0 ? (
                <div className="no-results">
                    <div className="no-results-icon">📭</div>
                    <h3>No Programs Found</h3>
                    <p>Try adjusting your search or filters</p>
                </div>
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

}
export default ProgramList;
