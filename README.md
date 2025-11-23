🌿 CropEye: Predictive GIS Dashboard for Precision Agriculture Recruiter Summary: A predictive GIS dashboard for precision agriculture. It monitors Land Health (NDVI), Pest Risk, and Weather using advanced geospatial analysis. The project validates a scalable, production-ready architecture by demonstrating real-time data ingestion and processing capabilities with open satellite and synthetic sensor data.

🚀 Project Overview CropEye is a full-stack, data-driven Geographic Information System (GIS) platform built to empower farmers with the predictive intelligence needed to optimize land health, manage risks, and maximize yield. It serves as a comprehensive visual interface that transforms complex geospatial and environmental time-series data into actionable, map-based insights for precision farming decisions.

✨ Key Features

CropEye provides a centralized, interactive map interface with real-time analytics across several critical domains:
Land Health Monitoring (NDVI/EVI): Visualize current and historical Vegetative Index (NDVI/EVI) data derived from open-access satellite imagery (e.g., Copernicus Sentinel). This allows for rapid identification of crop stress, nutrient deficiencies, and irrigation inconsistencies across the acreage.
Predictive Pest & Disease Risk Mapping: Integrates external models and simulated data to calculate and display hyper-local risk indices for common pests and diseases, based on environmental factors like temperature and humidity.
Hyper-Local Weather Forecasting: Delivers high-resolution, short-term weather forecasts directly layered onto the farm map, enabling timely scheduling of resource-intensive activities like spraying or harvesting.
Field-Level Data Aggregation: Allows users to define specific field boundaries to generate aggregated statistics and historical charts for soil, health, and weather metrics.

🛠️ Technical Strategy: Scalability & Real-Time Simulation

This project is architected to be production-ready and showcases critical skills in data ingestion, time-series analysis, and scalable dashboard design—all essential for enterprise GIS roles.
Recruiter Note: Real-time data input is successfully demonstrated using industry-standard simulation and open-access data sources, confirming the system's ability to seamlessly integrate physical hardware (drones, in-field sensors) when available.

## Module API Integrations

CropEye integrates multiple data sources through specialized modules, each leveraging specific APIs for accurate agricultural intelligence:

### 🌾 NDVI Module (Port 5001)

- **Purpose**: Monitors vegetation health and crop stress through satellite imagery analysis
- **Copernicus Integration**: Uses Sentinel-2 satellite data via Copernicus Data Space Ecosystem for multispectral imagery processing
  - **API Used**: Copernicus Data Space Ecosystem API (https://dataspace.copernicus.eu/)
  - **Data Type**: Sentinel-2 Level-2A multispectral imagery
  - **Authentication**: OAuth2 with client credentials (COPERNICUS_CLIENT_ID, COPERNICUS_CLIENT_SECRET)
  - **Parameters**: NIR (Band 8), Red (Band 4) for NDVI calculation
- **Data Sources**: Real-time satellite NDVI calculations with historical trend analysis
- **API Endpoint**: `/api/ndvi/analyze` (POST with lat/lng coordinates)
- **Key Features**: Vegetation coverage assessment, health status classification, temporal trend monitoring

### 🌱 Soil Module (Port 5002)

- **Purpose**: Analyzes soil composition, nutrient levels, and fertility parameters
- **Copernicus Integration**: Leverages SoilGrids API for global soil property maps
  - **API Used**: ISRIC SoilGrids REST API (https://soilgrids.org/)
  - **Data Type**: Global soil property predictions at 250m resolution
  - **Parameters**: pH, organic carbon, nitrogen, phosphorus, potassium, texture
- **NDVI Integration**: Correlates soil properties with vegetation health data from NDVI module
- **Data Sources**: pH, NPK levels, texture analysis, organic matter content
- **API Endpoint**: `/api/soil/analyze` (POST with coordinates and NDVI correlation)
- **Key Features**: Nutrient deficiency detection, soil type classification, fertility recommendations

### 🌤️ Weather Module (Port 5003)

- **Purpose**: Provides hyper-local weather forecasting and agricultural indices
- **OpenWeatherMap Integration**: Real-time weather data and 7-day forecasts
  - **API Used**: OpenWeatherMap One Call API 3.0 (https://openweathermap.org/api/one-call-3)
  - **Data Type**: Current weather, hourly forecasts, daily forecasts
  - **Authentication**: API key (OPENWEATHER_API_KEY)
  - **Parameters**: Temperature, humidity, precipitation, wind speed, solar radiation
- **Open-Meteo Integration**: Additional weather parameters and historical data
  - **API Used**: Open-Meteo API (https://open-meteo.com/)
  - **Data Type**: Historical weather data and additional meteorological parameters
  - **Parameters**: Additional climate variables, historical trends
- **Copernicus Integration**: ERA5 reanalysis data for long-term climate patterns
  - **API Used**: Copernicus Climate Data Store (CDS) API
  - **Data Type**: ERA5-Land reanalysis dataset
  - **Parameters**: Long-term temperature, precipitation, soil moisture patterns
- **API Endpoints**:
  - `/api/weather/current` (GET with lat/lng)
  - `/api/weather/agricultural` (GET with lat/lng for farming-specific indices)
- **Key Features**: GDD calculation, frost risk assessment, heat stress monitoring

### 🌾 Crop Recommendation Module (Port 5004)

- **Purpose**: Suggests optimal crops based on environmental conditions
- **Data Integration**: Combines soil (Port 5002), weather (Port 5003), and NDVI (Port 5001) data for recommendations
  - **Soil Data**: pH, nutrient levels from SoilGrids via Copernicus
  - **Weather Data**: Temperature, rainfall from OpenWeatherMap/Open-Meteo
  - **NDVI Data**: Vegetation health from Sentinel-2 via Copernicus
- **API Endpoint**: `/api/crop/recommend` (POST with environmental parameters)
- **Key Features**: Multi-factor scoring (pH, rainfall, temperature, NDVI), yield prediction

### 💧 Water Management Module (Port 5005)

- **Purpose**: Calculates irrigation requirements and water stress indices
- **Data Integration**: Uses weather (Port 5003) and soil (Port 5002) data for ET calculations
  - **Weather Data**: Temperature, humidity, wind speed from OpenWeatherMap
  - **Soil Data**: Texture, moisture retention from SoilGrids
- **API Endpoint**: `/api/water/calculate` (POST with weather_data, soil_data, crop_type, and growth_stage parameters)
- **Key Features**: Penman-Monteith ET0 calculation, irrigation scheduling, water stress monitoring

### 🐛 Pest & Disease Module (Port 5006)

- **Purpose**: Assesses pest and disease risks based on environmental conditions
- **Weather Integration**: Temperature and humidity-driven risk modeling from Weather module (Port 5003)
  - **Weather Data**: Real-time temperature, humidity from OpenWeatherMap
- **API Endpoint**: `/api/pests/assess` (POST with temperature, humidity, and crop_type parameters)
- **Key Features**: Pest risk scoring, disease prediction, integrated pest management recommendations

Strategy Component Demonstration

Key Skill Highlighted
Satellite Data Proxy
Dynamic processing of newly released Sentinel-2 or MODIS scenes to simulate live drone flyover imagery (e.g., "just-in-time" NDVI layers).
Geospatial Image Processing (GDAL, Raster Analysis)
Synthetic Sensor Streams
Code-based simulators generate realistic, time-stamped JSON data streams (e.g., soil moisture, temperature) to mimic an active IoT network.
Time-Series Data Management, Backend API Design
Third-Party API Integration
Continuous polling of services like OpenWeatherMap to provide dynamic, updating forecast data directly to the map interface.
External API Integration, System Reliability
⚙️ Technology Stack Frontend/Mapping: [Specify your choice: React/Angular/HTML, Mapbox GL JS/Leaflet]

Data Processing (Backend/Analysis): [Specify your choice: Python (GDAL, NumPy) / Node.js]

Data Storage: Firestore (for historical time-series logs and user configurations)

Styling: Tailwind CSS (for modern, responsive UI design)

Visualization: [Specify your choice: D3.js / Chart.js / Recharts]
