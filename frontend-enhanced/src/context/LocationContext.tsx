// src/contexts/LocationContext.tsx
// Location context compatible with your backend /analyze-location API

import React, { useState, useEffect } from "react";
import type { ReactNode } from "react";
import { useAuth } from "./AuthContext";
import api from "../api/api-client";
import type { AnalysisData } from "../types/analysis.types";
import { LocationContext } from "./location-context";
import type {
  LocationData,
  ReferenceFarm,
  NDVIReport,
} from "./location-context";

interface LocationProviderProps {
  children: ReactNode;
}

export const LocationProvider: React.FC<LocationProviderProps> = ({
  children,
}) => {
  const [userLocation, setUserLocation] = useState<LocationData | null>(null);
  const [analysisData, setAnalysisData] = useState<AnalysisData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [locationPermission, setLocationPermission] =
    useState<PermissionState | null>(null);
  const [referenceFarms, setReferenceFarms] = useState<ReferenceFarm[]>([]);

  const { getAuthHeader, isAuthenticated } = useAuth();

  // Define functions before effects so they can be referenced safely
  const requestLocationPermission = async () => {
    if (!navigator.geolocation) {
      setError("Geolocation is not supported by this browser");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const position = await new Promise<GeolocationPosition>(
        (resolve, reject) => {
          navigator.geolocation.getCurrentPosition(resolve, reject, {
            enableHighAccuracy: true,
            timeout: 10000,
            maximumAge: 300000, // 5 minutes
          });
        }
      );

      const { latitude, longitude } = position.coords;
      await updateLocation(latitude, longitude);
      setLocationPermission("granted");
    } catch (err) {
      const error = err as GeolocationPositionError | undefined;
      let errorMessage = "Unable to get your location";

      if (error) {
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
      }

      setError(errorMessage);
      setLoading(false);
    }
  };

  const fetchReferenceFarms = async () => {
    try {
      const { data } = await api.get("/farms", {
        headers: getAuthHeader(),
      });
      setReferenceFarms(data?.farms || []);
    } catch {
      // Silent failure for optional feature
    }
  };

  // Request GPS permission on app load
  useEffect(() => {
    if (isAuthenticated && !userLocation) {
      requestLocationPermission();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isAuthenticated]);

  // Fetch reference farms
  useEffect(() => {
    if (isAuthenticated) {
      fetchReferenceFarms();
    } else {
      setReferenceFarms([]);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isAuthenticated]);

  const updateLocation = async (
    lat: number,
    lng: number,
    address: string | null = null
  ) => {
    const newLocation: LocationData = {
      lat,
      lng,
      address,
      timestamp: new Date().toISOString(),
    };

    setUserLocation(newLocation);
    setAnalysisData(null);

    // Automatically analyze location
    if (isAuthenticated) {
      await analyzeLocation(lat, lng);
    }
  };

  const analyzeLocation = async (lat: number, lng: number) => {
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
        { headers: getAuthHeader() }
      );

      // Transform backend response to match frontend expectations
      const transformed: Record<string, unknown> = { ...data };

      if (data && data.ndvi) {
        const nd = data.ndvi;
        const analysisDate = data.analysis_date || new Date().toISOString();

        // Build ndvi_report for NdviPage
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

        // Build ndvi_analysis for dashboard
        transformed.ndvi_analysis = {
          vegetation_percentage:
            data.vegetation_coverage ?? data.vegetation_percentage ?? null,
          status:
            data.health_analysis?.status ||
            ((transformed.ndvi_report as NDVIReport | undefined)?.status ??
              null),
          value: nd.mean ?? null,
        };
      }

      setAnalysisData(transformed);

      if (Array.isArray(data?.reference_farms)) {
        setReferenceFarms(data.reference_farms);
      }
    } catch (err) {
      const e = err as {
        response?: { data?: { message?: string } };
        message?: string;
      };
      const apiMessage =
        e.response?.data?.message || e.message || "Analysis failed";
      setError(apiMessage);
    } finally {
      setLoading(false);
    }
  };
  // fetchReferenceFarms is implemented above

  const retryLocationRequest = () => {
    requestLocationPermission();
  };

  const updateAnalysis = (data: AnalysisData) => {
    setAnalysisData(data);
  };

  const clearError = () => {
    setError(null);
  };

  return (
    <LocationContext.Provider
      value={{
        userLocation,
        analysisData,
        loading,
        error,
        locationPermission,
        referenceFarms,
        updateLocation,
        analyzeLocation,
        requestLocationPermission,
        retryLocationRequest,
        clearError,
        updateAnalysis,
      }}
    >
      {children}
    </LocationContext.Provider>
  );
};
