import './styles/FormatMenu.css';

const FormatMenu = ({ onSave }) => {
  return (
    <div className="format-menu">
      <button onClick={() => onSave('json')}>
        <span className="format-icon">📄</span> JSON
      </button>
      <button onClick={() => onSave('csv')}>
        <span className="format-icon">📊</span> CSV
      </button>
      <button onClick={() => onSave('xlsx')}>
        <span className="format-icon">📑</span> XLSX
      </button>
      <button onClick={() => onSave('pdf')}>
        <span className="format-icon">📕</span> PDF
      </button>
    </div>
  );
};

export default FormatMenu;
