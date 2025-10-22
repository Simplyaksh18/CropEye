// src/types/analysis.types.ts
// Type definitions matching your backend API responses

export interface LocationData {
  latitude: number;
  longitude: number;
  address?: string;
}

export interface NDVIData {
  mean: number;
  median: number;
  std_dev: number;
  min: number;
  max: number;
}

export interface NDVIReport {
  latestValue: number;
  latestDate: string;
  status:
    | "Healthy"
    | "Moderate"
    | "Poor"
    | "Critical"
    | "Excellent"
    | "Good"
    | "Fair";
  trend: string;
  change: number | null;
  seasonalAverage: number;
  history: Array<{
    date: string;
    value: number;
  }>;
}

export interface HealthAnalysis {
  status: string;
  description?: string;
}

export interface TrendAnalysis {
  trend: string;
  summary: string;
}

export interface WeatherDay {
  date: string;
  temperature: {
    min: number;
    max: number;
    avg: number;
  };
  precipitation: number;
  humidity: number;
  wind: {
    avg_speed: number;
    gust_max: number;
  };
  outlook: string;
}

export interface WeatherForecast {
  days: WeatherDay[];
  summary: string;
}

export interface CropRecommendation {
  crop: string;
  suitabilityScore: number;
  reason: string;
  expectedHarvestSuccessRate: string;
  recommendedPractices: string[];
}

export interface SoilFertility {
  nitrogen_level?: number;
  phosphorus_level?: number;
  potassium_level?: number;
  ph_level?: number;
  moisture_level?: number;
  organic_matter?: number;
  quality_assessment?: string;
}

export interface PestAlert {
  pest_name: string;
  risk_level: "Low" | "Medium" | "High" | "Critical";
  description: string;
  prevention_measures: string[];
}

export interface ReferenceFarm {
  id: string;
  name: string;
  location: {
    latitude: number;
    longitude: number;
  };
  distance_km?: number;
}

// Main analysis data structure from backend
export interface AnalysisData {
  // NDVI data
  ndvi?: NDVIData;
  ndvi_report?: NDVIReport;
  ndvi_history?: Array<{ date: string; value: number }>;
  ndvi_analysis?: {
    vegetation_percentage: number;
    status: string;
    value: number;
  };

  // Health & Trend
  health_analysis?: HealthAnalysis;
  trend_analysis?: TrendAnalysis;
  vegetation_coverage?: number;
  vegetation_percentage?: number;

  // Weather
  weather_forecast?: WeatherForecast;

  // Crops
  crop_recommendations?: CropRecommendation[];

  // Soil
  soil_fertility?: SoilFertility;

  // Pests
  pest_alerts?: PestAlert[];

  // Reference farms
  reference_farms?: ReferenceFarm[];

  // Metadata
  analysis_date?: string;
  analysis_timestamp?: string;
  location?: LocationData;
}

// For form inputs
export interface LoginFormData {
  email: string;
  password: string;
}

export interface RegisterFormData {
  email: string;
  password: string;
  confirmPassword: string;
  firstName: string;
  lastName: string;
  farmName?: string;
  location?: string;
}

// API Response types
export interface APIResponse<T = unknown> {
  success: boolean;
  data?: T;
  message?: string;
  error?: string;
}

export interface AuthResponse {
  token: string;
  user?: {
    id: string;
    email: string;
    firstName: string;
    lastName: string;
    farmName?: string;
  };
}
