import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import { LocationProvider } from "./context/LocationContext";
import { ThemeProvider } from "./context/ThemeContext";
import ProtectedRoute from "./components/Auth/ProtectedRoute";
import Login from "./components/Auth/Login";
import Register from "./components/Auth/Register";
import MainLayout from "./components/Layout/MainLayout";
import OverviewPage from "./components/Pages/OverviewPage";
import WeatherPage from "./components/Pages/WeatherPage";
import NdviPage from "./components/Pages/NdviPage";
import CropsPage from "./components/Pages/CropsPage";
import PestsPage from "./components/Pages/PestsPage";
import InsightsPage from "./components/Pages/InsightsPage";
import "./App.css";

function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <LocationProvider>
          <Router>
            <div className="App">
              <Routes>
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route
                  path="/dashboard"
                  element={
                    <ProtectedRoute>
                      <MainLayout />
                    </ProtectedRoute>
                  }
                >
                  <Route index element={<Navigate to="overview" replace />} />
                  <Route path="overview" element={<OverviewPage />} />
                  <Route path="weather" element={<WeatherPage />} />
                  <Route path="ndvi" element={<NdviPage />} />
                  <Route path="crops" element={<CropsPage />} />
                  <Route path="pests" element={<PestsPage />} />
                  <Route path="insights" element={<InsightsPage />} />
                </Route>
                <Route
                  path="/"
                  element={<Navigate to="/dashboard" replace />}
                />
              </Routes>
            </div>
          </Router>
        </LocationProvider>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;
