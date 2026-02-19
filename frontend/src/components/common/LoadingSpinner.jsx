import './styles/LoadingSpinner.css';
const LoadingSpinner = ({ input }) => {
  return (
    <div className="loading-container">
      <div className="loading-spinner"></div>
      <p>{`Загрузка ${input || ''}...`}</p>
    </div>
  );
};

export default LoadingSpinner;
