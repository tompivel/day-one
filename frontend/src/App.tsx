import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { useAuthStore } from './store/useAuthStore';
import Home from './pages/Home';
import Dashboard from './pages/Dashboard';
import PlanDetail from './pages/PlanDetail';
import MacrocycleDetail from './pages/MacrocycleDetail';
import MicrocycleDetail from './pages/MicrocycleDetail';

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#90caf9',
    },
    secondary: {
      main: '#f48fb1',
    },
  },
});

// Protected Route Wrapper
const ProtectedRoute = ({ children }: { children: React.ReactElement }) => {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  if (!isAuthenticated) {
    return <Navigate to="/" replace />;
  }
  return children;
};

const App: React.FC = () => {
  return (
    <ThemeProvider theme={darkTheme}>
      <CssBaseline />
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="/plans/:planId"
            element={
              <ProtectedRoute>
                <PlanDetail />
              </ProtectedRoute>
            }
          />
          <Route
            path="/macrocycles/:macrocycleId"
            element={
              <ProtectedRoute>
                <MacrocycleDetail />
              </ProtectedRoute>
            }
          />
          <Route
            path="/microcycles/:microcycleId"
            element={
              <ProtectedRoute>
                <MicrocycleDetail />
              </ProtectedRoute>
            }
          />
        </Routes>
      </Router>
    </ThemeProvider>
  );
};

export default App;
