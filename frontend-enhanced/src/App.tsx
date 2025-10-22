// src/App.tsx

import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import { LocationProvider } from "./context/LocationContext";
import { ThemeProvider } from "./context/ThemeContext";

// Animations
import { SplashCursor } from "./components/animations/SplashCursor";
import { ParticlesBackground } from "./components/animations/ParticlesBackground";

// Pages
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import DashboardPage from "./pages/DashboardPage";
import OverviewPage from "./pages/OverviewPage";
import NDVIPage from "./pages/NDVIPage";
import WaterManagementPage from "./pages/WaterManagementPage";
import WeatherPage from "./pages/WeatherPage";
import CropsPage from "./pages/CropsPage";
import PestsPage from "./pages/PestsPage";
import SoilPage from "./pages/SoilPage";

// Layout
import MainLayout from "./components/layout/MainLayout";
import ProtectedRoute from "./components/Auth/ProtectedRoute.tsx";

function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <LocationProvider>
          <Router>
            <SplashCursor />

            <Routes>
              {/* Public Routes */}
              <Route path="/login" element={<LoginPage />} />
              <Route path="/register" element={<RegisterPage />} />

              {/* Protected Routes */}
              <Route
                path="/"
                element={
                  <ProtectedRoute>
                    <>
                      <ParticlesBackground
                        count={700}
                        speed={0.2}
                        spread={10}
                        baseSize={100}
                        mouseInteraction={true}
                      />
                      <MainLayout>
                        {/* Outlet will be rendered here */}
                      </MainLayout>
                    </>
                  </ProtectedRoute>
                }
              >
                <Route index element={<DashboardPage />} />
                <Route path="overview" element={<OverviewPage />} />
                <Route path="ndvi" element={<NDVIPage />} />
                <Route path="weather" element={<WeatherPage />} />
                <Route path="water" element={<WaterManagementPage />} />
                <Route path="crops" element={<CropsPage />} />
                <Route path="pests" element={<PestsPage />} />
                <Route path="soil" element={<SoilPage />} />
              </Route>
            </Routes>
          </Router>
        </LocationProvider>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;
