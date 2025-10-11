# CropEye - Location-Based GIS Analysis Platform

**Complete location-based agricultural GIS system with React frontend and Flask backend**

## 🚀 Quick Setup

### 1. Backend Setup

```bash
cd backend
pip install -r requirements.txt
python run_server.py
# Runs on http://localhost:5000
```

### 2. Frontend Setup

```bash
cd frontend
npm install
npm start
# Runs on http://localhost:3000
```

### 3. Production Build (optional)

```bash
cd frontend
npm run build
```

### 4. Diagnostics & Tests

```bash
cd backend
python test_login.py
```

> 💡 Need a different API location? Create a `.env` file in `frontend/` with
> `REACT_APP_API_BASE=https://your-api-host/api` and restart the dev server.
>
> 🔐 The AgroMonitoring key (`AGRO_API_KEY`) defaults to `041eafb782c11c245450c23d485e8f9a`. Override it in
> `backend/.env` when rotating credentials.

## 🌟 Features

- **Multi-page agronomy console** – Overview, Weather, NDVI, Crops, Pest Watch and Insights linked via a nav bar with smooth motion transitions.
- **AgroMonitoring integration** – Polygon NDVI history, 7-day forecast and vegetation summaries powered directly by the official API.
- **Reference farm library** – Instantly test accuracy using curated Indian research farms or drop in manual GPS coordinates.
- **Narrative recommendations** – Crop suggestions detail the agronomic rationale, expected success rates and field practices.
- **Immersive UI** – Aurora background, gallery imagery and a persistent light/dark theme toggle per user session.

## 🔨 Implementation Tasks

Replace placeholder methods in `backend/src/gis_processing/location_analyzer.py`:

- `_download_satellite_data()` - Copernicus API integration
- `_calculate_ndvi()` - NDVI from satellite bands
- `_estimate_soil_moisture()` - Spectral moisture indices

## 📍 Reference Farms (preloaded)

| Farm                                         | Latitude | Longitude | Focus                        |
| -------------------------------------------- | -------- | --------- | ---------------------------- |
| Punjab Agricultural University Research Farm | 30.9010  | 75.8573   | Wheat · Maize · Cotton       |
| Kerala Rice Research Station                 | 12.1848  | 75.1588   | Rice · Cassava · Coconut     |
| IARI Regional Station Karnal                 | 29.6857  | 76.9905   | Wheat · Mustard · Vegetables |
| ANGRAU RARS Lam Farm                         | 16.5167  | 80.6167   | Paddy · Maize · Pulses       |

Select any farm from the sidebar library to benchmark analysis accuracy, or plug in your own lat/long.

Ready for hands-on GIS implementation!
