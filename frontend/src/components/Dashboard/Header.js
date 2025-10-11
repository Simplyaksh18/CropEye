import React from "react";
import { useAuth } from "../../context/AuthContext";
import { LogOut, User } from "lucide-react";
import "./Header.css";

const Header = () => {
  const { user, logout } = useAuth();

  const handleLogout = async () => {
    await logout();
  };

  return (
    <header className="header">
      <div className="header-content">
        <div className="header-brand">
          <h1>CropEye</h1>
          <p>Location-based GIS Analysis for Smart Agriculture</p>
        </div>

        <div className="header-user">
          <div className="user-info">
            <User className="user-icon" />
            <span className="user-name">
              {user?.firstName} {user?.lastName}
            </span>
          </div>
          <button className="logout-button" onClick={handleLogout}>
            <LogOut className="logout-icon" />
            Logout
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;
