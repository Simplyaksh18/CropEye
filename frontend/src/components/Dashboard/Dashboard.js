import React from "react";
import { useAuth } from "../../context/AuthContext";
import Header from "./Header";
import LocationInput from "../LocationInput/LocationInput";
import AnalysisDashboard from "./AnalysisDashboard";
import "./Dashboard.css";

const Dashboard = () => {
  const { user } = useAuth();

  return (
    <div className="dashboard">
      <Header />
      <main className="dashboard-content">
        <div className="dashboard-welcome">
          <h1>Welcome back, {user?.firstName || "User"}!</h1>
          <p>Monitor your crops with real-time satellite and weather data</p>
        </div>
        <LocationInput />
        <AnalysisDashboard />
      </main>
    </div>
  );
};

export default Dashboard;
