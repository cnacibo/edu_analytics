import './styles/Instructions.css';
import React from 'react';
const Instructions = ({ onToggleInstructions }) => {
  return (
    <div className="modal-overlay" onClick={() => onToggleInstructions(false)}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Как работать с графом знаний?</h2>
          <button className="modal-close" onClick={() => onToggleInstructions(false)}>
            ×
          </button>
        </div>
        <div className="modal-body">
          <ul>
            <li>
              <b>Навигация:</b> чтобы приблизить фрагмент графа - выделите его, чтобы вернуться в
              изначальное положение - дважды нажмите на экран.
            </li>
            <li>
              <b>Фильтр по типу:</b> отметьте нужные типы вершин. Каждый тип выделен цветом.
            </li>
            <li>
              <b>Минимальное количество связей:</b> выберите минимальное количество ребер у вершины,
              чтобы скрыть узлы с малым числом рёбер – останутся только сильно связанные элементы.
            </li>
            <li>
              <b>Подписи:</b> наведите курсор на узел, чтобы увидеть его название (работает при
              любом масштабе).
            </li>
          </ul>
          <p>❗Данный граф построен для двух программ НИУ ВШЭ - ПИ и ПМИ</p>
        </div>
      </div>
    </div>
  );
};

export default Instructions;
