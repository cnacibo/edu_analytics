import React from 'react';
import './styles/Header.css';

const Header = ({ pageTitle = 'Dashboard' }) => {
  return (
    <header className="app-header">
      <div className="header-content">
        <h1 className="page-title">{pageTitle}</h1>
      </div>
    </header>
  );
};

export default Header;
