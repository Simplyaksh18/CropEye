import React, { useState } from "react";
import { useLocation } from "../../context/LocationContext";
import {
  MapPin,
  AlertCircle,
  RefreshCw,
  Compass,
  Navigation,
} from "lucide-react";
import "./LocationInput.css";

function LocationInput() {
  const {
    userLocation,
    loading,
    error,
    locationPermission,
    updateLocation,
    retryLocationRequest,
    clearError,
    referenceFarms,
    analyzeLocation,
  } = useLocation();

  const [manualCoords, setManualCoords] = useState({ lat: "", lng: "" });
  const [showManualInput, setShowManualInput] = useState(false);
  const [selectedFarm, setSelectedFarm] = useState(null);

  const handleManualSubmit = async (e) => {
    e.preventDefault();
    const lat = parseFloat(manualCoords.lat);
    const lng = parseFloat(manualCoords.lng);

    if (isNaN(lat) || isNaN(lng)) {
      alert("Please enter valid coordinates");
      return;
    }

    if (lat < -90 || lat > 90 || lng < -180 || lng > 180) {
      alert(
        "Please enter valid coordinate ranges (lat: -90 to 90, lng: -180 to 180)"
      );
      return;
    }

    await updateLocation(lat, lng, "Manual coordinates");
    setSelectedFarm(null);
    setShowManualInput(false);
    setManualCoords({ lat: "", lng: "" });
  };

  const handleFarmSelection = async (farm) => {
    setSelectedFarm(farm);
    await updateLocation(
      farm.coordinates.lat,
      farm.coordinates.lng,
      `${farm.name}, ${farm.country}`
    );
  };

  const handleReanalyze = async () => {
    if (userLocation) {
      await analyzeLocation(userLocation.lat, userLocation.lng);
    }
  };

  const handleRetry = () => {
    clearError();
    setSelectedFarm(null);
    retryLocationRequest();
  };

  if (userLocation && !loading && !error) {
    return (
      <div className="location-card location-success">
        <div className="location-header">
          <MapPin className="location-icon" />
          <h3>Location Captured</h3>
        </div>
        <p className="location-coords">
          {userLocation.lat.toFixed(4)}, {userLocation.lng.toFixed(4)}
        </p>
        {userLocation.address && (
          <p className="location-address">{userLocation.address}</p>
        )}
        <div className="success-actions">
          <button className="btn-primary" onClick={handleReanalyze}>
            Refresh analysis
          </button>
          <button
            className="btn-secondary"
            onClick={() => setShowManualInput(!showManualInput)}
          >
            Try another field
          </button>
        </div>
        {referenceFarms?.length > 0 && (
          <div className="reference-farms">
            <h4>
              <Compass size={16} /> Field library
            </h4>
            <div className="farm-pills">
              {referenceFarms.map((farm) => (
                <button
                  key={farm.id}
                  className={
                    selectedFarm?.id === farm.id
                      ? "farm-pill active"
                      : "farm-pill"
                  }
                  onClick={() => handleFarmSelection(farm)}
                >
                  {farm.name}
                </button>
              ))}
            </div>
          </div>
        )}
      </div>
    );
  }

  return (
    <div className="location-card">
      <div className="location-header">
        <MapPin className="location-icon" />
        <h3>Locate your farm</h3>
      </div>

      {referenceFarms?.length > 0 && (
        <div className="reference-farms">
          <h4>
            <Navigation size={16} /> Try a real farm (accuracy test)
          </h4>
          <div className="farm-pills">
            {referenceFarms.map((farm) => (
              <button
                key={farm.id}
                className={
                  selectedFarm?.id === farm.id
                    ? "farm-pill active"
                    : "farm-pill"
                }
                onClick={() => handleFarmSelection(farm)}
              >
                {farm.name}
              </button>
            ))}
          </div>
        </div>
      )}

      {loading && (
        <div className="loading-state">
          <RefreshCw className="loading-spinner" />
          <p>Getting your location and analyzing...</p>
        </div>
      )}

      {error && (
        <div className="error-state">
          <AlertCircle className="error-icon" />
          <p className="error-message">{error}</p>
          <div className="error-actions">
            <button className="btn-primary" onClick={handleRetry}>
              Try Again
            </button>
            <button
              className="btn-secondary"
              onClick={() => setShowManualInput(true)}
            >
              Enter Manually
            </button>
          </div>
        </div>
      )}

      {!loading && !error && !userLocation && (
        <div className="initial-state">
          <p>Choose a farm from the library or share your GPS location.</p>
          <button className="btn-primary" onClick={retryLocationRequest}>
            Get My Location
          </button>
          <button
            className="btn-secondary"
            onClick={() => setShowManualInput(true)}
          >
            Enter Coordinates Manually
          </button>
        </div>
      )}

      {showManualInput && (
        <div className="manual-input">
          <h4>Enter Coordinates Manually</h4>
          <form onSubmit={handleManualSubmit}>
            <div className="coord-inputs">
              <div className="input-group">
                <label>Latitude</label>
                <input
                  type="number"
                  step="any"
                  value={manualCoords.lat}
                  onChange={(e) =>
                    setManualCoords({ ...manualCoords, lat: e.target.value })
                  }
                  placeholder="e.g., 40.7128"
                  required
                />
              </div>
              <div className="input-group">
                <label>Longitude</label>
                <input
                  type="number"
                  step="any"
                  value={manualCoords.lng}
                  onChange={(e) =>
                    setManualCoords({ ...manualCoords, lng: e.target.value })
                  }
                  placeholder="e.g., -74.0060"
                  required
                />
              </div>
            </div>
            <div className="manual-actions">
              <button type="submit" className="btn-primary">
                Analyze Location
              </button>
              <button
                type="button"
                className="btn-secondary"
                onClick={() => setShowManualInput(false)}
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}
    </div>
  );
}

export default LocationInput;
