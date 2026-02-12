import React, { useState } from 'react';
import './styles/Sidebar.css';

const Sidebar = ({ onItemClick, onToggle }) => {
  const [isOpen, setIsOpen] = useState(false); // change

  const menuItems = [
    { text: 'Dashboard', icon: '📊' },
    { text: 'All Programs', icon: '📚' },
  ];

  const toggleSidebar = () => {
      const newState = !isOpen;
    setIsOpen(newState);
    if (onToggle) {
        onToggle(newState);
    }
  };

  return (
    <div className={`sidebar ${isOpen ? 'open' : 'closed'}`}>
      <button className="toggle-btn" onClick={toggleSidebar}>
        {isOpen ? '◀' : '▶'}
      </button>

      {isOpen && (
        <div className="sidebar-header">
          <h3>Edu Analytics</h3>
        </div>
      )}

      <nav className="sidebar-menu">
        {menuItems.map((item) => (
          <button
            key={item.text}
            className="menu-item"
            onClick={() => onItemClick(item)}
            title={!isOpen ? item.text : ''}
          >
            {isOpen &&
                <>
                <span className="menu-icon">{item.icon}</span>
                <span className="menu-text">{item.text}</span>
                </>
            }
          </button>
        ))}
      </nav>

      {isOpen && (
        <div className="sidebar-footer"></div>
      )}
    </div>
  );
};

export default Sidebar;
