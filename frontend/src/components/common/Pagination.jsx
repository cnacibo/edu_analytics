import "./styles/Pagination.css";
const Pagination = ({currentPage, totalPages, onPageChange}) => {
    if (totalPages <= 1) return null;
    return (
        <div className="pagination">
                <button
                    onClick={() => onPageChange(currentPage - 1)}
                    disabled={currentPage === 1}
                    className="pagination-btn"
                >
                    ⬅️ Предыдущая
                </button>
                <span className="page-info">
                    Страница {currentPage} из {totalPages}
                </span>
                <button
                    onClick={() => onPageChange(currentPage + 1)}
                    disabled={currentPage === totalPages}
                    className="pagination-btn"
                >
                    Следующая ➡️
                </button>
            </div>
    )
}

export default Pagination
