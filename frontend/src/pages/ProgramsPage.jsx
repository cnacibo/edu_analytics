import ProgramList from './../components/programs/ProgramList';
import FilterBar from "../components/programs/FilterBar";
import {hseApi, vuzopediaApi} from "../api";
import {useEffect, useState} from "react";
const ProgramsPage = () => {
    const [programs, setPrograms] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [pagination, setPagination] = useState({
        page: 1,
        size: 2,
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
    }, ['vuzopedia', pagination.page, filters]);

    const fetchPrograms = async () => {
        setLoading(true);
        setError(null);
        try {
            const params = {
                page: pagination.page,
                size: pagination.size,
            };
            Object.keys(params).forEach(key => {
                if (params[key] === '') delete params[key];
            });
            let responseVuzopedia = await vuzopediaApi.getPrograms(params);
            let responseHse = await hseApi.getPrograms(params);
            console.log('Setting programs:', responseVuzopedia);

            let programsData = [
                ...responseHse.programs.map(program => ({
                    ...program,
                    id: `hse-${program.id}`,
                    source: 'hse'
                })),
                ...responseVuzopedia.programs.map(program => ({
                    ...program,
                    id: `vuz-${program.id}`,
                    source: 'vuzopedia'
                }))
            ];

            console.log('Setting programs:', programsData);
            setPrograms(programsData);

            setPagination(prev => ({
                ...prev,
                total: responseVuzopedia.total + responseHse.total || responseVuzopedia.items?.length || 0,
                pages: responseVuzopedia.pages || Math.ceil((responseVuzopedia.total || 0) / prev.size)
            }));

        } catch (error) {
            setError(error.message);
            console.error('Error fetching programs:', error);
            setPrograms(getMockPrograms());
        } finally {
            setLoading(false);
        }
    }

    const getMockPrograms = () => {
        const programNames = [
            'Computer Science',
            'Data Analytics',
            'Software Engineering',
            'Artificial Intelligence',
            'Cybersecurity',
            'Web Development',
            'Machine Learning',
            'Cloud Computing',
            'Mobile Development',
            'Database Management'
        ];
        return Array.from({ length: 20 }, (_, i) => ({
          id: i + 1,
          name: programNames[i] || `Educational Program ${i + 1}`,
          study_type: i % 2 === 0 ? 'Бакалаврская программа' : 'Магистратура',
          code: `${1000 + i}`,
          cost: i * 100000 + i * 30,
        }));
      };

    const handleSearch = (e) => {
        e.preventDefault();
        setFilters(prev => ({ ...prev, q: e.target.search.value }));
        setPagination(prev => ({ ...prev, page: 1 }));
    };

    const handlePageChange = (newPage) => {
        setPagination(prev => ({ ...prev, page: newPage }));
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    if (loading) {
        return (
            <div className="program-list-container">
                <div className="loading-container">
                    <div className="loading-spinner"></div>
                    <p>Загрузка программ...</p>
                </div>
            </div>
        );
    }

    if (error && programs.length === 0) {
        return (
            <div className="program-list-container">
                <div className="error-container">
                    <div className="error-icon">❌</div>
                    <h3>Ошибка загрузки</h3>
                    <p>{error}</p>
                    <button onClick={fetchPrograms} className="retry-btn">
                        Повторить
                    </button>
                </div>
            </div>
        );
    }
return (
    <div className="programs-page">
        <FilterBar></FilterBar>
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
                    ⬅️Предыдущая
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
