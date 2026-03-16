import './styles/FilterBar.css';
const FilterBar = ({ filters, onInputChange, onFilterChange, onSourceChange, source }) => {
  const handleSearch = () => {
    onFilterChange();
  };

  const handleClear = () => {
    const clearedFilters = {
      q: '',
      max_budget_score: '',
      min_score: '',
      study_type: '',
      max_paid_score: '',
    };
    onInputChange(clearedFilters);
    onFilterChange(clearedFilters);
  };

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    onInputChange({
      [name]: value === '' ? '' : value,
    });
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };
  const changeSource = () => {
    const newValue = !source;
    onSourceChange(newValue);
  };

  return (
    <div className="filter-bar">
      <div className="search-row">
        <div className="search-container">
          <div className="search-input-wrapper">
            <input
              type="text"
              className="search-input"
              placeholder="Search programs by name..."
              value={filters.q || ''}
              onChange={(e) => onInputChange({ q: e.target.value })}
              onKeyPress={handleKeyPress}
            />
            {filters.q && (
              <button
                className="clear-search-btn"
                onClick={() => onInputChange({ q: '' })}
                aria-label="Clear search"
              >
                ✕
              </button>
            )}
          </div>
        </div>
        <div className="search-buttons">
          <button className="source-btn" onClick={changeSource}>
            {source ? 'НИУ ВШЭ' : 'Vuzopedia'}
          </button>
          <button className="search-btn" onClick={handleSearch}>
            <span className="btn-icon">🔍</span>
            Search
          </button>
          <button className="clear-btn" onClick={handleClear}>
            <span className="btn-icon">🗑️</span>
            Clear
          </button>
        </div>
      </div>
      <div className="filters-row">
        <div className="filter-item">
          <label htmlFor="max_cost">Макс. стоимость:</label>
          <input
            type="number"
            id="max_cost"
            name="max_cost"
            className="filter-input"
            placeholder="От 0 до 10 млн ₽"
            value={filters.max_cost || ''}
            onChange={handleFilterChange}
            min="0"
            step="100000"
            max="10000000"
          />
        </div>
        {!source && (
          <div className="filter-item">
            <label htmlFor="max_budget_score">Макс. балл на бюджет:</label>
            <input
              type="number"
              id="max_budget_score"
              name="max_budget_score"
              className="filter-input"
              placeholder="От 0 до 500"
              value={filters.max_budget_score || ''}
              onChange={handleFilterChange}
              min="0"
              step="20"
              max="500"
            />
          </div>
        )}
        {!source && (
          <div className="filter-item">
            <label htmlFor="max_paid_score">Макс. балл на платное:</label>
            <input
              type="number"
              id="max_paid_score"
              name="max_paid_score"
              className="filter-input"
              placeholder="От 0 до 500"
              value={filters.max_paid_score || ''}
              onChange={handleFilterChange}
              min="0"
              step="20"
              max="500"
            />
          </div>
        )}
        {source && (
          <div className="filter-item">
            <label htmlFor="study_type">Вид обучения:</label>
            <select
              id="study_type"
              name="study_type"
              className="filter-select"
              value={filters.study_type || ''}
              onChange={handleFilterChange}
            >
              <option value="">Все</option>
              <option value="бакалавр">Бакалавриат</option>
              <option value="магистр">Магистратура</option>
            </select>
          </div>
        )}
      </div>
    </div>
  );
};

export default FilterBar;
