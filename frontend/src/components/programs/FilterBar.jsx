import './styles/FilterBar.css'
import {useState} from "react";
const FilterBar = ({ onFilterChange}) => {
    const [searchQuery, setSearchQuery] = useState('');
    const [selectedFilters, setSelectedFilters] = useState({
        max_cost: 10^8,
        min_score: 0,
    })

    const handleSearch = () => {
        // onFilterChange({ search: searchQuery, ...selectedFilters });
      };

    const handleClear = () => {
        setSearchQuery('');
        setSelectedFilters({
            max_cost: 10^8,
            min_score: 0,
        });
      };

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
                      onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
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
