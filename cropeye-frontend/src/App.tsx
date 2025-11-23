// src/App.tsx

import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import { useAuth } from "./hooks/useAuth";
import { LocationProvider } from "./context/LocationContext";
import LoginPage from "./pages/LoginPage";
import DashboardPage from "./pages/DashboardPage";
import { NDVIPage } from "./pages/NDVIPage";
import { WeatherPage } from "./pages/WeatherPage";
import { WaterPage } from "./pages/WaterPage";
import { SoilPage } from "./pages/SoilPage";
import { CropsPage } from "./pages/CropsPage";
import { PestsPage } from "./pages/PestsPage";
import Footer from "./components/Footer";

const AppContent: React.FC = () => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-50">
        <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-green-600"></div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <LoginPage onLoginSuccess={() => {}} />;
  }

  return (
    <Router>
      <div className="min-h-screen flex flex-col">
        <div className="flex-1">
          <Routes>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/crops" element={<CropsPage />} />
            <Route path="/ndvi" element={<NDVIPage />} />
            <Route path="/pests" element={<PestsPage />} />
            <Route path="/soil" element={<SoilPage />} />
            <Route path="/water" element={<WaterPage />} />
            <Route path="/weather" element={<WeatherPage />} />
          </Routes>
        </div>
      </div>
      <Footer />
    </Router>
  );
};

const App: React.FC = () => {
  return (
    <AuthProvider>
      <LocationProvider>
        <AppContent />
      </LocationProvider>
    </AuthProvider>
  );
};

export default App;
