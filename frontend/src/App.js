import React from 'react';
import './App.css';
import MainLayout from './components/layout/MainLayout';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import DashboardPage from './pages/DashboardPage';
import ProgramsPage from './pages/ProgramsPage';
import ProgramDetailsPage from './pages/ProgramDetailsPage';

function App() {
  return (
    <Router>
      <MainLayout>
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/programs/hse/:id" element={<ProgramDetailsPage />} />
          <Route path="/programs/vuz/:id" element={<ProgramDetailsPage />} />
          <Route path="/programs" element={<ProgramsPage />} />
        </Routes>
      </MainLayout>
    </Router>
  );
}

export default App;
