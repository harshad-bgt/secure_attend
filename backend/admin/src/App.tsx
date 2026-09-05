import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import DashboardLayout from './components/layout/DashboardLayout';
import Dashboard from './pages/Dashboard';
import Login from './pages/Login';
import StudentsList from './pages/students/StudentsList';
import StudentDetails from './pages/students/StudentDetails';
import FacultyList from './pages/faculty/FacultyList';
import FacultyDetails from './pages/faculty/FacultyDetails';
import AcademicOverview from './pages/academic/AcademicOverview';
import AttendanceSessions from './pages/attendance/AttendanceSessions';

import { ThemeProvider } from './components/ThemeProvider';
import { AuthProvider, useAuth } from './contexts/AuthContext';

const queryClient = new QueryClient();

const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  const { isAuthenticated, isLoading } = useAuth();
  
  if (isLoading) return <div className="flex h-screen items-center justify-center dark:bg-slate-900 dark:text-white">Loading...</div>;
  if (!isAuthenticated) return <Navigate to="/login" replace />;
  
  return <>{children}</>;
};

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <ThemeProvider defaultTheme="light" storageKey="vite-ui-theme">
          <Router>
            <Routes>
            <Route path="/login" element={<Login />} />
          
          <Route path="/" element={<ProtectedRoute><DashboardLayout /></ProtectedRoute>}>
            <Route index element={<Navigate to="/dashboard" replace />} />
            <Route path="dashboard" element={<Dashboard />} />
            
            <Route path="students" element={<StudentsList />} />
            <Route path="students/:id" element={<StudentDetails />} />
            
            <Route path="faculty" element={<FacultyList />} />
            <Route path="faculty/:id" element={<FacultyDetails />} />
            
            <Route path="academic" element={<AcademicOverview />} />
            
            <Route path="attendance" element={<AttendanceSessions />} />
          </Route>
          
          <Route path="*" element={<div className="flex h-screen items-center justify-center dark:bg-slate-900 dark:text-white">404 - Not Found</div>} />
        </Routes>
      </Router>
      </ThemeProvider>
      </AuthProvider>
    </QueryClientProvider>
  );
}

export default App;
