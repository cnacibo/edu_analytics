import "./styles/EmptyResult.css";
const EmptyResult = ({message, header = "Ничего не найдено"}) => {
    return (
            <div className="no-results">
                    <div className="no-results-icon">📭</div>
                    <h3>{header}</h3>
                {message && (
                    <p>{message}</p>
                )}

                </div>
        );
}

export default EmptyResult
