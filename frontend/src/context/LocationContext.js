import React, { createContext, useState, useContext, useEffect } from "react";
import { useAuth } from "./AuthContext";
import api from "../api/client";

const LocationContext = createContext();

export const useLocation = () => {
  const context = useContext(LocationContext);
  if (!context) {
    throw new Error("useLocation must be used within a LocationProvider");
  }
  return context;
};

export const LocationProvider = ({ children }) => {
  const [userLocation, setUserLocation] = useState(null);
  const [analysisData, setAnalysisData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [locationPermission, setLocationPermission] = useState(null);
  const [referenceFarms, setReferenceFarms] = useState([]);

  const { getAuthHeader, isAuthenticated } = useAuth();

  // Request GPS permission and get location on app load
  useEffect(() => {
    if (isAuthenticated && !userLocation) {
      requestLocationPermission();
    }
  }, [isAuthenticated]);

  useEffect(() => {
    if (isAuthenticated) {
      fetchReferenceFarms();
    } else {
      setReferenceFarms([]);
    }
  }, [isAuthenticated]);

  const requestLocationPermission = async () => {
    if (!navigator.geolocation) {
      setError("Geolocation is not supported by this browser");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const position = await new Promise((resolve, reject) => {
        navigator.geolocation.getCurrentPosition(resolve, reject, {
          enableHighAccuracy: true,
          timeout: 10000,
          maximumAge: 300000, // 5 minutes
        });
      });

      const { latitude, longitude } = position.coords;
      await updateLocation(latitude, longitude);
      setLocationPermission("granted");
    } catch (error) {
      let errorMessage = "Unable to get your location";

      switch (error.code) {
        case error.PERMISSION_DENIED:
          errorMessage =
            "Location access denied. Please enable location permissions.";
          setLocationPermission("denied");
          break;
        case error.POSITION_UNAVAILABLE:
          errorMessage = "Location information unavailable";
          break;
        case error.TIMEOUT:
          errorMessage = "Location request timed out";
          break;
        default:
          errorMessage = "An unknown error occurred while getting location";
      }

      setError(errorMessage);
      setLoading(false);
    }
  };

  const updateLocation = async (lat, lng, address = null) => {
    const newLocation = {
      lat,
      lng,
      address,
      timestamp: new Date().toISOString(),
    };

    setUserLocation(newLocation);
    setAnalysisData(null);

    // Automatically analyze location after setting it
    if (isAuthenticated) {
      await analyzeLocation(lat, lng);
    }
  };

  const analyzeLocation = async (lat, lng) => {
    if (!isAuthenticated) {
      setError("Please log in to analyze location");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const { data } = await api.post(
        "/analyze-location",
        { lat, lng },
        {
          headers: getAuthHeader(),
        }
      );
      // Normalize NDVI response from backend to match frontend expectations.
      // New backend returns `ndvi` (mean, median, min, max, std) plus
      // `health_analysis`, `vegetation_coverage`, `trend_analysis`.
      // Many frontend components expect `analysisData.ndvi_report` and
      // `analysisData.ndvi_analysis` (legacy shape). Create those fields
      // when `data.ndvi` is present so UI keeps working.
      const transformed = { ...data };

      if (data && data.ndvi) {
        const nd = data.ndvi;
        const analysisDate = data.analysis_date || new Date().toISOString();

        // Build a lightweight ndvi_report used by NdviPage
        transformed.ndvi_report = {
          latestValue: typeof nd.mean === "number" ? nd.mean : null,
          latestDate: analysisDate,
          status:
            data.health_analysis?.status ||
            (nd.mean >= 0.6 ? "Healthy" : nd.mean >= 0.3 ? "Moderate" : "Poor"),
          trend:
            data.trend_analysis?.summary || data.trend_analysis?.trend || null,
          change:
            typeof nd.mean === "number" && typeof nd.median === "number"
              ? Number((nd.mean - nd.median).toFixed(3))
              : null,
          seasonalAverage: nd.mean || null,
          history: Array.isArray(data.ndvi_history) ? data.ndvi_history : [],
        };

        // Build a compact ndvi_analysis used by the dashboard
        transformed.ndvi_analysis = {
          vegetation_percentage:
            data.vegetation_coverage ?? data.vegetation_percentage ?? null,
          status:
            data.health_analysis?.status || transformed.ndvi_report.status,
          value: nd.mean ?? null,
        };
      }

      setAnalysisData(transformed);
      if (Array.isArray(data?.reference_farms)) {
        setReferenceFarms(data.reference_farms);
      }
    } catch (error) {
      const apiMessage =
        error.response?.data?.message || error.message || "Analysis failed";
      setError(apiMessage);
    } finally {
      setLoading(false);
    }
  };

  const fetchReferenceFarms = async () => {
    try {
      const { data } = await api.get("/farms", {
        headers: getAuthHeader(),
      });
      setReferenceFarms(data?.farms || []);
    } catch (error) {
      // Leave silent - optional feature
    }
  };

  const retryLocationRequest = () => {
    requestLocationPermission();
  };

  const updateAnalysis = (data) => {
    setAnalysisData(data);
  };

  return (
    <LocationContext.Provider
      value={{
        userLocation,
        analysisData,
        loading,
        error,
        locationPermission,
        updateLocation,
        updateAnalysis,
        analyzeLocation,
        requestLocationPermission,
        retryLocationRequest,
        referenceFarms,
        refreshReferenceFarms: fetchReferenceFarms,
        setLoadingState: setLoading,
        setErrorState: setError,
        clearError: () => setError(null),
      }}
    >
      {children}
    </LocationContext.Provider>
  );
};
