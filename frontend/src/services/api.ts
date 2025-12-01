// src/services/api.ts

import { apiClient } from "./apiClient";
import type {
  NDVIResponse,
  SoilResponse,
  WeatherResponse,
  WaterResponse,
  CropResponse,
  PestResponse,
} from "../types";

export const API_BASE = {
  ndvi: import.meta.env.VITE_NDVI_API_URL || "/api/ndvi",
  soil: import.meta.env.VITE_SOIL_API_URL || "/api/soil",
  weather: import.meta.env.VITE_WEATHER_API_URL || "/api/weather",
  // backend uses singular 'crop' namespace
  crops: import.meta.env.VITE_CROPS_API_URL || "/api/crop",
  water: import.meta.env.VITE_WATER_API_URL || "/api/water",
  // backend uses singular 'pest' namespace
  pests: import.meta.env.VITE_PESTS_API_URL || "/api/pest",
};

export const api = {
  ndvi: {
    analyze: (lat: number, lng: number) =>
      apiClient<NDVIResponse>(`${API_BASE.ndvi}/analyze`, {
        method: "POST",
        body: JSON.stringify({ latitude: lat, longitude: lng }),
      }),
  },

  soil: {
    analyze: (lat: number, lng: number, includeNDVI = true) =>
      apiClient<SoilResponse>(`${API_BASE.soil}/analyze`, {
        method: "POST",
        body: JSON.stringify({
          latitude: lat,
          longitude: lng,
          coordinate_source: "user",
          include_ndvi: includeNDVI,
        }),
      }),
  },

  weather: {
    current: (lat: number, lng: number) =>
      apiClient<WeatherResponse>(
        `${API_BASE.weather}/current?lat=${lat}&lng=${lng}`
      ),

    agricultural: (lat: number, lng: number) =>
      apiClient<WeatherResponse>(
        `${API_BASE.weather}/agricultural?lat=${lat}&lng=${lng}`
      ),
  },

  water: {
    calculate: (data: {
      weather_data: { temp: number; humidity: number };
      soil_data: { texture: string };
      crop_type: string;
      growth_stage: string;
    }) =>
      apiClient<WaterResponse>(`${API_BASE.water}/irrigation/calculate`, {
        method: "POST",
        body: JSON.stringify(data),
      }),
  },

  crops: {
    // Integrated: ask backend to fetch soil/weather/ndvi and compute recommendations
    recommendIntegrated: (lat: number, lng: number) =>
      apiClient<CropResponse>(`${API_BASE.crops}/recommend/integrated`, {
        method: "POST",
        body: JSON.stringify({ latitude: lat, longitude: lng }),
      }),

    // Legacy/simple: supply all parameters from client (keeps compatibility)
    recommend: (data: {
      latitude: number;
      longitude: number;
      ph: number;
      rainfall: number;
      temp_mean: number;
      ndvi: number;
    }) =>
      apiClient<CropResponse>(`${API_BASE.crops}/recommend`, {
        method: "POST",
        body: JSON.stringify(data),
      }),
  },

  pests: {
    assess: (data: {
      temp: number;
      humidity: number;
      crop_type: string;
      additional_factors?: Record<string, unknown>;
    }) =>
      apiClient<PestResponse>(`${API_BASE.pests}/threats/comprehensive`, {
        method: "POST",
        body: JSON.stringify(data),
      }),
  },
};

export default api;
