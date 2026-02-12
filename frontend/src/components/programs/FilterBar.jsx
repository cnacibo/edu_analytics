import './styles/FilterBar.css'
import {useEffect, useState} from "react";
const FilterBar = ({ onSearch, onSourceChange, onFilterChange, filters, source }) => {
    const [searchQuery, setSearchQuery] = useState('');
    const [selectedFilters, setSelectedFilters] = useState(filters);
    const [localSource, setLocalSource] = useState(source);

    useEffect(() => {
        setLocalSource(source);
    }, [source]);

    useEffect(() => {
        if (filters) {
            setSelectedFilters({
                max_cost: filters.max_cost || '',
                min_score: filters.min_score || '',
            });
        }
    }, [filters]);

    const handleSearch = () => {
        const allFilters = {
            q: searchQuery,
            max_cost: selectedFilters.max_cost ? Number(selectedFilters.max_cost) : '',
            min_score: selectedFilters.min_score ? Number(selectedFilters.min_score) : '',
        };
        onFilterChange(allFilters);
         onSearch(searchQuery)
      };

    const handleClear = () => {
        setSearchQuery('');
        setSelectedFilters({
            max_cost: '',
            min_score: '',
        });
        onFilterChange({
            q: '',
            max_cost: '',
            min_score: '',
        });
        onSearch('');
      };

    const handleFilterChange = (e) => {
        const { name, value } = e.target;
        setSelectedFilters(prev => ({
            ...prev,
            [name]: value
        }));
    }

    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            handleSearch();
        }
    };
    const changeSource = () => {
        const newValue = !localSource
        setLocalSource(newValue);
        onSourceChange(newValue)
    }

    return (
        <div className="filter-bar">
            <div className="search-section">
                <div className="search-container">
                  <div className="search-input-wrapper">
                    <input
                      type="text"
                      className="search-input"
                      placeholder="Search programs by name..."
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                      onKeyPress={handleKeyPress}
                    />
                    {searchQuery && (
                      <button
                        className="clear-search-btn"
                        onClick={() => setSearchQuery('')}
                        aria-label="Clear search"
                      >
                        ✕
                      </button>
                    )}
                  </div>
                </div>
                <div className="filters">
                    <div className="filters-row">
                        <div className="filter-item">
                            <label htmlFor="max_cost">Макс. стоимость:</label>
                            <input
                                type="number"
                                id="max_cost"
                                name="max_cost"
                                className="filter-input"
                                placeholder="От 0 до 10 млн ₽"
                                value={selectedFilters.max_cost}
                                onChange={handleFilterChange}
                                min="0"
                                step="100000"
                                max="10000000"
                            />
                        </div>
                        <div className="filter-item">
                            <label htmlFor="min_score">Мин. балл:</label>
                            <input
                                type="number"
                                id="min_score"
                                name="min_score"
                                className="filter-input"
                                placeholder="От 0 до 100"
                                value={selectedFilters.min_score}
                                onChange={handleFilterChange}
                                min="0"
                                step="10"
                                max="100"
                            />
                        </div>
                    </div>
                    <div className="choose-source">
                        <button className="source-btn" onClick={changeSource}>
                            {localSource ? 'НИУ ВШЭ' : 'Vuzopedia'}
                        </button>
                    </div>
                </div>
                <div className="search-buttons">
                  <button className="search-btn primary-btn" onClick={handleSearch}>
                    <span className="btn-icon">🔍</span>
                    Search
                  </button>
                  <button className="clear-btn secondary-btn" onClick={handleClear}>
                    <span className="btn-icon">🗑️</span>
                    Clear
                  </button>
                </div>
              </div>

        </div>
    );
}

export default FilterBar;
