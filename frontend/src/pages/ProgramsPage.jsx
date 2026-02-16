import ProgramList from './../components/programs/ProgramList';
import FilterBar from "../components/programs/FilterBar";
import './styles/ProgramsPage.css'
import {hseApi, vuzopediaApi} from "../api";
import {useEffect, useState} from "react";
const ProgramsPage = () => {
    const [programs, setPrograms] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [sourceHSE, setSourceHSE] = useState(true);
    const [pagination, setPagination] = useState({
        page: 1,
        size: 4,
        total: 0,
        pages: 0
    });

    const [filters, setFilters] = useState({
        max_cost: '',
        min_score: '',
        q: ''
    });

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

            if (!sourceHSE && filters.min_score) {
                params.min_score = filters.min_score;
            }

            Object.keys(params).forEach(key => {
                if (params[key] === '') delete params[key];
            });

            let response;
            if (sourceHSE) {
                response = await hseApi.getPrograms(params);
            } else {
                response = await vuzopediaApi.getPrograms(params);
            }

            const programsData = (response.programs || []).map(program => ({
                ...program,
                source: sourceHSE ? 'hse' : 'vuz'
            }))


            setPrograms(programsData);

            setPagination(prev => ({
                ...prev,
                total: response.total || 0,
                pages: response.total_pages || 0
            }));

        } catch (error) {
            setError(error.message);
            console.error('Error fetching programs:', error);
        } finally {
            setLoading(false);
        }
    }

    const handleSearch = (searchQuery) => {
        setFilters(prev => ({
            ...prev,
            q: searchQuery
        }));
        setPagination(prev => ({ ...prev, page: 1 }));
    };

    const handleFilterChange = (newFilters) => {
        setFilters(prev => ({
            ...prev,
            ...newFilters
        }));
        setPagination(prev => ({
            ...prev,
            page: 1
        }));
    };

    const handleSourceChange = (newSourceValue) => {
        setSourceHSE(newSourceValue)
        setPagination(prev => ({ ...prev, page: 1 }));
    }

    const handlePageChange = (newPage) => {
        setPagination(prev => ({ ...prev, page: newPage }));
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    if (loading) {
        return (
            <div className="program-container">
                <div className="loading-container">
                    <div className="loading-spinner"></div>
                    <p>Загрузка программ...</p>
                </div>
            </div>
        );
    }

    if (error && programs.length === 0) {
        return (
            <div className="program-container">
                <div className="error-container">
                    <div className="error-icon">❌</div>
                    <h3>Ошибка загрузки</h3>
                    <button onClick={fetchPrograms} className="retry-btn">
                        Повторить
                    </button>
                </div>
            </div>
        );
    }

return (
    <div className="programs-page">
        <FilterBar
        onSearch={handleSearch}
        onSourceChange={handleSourceChange}
                    onFilterChange={handleFilterChange}
                    filters={filters}
        source={sourceHSE}></FilterBar>
        <ProgramList
        programs={programs}
        loading={loading}
        error={error}
        >
        </ProgramList>
        {pagination.pages > 1 && (
            <div className="pagination">
                <button
                    onClick={() => setPagination(prev => ({ ...prev, page: prev.page - 1 }))}
                    disabled={pagination.page === 1}
                    className="pagination-btn"
                >
                    ⬅️ Предыдущая
                </button>
                <span className="page-info">
                    Страница {pagination.page} из {pagination.pages}
                </span>
                <button
                    onClick={() => setPagination(prev => ({ ...prev, page: prev.page + 1 }))}
                    disabled={pagination.page === pagination.pages}
                    className="pagination-btn"
                >
                    Следующая ➡️
                </button>
            </div>
        )}
    </div>
);
}

export default ProgramsPage;
