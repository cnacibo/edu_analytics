import React, {useState} from 'react';
import Sidebar from './Sidebar';
import './styles/Sidebar.css';
import Header from "./Header";
import './styles/MainLayout.css';
import DashboardPage from "./../../pages/DashboardPage";
import ProgramsPage from "./../../pages/ProgramsPage";

const MainLayout = () => {
    const [currentPage, setCurrentPage] = useState('All Programs'); // change
    const [isSidebarOpen, setIsSidebarOpen] = useState(false); // change
    const handlePageChange = (item) => {
        setCurrentPage(item.text);
      };

    const handleSidebarToggle = (isOpen) => {
        setIsSidebarOpen(isOpen);
    };

    const renderContent = () => {
        switch (currentPage) {
            case 'Dashboard':
                return <DashboardPage />;
            case 'All Programs':
                return <ProgramsPage />;
            default:
                return <DashboardPage />;

        }
    }

  return (
     <div className="main-layout">
      <Sidebar onItemClick={handlePageChange} onToggle={handleSidebarToggle} />
        <div className="content-area">
               <Header pageTitle={currentPage} />
              <main className={`main-content ${isSidebarOpen ? 'sidebar-open' : 'sidebar-closed'}`}>
                  {renderContent()}
              </main>
        </div>
    </div>
  );
};

export default MainLayout;
