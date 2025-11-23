// API Response Types
export interface CropResponse {
  success: boolean;
  timestamp: string;
  location: {
    latitude: number;
    longitude: number;
  };
  input_parameters: {
    latitude: number;
    longitude: number;
    ph: number;
    rainfall: number;
    temp_mean: number;
    ndvi: number;
  };
  recommendations: Crop[];
  // backward-compat alias used by frontend pages
  crops?: Crop[];
  // optional weights breakdown (may be provided by API)
  weights?: Record<string, number>;
  total_crops_analyzed: number;
}

export interface Crop {
  crop: string;
  score: number;
  components: Record<string, number>;
}

export interface NDVIResponse {
  ndvi_value: number;
  trend: NDVITrend[];
  health_status: string;
  vegetation_coverage: number;
  timestamp: string;
}

export interface NDVITrend {
  date: string;
  value: number;
}

export interface PestResponse {
  success: boolean;
  crop_type: string;
  conditions: {
    temp: number;
    humidity: number;
  };
  pests: Pest[];
  diseases: Disease[];
  total_threats: number;
}

export interface Pest {
  pest: string;
  risk_score: number;
  risk_level: string;
  symptoms: string[];
  control_measures: string[];
}

export interface Disease {
  disease: string;
  risk_score: number;
  risk_level: string;
  symptoms: string[];
  control_measures: string[];
}

export interface SoilResponse {
  ph: number;
  nitrogen: number;
  phosphorus: number;
  potassium: number;
  texture: string;
  recommendations: string[];
  confidence: number;
  data_source: string;
}

export interface WaterResponse {
  success: boolean;
  timestamp: string;
  crop_type: string;
  growth_stage: string;
  schedule: {
    et0_mm_day: number;
    etc_mm_day: number;
    irrigation: {
      gross_irrigation_mm: number;
      net_irrigation_mm: number;
      irrigation_efficiency: number;
    };
    schedule: {
      irrigation_schedule_days: number;
      next_irrigation_date: string;
      water_stress_index: number;
      recommendation: string;
    };
  };
  // convenience top-level aliases that some pages expect
  et0_mm_day?: number;
  etc_mm_day?: number;
  irrigation_requirement_mm?: number;
  irrigation_schedule_days?: number;
  water_stress_index?: number;
  recommendation?: string;
}

export interface WeatherResponse {
  temp: number;
  humidity: number;
  rainfall: number;
  wind_speed: number;
  alerts: WeatherAlert[];
  forecast_7day: ForecastDay[];
  agricultural_context: AgriculturalContext;
}

export interface WeatherAlert {
  type: string;
  message: string;
}

export interface ForecastDay {
  date: string;
  temp_max: number;
  temp_min: number;
  rain: number;
}

export interface AgriculturalContext {
  gdd: number;
  frost_risk: string;
  heat_stress: number;
}

// Location Types
export interface Location {
  lat: number;
  lng: number;
  name?: string;
}

export interface FarmingLand {
  boundaries: Location[];
  area: number; // in hectares
  name?: string;
}

// Auth Types
export interface User {
  id: string;
  email: string;
  name: string;
}

// API Request Types
export interface CropRecommendationRequest {
  latitude: number;
  longitude: number;
  ph: number;
  rainfall: number;
  temp_mean: number;
  ndvi: number;
}

export interface PestAssessmentRequest {
  temp: number;
  humidity: number;
  crop_type: string;
}

export interface WaterCalculationRequest {
  weather_data: {
    temp: number;
    humidity: number;
  };
  soil_data: {
    texture: string;
  };
  crop_type: string;
  growth_stage: string;
}
