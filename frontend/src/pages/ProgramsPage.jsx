import ProgramList from './../components/programs/ProgramList';
import FilterBar from "../components/programs/FilterBar";
import './styles/ProgramsPage.css'
import {hseApi, vuzopediaApi} from "../api";
import {useEffect, useState} from "react";
import Pagination from "../components/common/Pagination";
import LoadingSpinner from "../components/common/LoadingSpinner";
import Error from "../components/common/Error";
import {exportPrograms} from "../utils/export/exportPrograms";
import FormatMenu from "../components/programs/FormatMenu";

const ProgramsPage = () => {
    const [programs, setPrograms] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [sourceHSE, setSourceHSE] = useState(true);
    const [showMenu, setShowMenu] = useState(false);
    const [pagination, setPagination] = useState({
        page: 1,
        size: 10,
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
                exportPrograms(response.programs, sourceHSE ? 'hse' : 'vuz', filters, pagination.total, format)
                setShowMenu(false);

            } catch (error) {
                console.error('Ошибка при сохранении файла:', error);
                alert('Не удалось сохранить файл!');
            }

        }

    }

    const toggleMenu = () => {
        setShowMenu(!showMenu);
    };

    if (loading) {
        return (
            <LoadingSpinner
                input="программ">
            </LoadingSpinner>
        );
    }

    if (error && programs.length === 0) {
        return (
            <Error
            onRetry={fetchPrograms}
            message="Не удалось загрузить программы">
            </Error>
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
        <div className="save-button-container" >
            {programs.length > 0 && (
                <button
                        className="save-button"
                        onClick={toggleMenu}
                        disabled={programs.length === 0}
                    >
                        <span className="save-icon">💾</span>
                        Сохранить в файл
                    </button>
            )}
            {showMenu && (
                        <FormatMenu onSave={handleSaveToFile} />
                    )}
        </div>

        <ProgramList
        programs={programs}
        loading={loading}
        error={error}
        >
        </ProgramList>
        <Pagination
        currentPage={pagination.page}
        totalPages={pagination.pages}
        onPageChange={handlePageChange}>
        </Pagination>
    </div>
);
}

export default ProgramsPage;
