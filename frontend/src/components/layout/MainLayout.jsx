import React, { useEffect, useState } from 'react';
import Sidebar from './Sidebar';
import './styles/Sidebar.css';
import Header from './Header';
import './styles/MainLayout.css';
import { useNavigate, useLocation } from 'react-router-dom';

const MainLayout = ({ children }) => {
  const location = useLocation();
  const pageTitles = {
    '/': 'Dashboard',
    '/programs': 'Programs',
  };
  const [currentPage, setCurrentPage] = useState(pageTitles[location.pathname]);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  const navigate = useNavigate();

  useEffect(() => {
    const path = location.pathname;
    if (pageTitles[path]) {
      setCurrentPage(pageTitles[path]);
    } else if (path.startsWith('/programs/hse') || path.startsWith('/programs/vuz')) {
      setCurrentPage('Program Details');
    }
  }, [location.pathname]);

  const handleSidebarToggle = (isOpen) => {
    setIsSidebarOpen(isOpen);
  };

  const handlePageChange = (item) => {
    setCurrentPage(item.text);
    navigate(item.path);
  };

  return (
    <div className="main-layout">
      <Sidebar onItemClick={handlePageChange} onToggle={handleSidebarToggle} />
      <div className="content-area">
        <Header pageTitle={currentPage} />
        <main className={`main-content ${isSidebarOpen ? 'sidebar-open' : 'sidebar-closed'}`}>
          {children}
        </main>
      </div>
    </div>
  );
};

export default MainLayout;
