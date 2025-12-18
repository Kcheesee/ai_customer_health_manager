import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import AccountsPage from './pages/Accounts';
import AccountDetail from './pages/AccountDetail';
import SettingsPage from './pages/Settings';
import Dashboard from './pages/Dashboard';
import { MainLayout } from './components/layout/MainLayout';
import ContractsPage from './pages/Contracts';
import InputsPage from './pages/Inputs';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />

        <Route element={<MainLayout />}>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/accounts" element={<AccountsPage />} />
          <Route path="/accounts/:id" element={<AccountDetail />} />
          <Route path="/contracts" element={<ContractsPage />} />
          <Route path="/inputs" element={<InputsPage />} />
          <Route path="/settings" element={<SettingsPage />} />
        </Route>

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
