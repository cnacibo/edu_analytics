import './styles/CourseCard.css';
const CourseCard = ({ course }) => {
  const getStatusColor = (status) => {
    switch (status?.toLowerCase()) {
      case 'обязательная':
        return '#28a745';
      case 'по выбору':
        return '#ffc107';
      default:
        return '#6c757d';
    }
  };
  const getYearLabel = (year) => {
    const years = ['1-й курс', '2-й курс', '3-й курс', '4-й курс'];
    return years[year - 1] || `${year}-й курс`;
  };

  return (
    <div className="cc-card">
      <div className="cc-header">
        <div className="cc-title-wrapper">
          <h4 className="cc-title">{course.title}</h4>
          <div className="cc-meta">
            <span className="cc-track">{course.track || 'Нет информации о специализации'}</span>
            <span className="cc-language">{course.language || 'Русский'}</span>
          </div>
        </div>
      </div>

      <div className="cc-content">
        <div className="cc-info-grid">
          <div className="cc-info-item">
            <span className="cc-info-label">Кредиты</span>
            <span className="cc-info-value cc-credits">{course.credits}</span>
          </div>
          <div className="cc-info-item">
            <span className="cc-info-label">Год</span>
            <span className="cc-info-value">{getYearLabel(course.year)}</span>
          </div>
          <div className="cc-info-item">
            <span className="cc-info-label">Модуль</span>
            <span className="cc-info-value">{course.module || 'Нет информации'}</span>
          </div>
        </div>
        <div className="cc-status-row">
          <span
            className="cc-status-badge"
            style={{ backgroundColor: getStatusColor(course.status) }}
          >
            {course.status || 'Обязательная'}
          </span>
        </div>
        {course.content && (
          <div className="cc-section">
            <div className="cc-section-title">Содержание</div>
            <p className="cc-content-text">{course.content || 'Нет информации'}</p>
          </div>
        )}
        {course.results && (
          <div className="cc-section">
            <div className="cc-section-title">Результаты освоения</div>
            <p className="cc-results">{course.results || 'Нет информации'}</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default CourseCard;
