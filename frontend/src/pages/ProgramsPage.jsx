import ProgramList from './../components/programs/ProgramList';
import FilterBar from '../components/programs/FilterBar';
import './styles/ProgramsPage.css';
import { hseApi, vuzopediaApi } from '../api';
import { useEffect, useState } from 'react';
import Pagination from '../components/common/Pagination';
import LoadingSpinner from '../components/common/LoadingSpinner';
import Error from '../components/common/Error';
import { exportPrograms } from '../utils/export/exportPrograms';
import FormatMenu from '../components/programs/FormatMenu';
import { useSearchParams } from 'react-router-dom';

const ProgramsPage = () => {
  const [programs, setPrograms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [sourceHSE, setSourceHSE] = useState(true);
  const [showMenu, setShowMenu] = useState(false);
  const [searchParams, setSearchParams] = useSearchParams();
  const [pagination, setPagination] = useState({
    page: 1,
    size: 20,
    total: 0,
    pages: 0,
  });

  const [filters, setFilters] = useState({
    q: '',
    max_cost: '',
    max_budget_score: '',
    max_paid_score: '',
    study_type: '',
  });

  const [inputFilters, setInputFilters] = useState({
    q: '',
    max_cost: '',
    max_budget_score: '',
    max_paid_score: '',
    study_type: '',
  });

  useEffect(() => {
    const q = searchParams.get('q') ?? '';
    const max_cost = searchParams.get('max_cost') ?? '';
    const max_budget_score = searchParams.get('max_budget_score') ?? '';
    const max_paid_score = searchParams.get('max_paid_score') ?? '';
    const study_type = searchParams.get('study_type') ?? '';
    const page = Number(searchParams.get('page') ?? 1);
    const source = searchParams.get('source') ?? (sourceHSE ? 'hse' : 'vuz');

    setInputFilters({ q, max_cost, max_budget_score, max_paid_score, study_type });
    setFilters({ q, max_cost, max_budget_score, max_paid_score, study_type });
    setPagination((prev) => ({ ...prev, page }));
    setSourceHSE(source === 'hse');
  }, [searchParams]);

  useEffect(() => {
    fetchPrograms();
  }, [pagination.page, filters, sourceHSE]);

  const fetchPrograms = async () => {
    setLoading(true);
    setError(null);
    setPrograms([]);
    try {
      const params = {
        page: pagination.page,
        size: pagination.size,
      };

      if (filters.q) {
        params.q = filters.q;
      }

      if (filters.max_cost) {
        params.max_cost = filters.max_cost;
      }

      if (!sourceHSE && filters.max_budget_score) {
        params.max_budget_score = filters.max_budget_score;
      }

      if (!sourceHSE && filters.max_paid_score) {
        params.max_paid_score = filters.max_paid_score;
      }

      if (sourceHSE && filters.study_type) {
        params.study_type = filters.study_type;
      }

      Object.keys(params).forEach((key) => {
        if (params[key] === '') delete params[key];
      });

      let response;
      if (sourceHSE) {
        response = await hseApi.getPrograms(params);
      } else {
        response = await vuzopediaApi.getPrograms(params);
      }

      const programsData = (response.programs || []).map((program) => ({
        ...program,
        source: sourceHSE ? 'hse' : 'vuz',
      }));

      setPrograms(programsData);

      setPagination((prev) => ({
        ...prev,
        total: response.total || 0,
        pages: response.total_pages || 0,
      }));
    } catch (error) {
      setError(error.message);
      console.error('Error fetching programs:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (newFilters = inputFilters) => {
    setFilters((prev) => ({ ...prev, ...newFilters }));
    setPagination((prev) => ({ ...prev, page: 1 }));
    const next = {
      ...Object.fromEntries(searchParams.entries()),
      ...newFilters,
      page: 1,
      source: sourceHSE ? 'hse' : 'vuz',
    };

    Object.keys(next).forEach((k) => {
      if (next[k] === '' || next[k] == null) delete next[k];
    });
    setSearchParams(next);
  };

  const handleInputChange = (partial) => {
    setInputFilters((prev) => ({ ...prev, ...partial }));
  };

  const handleSourceChange = (newSourceValue) => {
    setSourceHSE(newSourceValue);
    setPagination((prev) => ({ ...prev, page: 1 }));
    const next = {
      ...Object.fromEntries(searchParams.entries()),
      source: newSourceValue ? 'hse' : 'vuz',
      page: 1,
    };
    Object.keys(next).forEach((k) => {
      if (next[k] === '' || next[k] == null) delete next[k];
    });
    setSearchParams(next);
  };

  const handlePageChange = (newPage) => {
    setPagination((prev) => ({ ...prev, page: newPage }));
    const next = {
      ...Object.fromEntries(searchParams.entries()),
      page: newPage,
    };
    Object.keys(next).forEach((k) => {
      if (next[k] === '' || next[k] == null) delete next[k];
    });
    setSearchParams(next);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleSaveToFile = async (format) => {
    if (programs && programs.length > 0) {
      try {
        const params = {
          page: 1,
          size: pagination.total,
        };

        if (filters.q) {
          params.q = filters.q;
        }

        if (filters.max_cost) {
          params.max_cost = filters.max_cost;
        }

        if (!sourceHSE && filters.max_budget_score) {
          params.max_budget_score = filters.max_budget_score;
        }

        if (!sourceHSE && filters.max_paid_score) {
          params.max_paid_score = filters.max_paid_score;
        }

        if (sourceHSE && filters.study_type) {
          params.study_type = filters.study_type;
        }

        Object.keys(params).forEach((key) => {
          if (params[key] === '') delete params[key];
        });
        let response;
        if (sourceHSE) {
          response = await hseApi.getPrograms(params);
        } else {
          response = await vuzopediaApi.getPrograms(params);
        }
        exportPrograms(
          response.programs,
          sourceHSE ? 'hse' : 'vuz',
          filters,
          pagination.total,
          format
        );
        setShowMenu(false);
      } catch (error) {
        console.error('Ошибка при сохранении файла:', error);
        alert('Не удалось сохранить файл!');
      }
    }
  };

  const toggleMenu = () => {
    setShowMenu(!showMenu);
  };

  if (loading) {
    return <LoadingSpinner input="программ"></LoadingSpinner>;
  }

  if (error && programs.length === 0) {
    return <Error onRetry={fetchPrograms} message="Не удалось загрузить программы"></Error>;
  }

  return (
    <div className="programs-page">
      <FilterBar
        filters={inputFilters}
        onInputChange={handleInputChange}
        onFilterChange={handleFilterChange}
        onSourceChange={handleSourceChange}
        source={sourceHSE}
      ></FilterBar>
      <div className="save-button-container">
        {programs.length > 0 && (
          <button className="save-button" onClick={toggleMenu} disabled={programs.length === 0}>
            <span className="save-icon">💾</span>
            Сохранить в файл
          </button>
        )}
        {showMenu && <FormatMenu onSave={handleSaveToFile} />}
      </div>

      <ProgramList programs={programs} loading={loading} error={error}></ProgramList>
      <Pagination
        currentPage={pagination.page}
        totalPages={pagination.pages}
        onPageChange={handlePageChange}
      ></Pagination>
    </div>
  );
};

export default ProgramsPage;
