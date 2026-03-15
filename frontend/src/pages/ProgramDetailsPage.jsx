import CoursesList from '../components/programs/CoursesList';
import { hseApi, vuzopediaApi } from '../api';
import { useLocation, useNavigate, useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import './styles/ProgramDetailsPage.css';
import './styles/ProgramsPage.css';
import Pagination from '../components/common/Pagination';
import LoadingSpinner from '../components/common/LoadingSpinner';
import Error from '../components/common/Error';

const ProgramDetailsPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const params = useParams();
  const [program, setProgram] = useState(location.state?.program || null);
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(!location.state?.program);
  const [error, setError] = useState(null);
  const [loadingCourses, setLoadingCourses] = useState(false);
  const [coursesError, setCoursesError] = useState(null);
  const [pagination, setPagination] = useState({
    page: 1,
    size: 10,
    total: 0,
    pages: 0,
  });

  const sourceHSE = location.pathname.includes('/hse/');
  const programId = params.id;

  useEffect(() => {
    if (!program && programId) {
      fetchProgramById();
    }
  }, [programId]);

  useEffect(() => {
    if (program && programId) {
      fetchCoursesByProgramId();
    }
  }, [pagination.page, program, programId]);

  const handlePageChange = (newPage) => {
    setPagination((prev) => ({ ...prev, page: newPage }));
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const fetchProgramById = async () => {
    setLoading(true);
    setError(null);
    try {
      let response;
      if (sourceHSE) {
        response = await hseApi.getProgram(programId);
      } else {
        response = await vuzopediaApi.getProgram(programId);
      }

      setProgram({
        ...response,
        source: sourceHSE ? 'hse' : 'vuz',
      });
    } catch (error) {
      setError(error.message);
      console.error('Error fetching program:', error);
    } finally {
      setLoading(false);
    }
  };
  const fetchCoursesByProgramId = async () => {
    setLoadingCourses(true);
    setCoursesError(null);
    try {
      const paginationParams = {
        page: pagination.page,
        size: pagination.size,
      };
      let response = [];
      if (sourceHSE) {
        response = await hseApi.getCourses(programId, paginationParams);
        const coursesData = response.courses || [];
        setCourses(coursesData);
      }
      setPagination((prev) => ({
        ...prev,
        total: response.total || 0,
        pages: response.total_pages || 0,
      }));
    } catch (error) {
      setCoursesError(error.message);
      console.error('Error fetching courses:', error);
    } finally {
      setLoadingCourses(false);
    }
  };

  if (loading) {
    return (
      <>
        <button className="pdp-back-button" onClick={() => navigate('/programs')}>
          Назад к списку
        </button>
        <LoadingSpinner input="программы"></LoadingSpinner>
      </>
    );
  }

  if (error || !program) {
    return (
      <div className="program-container">
        <button className="pdp-back-button" onClick={() => navigate('/programs')}>
          Назад к списку
        </button>
        <Error onRetry={fetchProgramById} message="Не удалось загрузить программу"></Error>
      </div>
    );
  }

  return (
    <div className="program-details-page">
      <button className="pdp-back-button" onClick={() => navigate('/programs')}>
        Назад к списку
      </button>
      <div className="pdp-header">
        <div className="pdp-icon">{sourceHSE ? '🎓' : '🏛️'}</div>
        <div className="pdp-title-wrapper">
          <h1 className="pdp-title">{program.name}</h1>
          <div className="pdp-meta">
            {sourceHSE && <span className="pdp-type">{program.study_type}</span>}
            <span className="pdp-badge">{sourceHSE ? 'НИУ ВШЭ' : 'Vuzopedia'}</span>
          </div>
        </div>
        {sourceHSE && <button className="pdp-graph-button">Построить граф</button>}
      </div>
      <div className="pdp-info-grid">
        <div className="pdp-card">
          <h3 className="pdp-card-title">Основная информация</h3>
          <div className="pdp-card-content">
            <div className="pdp-info-row">
              <span className="pdp-info-label">Код программы:</span>
              <span className="pdp-info-value pdp-info-code">{program.code || '—'}</span>
            </div>
            <div className="pdp-info-row">
              <span className="pdp-info-label">Стоимость обучения:</span>
              <span className="pdp-info-value pdp-info-cost">
                {program.cost ? `${program.cost.toLocaleString()} ₽/год` : '—'}
              </span>
            </div>
          </div>
        </div>

        {sourceHSE && (
          <div className="pdp-card">
            <h3 className="pdp-card-title">Места</h3>
            <div className="pdp-card-content">
              <div className="pdp-info-row">
                <span className="pdp-info-label">Бюджетные места:</span>
                <span className="pdp-info-value pdp-info-highlight">
                  {program.budget_places || '—'}
                </span>
              </div>
              <div className="pdp-info-row">
                <span className="pdp-info-label">Платные места:</span>
                <span className="pdp-info-value pdp-info-highlight">
                  {program.paid_places || '—'}
                </span>
              </div>
              <div className="pdp-info-row">
                <span className="pdp-info-label">Места для иностранцев:</span>
                <span className="pdp-info-value pdp-info-highlight">
                  {program.foreigners_places || '—'}
                </span>
              </div>
            </div>
          </div>
        )}
        {!sourceHSE && (
          <>
            <div className="pdp-card">
              <h3 className="pdp-card-title">О программе</h3>
              <div className="pdp-card-content">
                <div className="pdp-info-row">
                  <span className="pdp-info-label">Сфера:</span>
                  <span className="pdp-info-value">{program.sphere || '—'}</span>
                </div>
                <div className="pdp-info-row pdp-info-career">
                  <span className="pdp-info-label">Карьерные перспективы:</span>
                  <span className="pdp-info-value">{program.career_prospects || '—'}</span>
                </div>
              </div>
            </div>

            <div className="pdp-card">
              <h3 className="pdp-card-title">Проходные баллы</h3>
              <div className="pdp-card-content">
                <div className="pdp-info-row">
                  <span className="pdp-info-label">Бюджет:</span>
                  <span className="pdp-info-value pdp-info-highlight">
                    {program.min_budget_score || '—'}
                  </span>
                </div>
                <div className="pdp-info-row">
                  <span className="pdp-info-label">Платное:</span>
                  <span className="pdp-info-value pdp-info-highlight">
                    {program.min_paid_score || '—'}
                  </span>
                </div>
              </div>
            </div>
          </>
        )}
      </div>
      {sourceHSE ? (
        <div className="pdp-courses-section">
          <h3 className="pdp-section-title">Дисциплины программы</h3>
          <CoursesList courses={courses} loading={loadingCourses} error={coursesError} />
          <Pagination
            currentPage={pagination.page}
            totalPages={pagination.pages}
            onPageChange={handlePageChange}
          ></Pagination>
        </div>
      ) : (
        <div className="pdp-courses-section pdp-no-courses">
          <p>Информация о курсах доступна только для программ НИУ ВШЭ</p>
        </div>
      )}
    </div>
  );
};

export default ProgramDetailsPage;
