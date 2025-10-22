// src/context/location-context.ts
import { createContext } from "react";

export interface ReferenceFarm {
  id: string;
  name?: string;
  lat?: number;
  lng?: number;
}

export type NDVIReport = {
  latestValue?: number | null;
  latestDate?: string | null;
  status?: string | null;
  trend?: unknown;
  change?: number | null;
  seasonalAverage?: number | null;
  history?: unknown[];
};

export interface LocationData {
  lat: number;
  lng: number;
  address?: string | null;
  timestamp: string;
}

import type { AnalysisData } from "../types/analysis.types";

export interface LocationContextType {
  userLocation: LocationData | null;
  analysisData: AnalysisData | null;
  loading: boolean;
  error: string | null;
  locationPermission: PermissionState | null;
  referenceFarms: ReferenceFarm[];
  updateLocation: (lat: number, lng: number, address?: string) => Promise<void>;
  analyzeLocation: (lat: number, lng: number) => Promise<void>;
  requestLocationPermission: () => Promise<void>;
  retryLocationRequest: () => void;
  clearError: () => void;
  updateAnalysis: (data: AnalysisData) => void;
}

export const LocationContext = createContext<LocationContextType | undefined>(
  undefined
);

export default LocationContext;
