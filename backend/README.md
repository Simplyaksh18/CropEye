# CropEye Location-Based GIS Backend

**Location-based agricultural analysis API with GIS processing capabilities**

This backend receives user location coordinates from the frontend and performs comprehensive GIS analysis including NDVI calculation, soil moisture estimation, and crop recommendations.

## 🔨 Implementation Status

### ✅ Complete Features

- **REST API Endpoints** - Flask API ready to receive location requests
- **Location Validation** - Coordinate validation and bounding box generation
- **Mock Data Generation** - Realistic test data for frontend development
- **Error Handling** - Comprehensive error handling and logging
- **CORS Support** - Frontend integration ready

### 🔨 Ready for YOUR Implementation

- **Satellite Data Download** - Connect to Copernicus API (placeholders provided)
- **NDVI Calculation** - Process satellite bands with rasterio (structure ready)
- **Soil Moisture Analysis** - Implement spectral indices (framework ready)
- **Crop Recommendations** - Enhance rule-based algorithm (basic version included)

## 🚀 Quick Start

### Setup

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env  # Configure if needed
python app.py
```

The API will be available at: `http://localhost:5000`

### Test the API

```bash
# Check API status
curl http://localhost:5000/

# Test location analysis
curl -X POST http://localhost:5000/api/analyze-location \
  -H "Content-Type: application/json" \
  -d '{"latitude": 30.7333, "longitude": 76.7794}'
```

## 📍 API Endpoints

### `POST /api/analyze-location`

Analyze a specific geographic location

**Request Body:**

```json
{
  "latitude": 30.7333,
  "longitude": 76.7794,
  "bbox": [76.6833, 30.6833, 76.7833, 30.7833],
  "analysis_type": "comprehensive"
}
```

**Response:**

```json
{
  "ndvi_analysis": {
    "avg_ndvi": 0.652,
    "status": "Healthy",
    "vegetation_percentage": 78.3,
    "source": "placeholder_calculation"
  },
  "soil_moisture_analysis": {
    "soil_moisture": 0.347,
    "dry_percentage": 23.5,
    "wet_percentage": 31.2,
    "unit": "fraction"
  },
  "weather_data": {
    "temperature": 28.4,
    "humidity": 67.2,
    "conditions": "Clear"
  },
  "crop_recommendations": {
    "recommended_crops": ["Rice", "Wheat", "Maize"],
    "confidence": 0.85,
    "soil_type": "Loamy"
  }
}
```

### `GET /api/status`

Get API status and implementation progress

### `GET /health`

Simple health check endpoint

## 🔨 Your GIS Implementation Tasks

### 1. Satellite Data Download (`src/gis_processing/location_analyzer.py`)

```python
def _download_satellite_data(self, bbox: List[float]) -> Optional[Dict]:
    # TODO: Implement Copernicus API integration
    # 1. Register at dataspace.copernicus.eu
    # 2. Search for Sentinel-2 L2A data
    # 3. Download scenes with low cloud cover
    # 4. Return paths to extracted bands
    pass
```

**What you need to do:**

- Sign up for free Copernicus account
- Use `requests` library to query the catalog API
- Download Sentinel-2 L2A scenes covering the bbox
- Extract `.SAFE` directories and return band file paths

### 2. NDVI Calculation (`src/gis_processing/location_analyzer.py`)

```python
def _calculate_ndvi(self, satellite_data: Dict, lat: float, lng: float) -> Dict:
    # TODO: Implement NDVI calculation using rasterio
    # 1. Load B04 (red) and B08 (NIR) bands
    # 2. Apply NDVI formula: (NIR - Red) / (NIR + Red)
    # 3. Crop to area around coordinates
    # 4. Calculate statistics and classification
    pass
```

**What you need to do:**

- Install rasterio: `pip install rasterio`
- Load red (B04) and NIR (B08) bands from Sentinel-2 data
- Apply NDVI formula pixel by pixel
- Calculate mean, min, max, and vegetation percentages
- Classify as poor/moderate/healthy vegetation

### 3. Soil Moisture Estimation (`src/gis_processing/location_analyzer.py`)

```python
def _estimate_soil_moisture(self, satellite_data: Dict, lat: float, lng: float) -> Dict:
    # TODO: Implement spectral moisture indices
    # 1. Load NIR (B08) and SWIR (B11, B12) bands
    # 2. Calculate NDMI: (NIR - SWIR1) / (NIR + SWIR1)
    # 3. Calculate MSI: SWIR1 / NIR
    # 4. Combine indices for moisture estimate
    pass
```

**What you need to do:**

- Load NIR, SWIR1 (B11), and SWIR2 (B12) bands
- Calculate Normalized Difference Moisture Index (NDMI)
- Calculate Moisture Stress Index (MSI)
- Combine indices to estimate soil moisture (0-1 scale)
- Calculate dry/moderate/wet area percentages

### 4. Enhanced Crop Recommendations

```python
def _generate_crop_recommendations(self, ndvi_data, moisture_data, weather_data, lat, lng):
    # TODO: Implement advanced recommendation algorithm
    # Current: Basic rule-based system
    # Enhance with: Regional crop databases, ML models, market data
    pass
```

**Enhancement ideas:**

- Add regional crop suitability databases
- Include seasonal planting calendars
- Consider soil pH and nutrient requirements
- Add market price and demand data
- Implement machine learning models

## 📦 Project Structure

```
backend/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── .env.example                   # Configuration template
├── src/
│   ├── gis_processing/
│   │   ├── location_analyzer.py   # Main GIS processing logic (YOUR IMPLEMENTATION)
│   │   └── mock_data_generator.py # Test data generation
│   └── __init__.py
├── data/                          # Satellite data storage
├── output/                        # Analysis results
└── README.md                      # This file
```

## 🛠️ Required Libraries for GIS Implementation

Add these to `requirements.txt` when you start implementing:

```txt
# GIS processing libraries
rasterio==1.3.8
geopandas==0.14.0
shapely==2.0.1
numpy==1.24.3

# Satellite data access
sentinelsat==1.2.1

# Additional scientific libraries
scipy==1.11.1
scikit-image==0.21.0
```

## 🧪 Testing Your Implementation

### Unit Testing

```bash
# Test location analyzer
python -c "from src.gis_processing.location_analyzer import test_location_analyzer; test_location_analyzer()"

# Test mock data generator
python src/gis_processing/mock_data_generator.py
```

### Integration Testing

```bash
# Start the API server
python app.py

# Test with frontend
# Start React frontend and test location input
```

## 🌍 Example Coordinates for Testing

- **Chandigarh, India**: 30.7333, 76.7794
- **Punjab, India**: 31.1471, 75.3412
- **Iowa, USA**: 41.5868, -93.6250
- **São Paulo, Brazil**: -23.5505, -46.6333

## 📝 Implementation Progress Checklist

- [ ] Set up Copernicus account and credentials
- [ ] Implement satellite data download
- [ ] Install and test rasterio for band processing
- [ ] Implement NDVI calculation from satellite bands
- [ ] Implement soil moisture spectral indices
- [ ] Test with real satellite data
- [ ] Enhance crop recommendation algorithm
- [ ] Add error handling for satellite data processing
- [ ] Optimize performance for larger areas
- [ ] Add caching for repeated requests

## 🚀 Deployment

When you're ready to deploy:

1. **Local Development**: Use the current Flask dev server
2. **Production**: Deploy with Gunicorn + Nginx
3. **Cloud**: Deploy on AWS/GCP/Azure with container support
4. **Environment**: Set production environment variables

## 📚 Resources for Implementation

- **Copernicus Data Access**: https://dataspace.copernicus.eu/
- **Rasterio Documentation**: https://rasterio.readthedocs.io/
- **Sentinel-2 Band Information**: https://sentinels.copernicus.eu/web/sentinel/missions/sentinel-2
- **NDVI Formula**: (NIR - Red) / (NIR + Red)
- **Spectral Indices**: https://www.indexdatabase.de/

---

**Ready to implement real GIS processing! The structure is all set up for your hands-on work.**

## 🔐 Copernicus credentials (important)

This project integrates with the Copernicus (Sentinel) data space for satellite data. For security, do NOT store your Copernicus credentials in source control. Instead, set the following environment variables on your development machine before running downloads or the Flask app:

- `COPERNICUS_USERNAME` — your Copernicus/Dataspace username
- `COPERNICUS_PASSWORD` — your Copernicus/Dataspace password
- `COPERNICUS_CLIENT_ID` — (optional) OAuth client id
- `COPERNICUS_CLIENT_SECRET` — (optional) OAuth client secret

Example (Windows PowerShell):

```powershell
# Temporarily set for current session
$Env:COPERNICUS_USERNAME = 'your_username_here'
$Env:COPERNICUS_PASSWORD = 'your_password_here'
$Env:COPERNICUS_CLIENT_ID = 'your_client_id_here'
$Env:COPERNICUS_CLIENT_SECRET = 'your_client_secret_here'

# Run the backend (in the same PowerShell session)
python app.py
```

### Running behind a proxy or testing with a local product

If your network requires an HTTP(S) proxy, set the standard environment variables before starting the backend (PowerShell example):

```powershell
$Env:HTTP_PROXY = 'http://proxy.example:3128'
$Env:HTTPS_PROXY = 'http://proxy.example:3128'
# then run the backend in the same session
python app.py
```

For offline testing you can provide a local Sentinel `.SAFE` or `.zip` product and skip live downloads. Place the SAFE/ZIP file somewhere in the repo (for example `backend/data/sample_product.zip`) and set:

```powershell
$Env:COPERNICUS_LOCAL_PRODUCT_PATH = 'C:\path\to\backend\data\sample_product.zip'
# then run the backend; NDVI downloader will attempt to extract B04/B08 from the provided archive
python app.py
```

The downloader will prefer a provided `COPERNICUS_LOCAL_PRODUCT_PATH` over live API calls and still return full analysis results that you can use to validate the frontend.

If you prefer a persistent approach for local development, use a `.env` file and a loader such as `python-dotenv` (do not commit `.env` to Git). The repository contains `.env.example` with placeholder names.

If you accidentally committed credentials to source control, remove them immediately and rotate the secrets in the Copernicus account.
