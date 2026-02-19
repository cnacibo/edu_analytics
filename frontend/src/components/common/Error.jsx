import './styles/Error.css';
const Error = ({ onRetry, message = 'Ошибка загрузки' }) => {
  return (
    <div className="program-container">
      <div className="error-container">
        <div className="error-icon">😪</div>
        <h3>{message}</h3>
        {onRetry && (
          <button onClick={onRetry} className="retry-btn">
            Повторить
          </button>
        )}
      </div>
    </div>
  );
};

export default Error;
