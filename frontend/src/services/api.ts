// src/services/api.ts

const BASE = {
  crops: "http://localhost:5004",
  ndvi: "http://localhost:5001",
  soil: "http://localhost:5002",
  weather: "http://localhost:5003",
  water: "http://localhost:5005",
  pests: "http://localhost:5006",
};

const req = async (url: string, options?: RequestInit) => {
  const res = await fetch(url, options);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
};

const api = {
  crops: {
    recommend: (lat: number, lng: number) =>
      req(`${BASE.crops}/api/crop/recommend/integrated`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ latitude: lat, longitude: lng }),
      }),
  },

  ndvi: {
    analyze: (lat: number, lng: number) =>
      req(`${BASE.ndvi}/api/ndvi/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ latitude: lat, longitude: lng }),
      }),
  },

  soil: {
    analyze: (
      lat: number,
      lng: number,
      options?: {
        coordinate_source?: string;
        include_ndvi?: boolean;
        analysis_depth?: string;
      }
    ) =>
      req(`${BASE.soil}/api/soil/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          latitude: lat,
          longitude: lng,
          coordinate_source: options?.coordinate_source || "manual",
          include_ndvi: options?.include_ndvi ?? true,
          analysis_depth: options?.analysis_depth || "comprehensive",
        }),
      }),
  },

  weather: {
    current: (lat: number, lng: number) =>
      req(`${BASE.weather}/api/weather/current?lat=${lat}&lng=${lng}`),
  },

  water: {
    calculate: (lat: number, lng: number, crop: string, stage: string) =>
      req(`${BASE.water}/api/water/irrigation/integrated`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          latitude: lat,
          longitude: lng,
          crop_type: crop,
          growth_stage: stage,
        }),
      }),
  },

  pests: {
    assess: (lat: number, lng: number, crop: string) =>
      req(`${BASE.pests}/api/threats/integrated`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          latitude: lat,
          longitude: lng,
          crop_type: crop,
          additional_factors: {},
        }),
      }),
  },
};

export default api;
