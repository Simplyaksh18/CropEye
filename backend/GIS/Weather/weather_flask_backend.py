#!/usr/bin/env python3
"""
Weather Analysis Flask Backend
Exposes OpenWeatherMap and Copernicus ERA5 historical weather data via a REST API.

Location: D:\\CropEye1\\backend\\GIS\\Weather\\weather_flask_backend.py

Author: CropEye1 System
Date: October 18, 2025
"""

import os
import logging
from datetime import datetime
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from dotenv import load_dotenv

# Load .env from the root of the 'backend' directory
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
dotenv_path = os.path.join(backend_dir, '.env')
load_dotenv(dotenv_path=dotenv_path)

# Import weather data collector
try:
    from weather_data_collector import WeatherDataCollector
except ImportError:
    logger = logging.getLogger(__name__)
    logger.error("Cannot import WeatherDataCollector")
    WeatherDataCollector = None

# Flask app initialization
app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize weather collector
try:
    weather_collector = WeatherDataCollector() if WeatherDataCollector else None
    logger.info("✅ Weather Data Collector initialized")
except Exception as e:
    logger.error(f"❌ Failed to initialize Weather Data Collector: {e}")
    weather_collector = None


# NOTE: Static route for serving NDVI output images has been removed.
# If you need this during development again, re-enable it or guard it with
# an environment variable such as NDVI_WRITE_IMAGES.


# ============================================================
# HEALTH CHECK ENDPOINT
# ============================================================

@app.route('/api/weather/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    Returns status of weather module and integrations
    """
    try:
        health_status = {
            'status': 'healthy',
            'service': 'Weather Analysis Backend',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0',
            'port': 5003,
            'modules': {
                'weather_collector': 'active' if weather_collector else 'unavailable',
                'openweather_api': 'active' if (weather_collector and getattr(weather_collector, 'openweather_api', None)) else 'unavailable',
                'copernicus_api': 'active' if (
                    weather_collector and
                    getattr(weather_collector, 'copernicus_api', None) and
                    getattr(getattr(weather_collector, 'copernicus_api'), 'is_available', lambda: False)()
                ) else 'fallback'
            },
            'data_sources': {
                'openweathermap': 'real-time forecast',
                'copernicus_era5': 'historical reanalysis',
                'fallback': 'available'
            },
            'features': {
                'current_weather': 'enabled',
                'hourly_forecast': 'enabled (48 hours)',
                'historical_data': 'enabled',
                'agricultural_indices': 'enabled',
                'weather_alerts': 'enabled',
                'soil_integration': 'enabled',
                'ndvi_integration': 'enabled'
            },
            'agricultural_indices': {
                'growing_degree_days': 'enabled',
                'evapotranspiration': 'enabled',
                'frost_risk_assessment': 'enabled',
                'heat_stress_index': 'enabled'
            }
        }
        
        return jsonify(health_status), 200
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500


# ============================================================
# CURRENT WEATHER ENDPOINT
# ============================================================

@app.route('/api/weather/current', methods=['GET'])
def get_current_weather():
    """
    Get current weather conditions
    
    URL: /api/weather/current?lat=<latitude>&lng=<longitude>
    Method: GET
    
    Returns:
        JSON with current weather data and agricultural context
    """
    try:
        lat = request.args.get('lat', type=float)
        lng = request.args.get('lng', type=float)

        if lat is None or lng is None:
            return jsonify({'error': 'lat and lng query parameters are required'}), 400

        if not (-90 <= lat <= 90 and -180 <= lng <= 180):
            return jsonify({'error': 'Invalid coordinate range'}), 400

        if not weather_collector:
            return jsonify({'error': 'Weather collector not initialized'}), 503
        
        logger.info(f"🌤️ Current weather request: ({lat}, {lng})")
        
        # Get current weather
        weather_data = weather_collector.get_current_weather(lat, lng)
        
        if 'error' in weather_data:
            return jsonify(weather_data), 400
        
        logger.info(f"✅ Current weather retrieved for ({lat}, {lng})")
        
        return jsonify(weather_data), 200
        
    except ValueError as e:
        logger.error(f"Invalid coordinates: {e}")
        return jsonify({
            'error': 'Invalid coordinates',
            'details': str(e)
        }), 400
        
    except Exception as e:
        logger.error(f"❌ Current weather error: {e}")
        return jsonify({
            'error': 'Failed to retrieve current weather',
            'details': str(e)
        }), 500


# ============================================================
# HOURLY FORECAST ENDPOINT
# ============================================================

@app.route('/api/weather/hourly', methods=['GET'])
def get_hourly_forecast():
    """
    Get hourly weather forecast (up to 48 hours)
    
    URL: /api/weather/hourly?lat=<latitude>&lng=<longitude>&hours=24
    Method: GET
    
    Returns:
        JSON with hourly forecast data
    """
    try:
        lat = request.args.get('lat', type=float)
        lng = request.args.get('lng', type=float)
        hours = request.args.get('hours', default=48, type=int)

        if lat is None or lng is None:
            return jsonify({'error': 'lat and lng query parameters are required'}), 400
        
        hours = min(hours, 48)  # Max 48 hours

        if not weather_collector:
            return jsonify({'error': 'Weather collector not initialized'}), 503
        
        logger.info(f"🌤️ Hourly forecast request: ({lat}, {lng}), {hours} hours")
        
        # Get forecast
        forecast_data = weather_collector.get_hourly_forecast(lat, lng, hours)
        
        if 'error' in forecast_data:
            return jsonify(forecast_data), 400
        
        logger.info(f"✅ Hourly forecast retrieved for ({lat}, {lng})")
        
        return jsonify(forecast_data), 200
        
    except Exception as e:
        logger.error(f"❌ Hourly forecast error: {e}")
        return jsonify({
            'error': 'Failed to retrieve hourly forecast',
            'details': str(e)
        }), 500


# ============================================================
# HISTORICAL WEATHER ENDPOINT
# ============================================================

@app.route('/api/weather/historical', methods=['POST'])
def get_historical_weather():
    """
    Get historical weather data (Copernicus ERA5)
    
    URL: /api/weather/historical
    Method: POST
    Body: {"latitude": 30.3, "longitude": 76.3, "start_date": "2025-10-01", "end_date": "2025-10-15"}
    
    Returns:
        JSON with historical weather data
    """
    try:
        if not weather_collector:
            return jsonify({'error': 'Weather collector not initialized'}), 503
        
        # Get date parameters
        data = request.get_json(force=True)
        
        required_fields = ['latitude', 'longitude', 'start_date', 'end_date']
        if not data or not all(field in data for field in required_fields):
            return jsonify({
                'error': 'Missing required parameters',
                'required': required_fields,
                'example_body': {"latitude": 30.3, "longitude": 76.3, "start_date": "2025-10-01", "end_date": "2025-10-03"}
            }), 400
        
        start_date = data['start_date']
        end_date = data['end_date']
        
        lat = float(data['latitude'])
        lng = float(data['longitude'])
        
        logger.info(f"🌤️ Historical data request: ({lat}, {lng}), {start_date} to {end_date}")

        # Get historical data
        historical_data = weather_collector.get_historical_weather(lat, lng, start_date, end_date)
        
        if 'error' in historical_data:
            return jsonify(historical_data), 400
        
        logger.info(f"✅ Historical data retrieved for ({lat}, {lng})")
        
        return jsonify(historical_data), 200
        
    except Exception as e:
        logger.error(f"❌ Historical data error: {e}")
        return jsonify({
            'error': 'Failed to retrieve historical weather data',
            'details': str(e)
        }), 500


# ============================================================
# AGRICULTURAL INDICES ENDPOINT
# ============================================================

@app.route('/api/weather/agricultural', methods=['GET'])
def get_agricultural_indices():
    """
    Get agricultural weather indices
    
    URL: /api/weather/agricultural?lat=<latitude>&lng=<longitude>
    Method: GET
    
    Returns:
        JSON with GDD, ET, frost risk, heat stress
    """
    try:
        lat = request.args.get('lat', type=float)
        lng = request.args.get('lng', type=float)

        if lat is None or lng is None:
            return jsonify({'error': 'lat and lng query parameters are required'}), 400

        if not weather_collector:
            return jsonify({'error': 'Weather collector not initialized'}), 503
        
        logger.info(f"🌾 Agricultural indices request: ({lat}, {lng})")
        
        # Get current weather for calculations
        weather_data = weather_collector.get_current_weather(lat, lng)
        if 'error' in weather_data:
            return jsonify(weather_data), 400
        
        # The collector already calculates these in 'agricultural_context'
        agricultural_indices = weather_data.get('agricultural_context', {})
        agricultural_indices['location'] = {'latitude': lat, 'longitude': lng}
        
        logger.info(f"✅ Agricultural indices calculated for ({lat}, {lng})")
        
        return jsonify(agricultural_indices), 200
        
    except Exception as e:
        logger.error(f"❌ Agricultural indices error: {e}")
        return jsonify({
            'error': 'Failed to calculate agricultural indices',
            'details': str(e)
        }), 500


# ============================================================
# WEATHER ALERTS ENDPOINT
# ============================================================

@app.route('/api/weather/alerts', methods=['GET'])
def get_weather_alerts():
    """
    Get weather alerts
    
    URL: /api/weather/alerts?lat=<latitude>&lng=<longitude>
    Method: GET
    
    Returns:
        JSON with active weather alerts
    """
    try:
        lat = request.args.get('lat', type=float)
        lng = request.args.get('lng', type=float)

        if lat is None or lng is None:
            return jsonify({'error': 'lat and lng query parameters are required'}), 400

        if not weather_collector:
            return jsonify({'error': 'Weather collector not initialized'}), 503

        logger.info(f"⚠️ Weather alerts request: ({lat}, {lng})")
        
        # Get current weather
        weather_data = weather_collector.get_current_weather(lat, lng)
        
        # Get forecast
        forecast_data = weather_collector.get_hourly_forecast(lat, lng, 24)
        
        alerts = []
        
        # Check for extreme temperatures
        temp = weather_data['temperature']['current']
        if temp < 0:
            alerts.append({
                'type': 'frost',
                'severity': 'high',
                'message': f'Freezing temperature: {temp}°C',
                'recommendation': 'Protect sensitive crops immediately',
                'timestamp': datetime.now().isoformat()
            })
        elif temp > 40:
            alerts.append({
                'type': 'extreme_heat',
                'severity': 'high',
                'message': f'Extreme heat: {temp}°C',
                'recommendation': 'Ensure adequate irrigation and livestock protection',
                'timestamp': datetime.now().isoformat()
            })
        
        # Check agricultural context for frost risk
        if 'agricultural_context' in weather_data:
            frost_risk = weather_data['agricultural_context'].get('frost_risk', {})
            if frost_risk.get('risk_level') in ['high', 'medium-high']:
                alerts.append({
                    'type': 'frost_warning',
                    'severity': 'medium',
                    'message': f'Frost risk: {frost_risk.get("risk_level")}',
                    'recommendation': frost_risk.get('recommendation', ''),
                    'timestamp': datetime.now().isoformat()
                })
        
        # Check for high winds
        wind_speed = weather_data['wind']['speed']
        if wind_speed > 15:
            alerts.append({
                'type': 'high_wind',
                'severity': 'medium',
                'message': f'High winds: {wind_speed} m/s',
                'recommendation': 'Secure structures and protect young plants',
                'timestamp': datetime.now().isoformat()
            })
        
        # Check forecast for heavy rain
        if 'hourly' in forecast_data:
            total_rain = sum([h.get('rain_3h', 0) for h in forecast_data['hourly'][:8]])
            if total_rain > 50:
                alerts.append({
                    'type': 'heavy_rain',
                    'severity': 'medium',
                    'message': f'Heavy rainfall expected: {total_rain:.1f}mm in 24h',
                    'recommendation': 'Ensure proper drainage, delay irrigation',
                    'timestamp': datetime.now().isoformat()
                })
        
        result = {
            'location': {'latitude': lat, 'longitude': lng},
            'timestamp': datetime.now().isoformat(),
            'alerts': alerts,
            'alert_count': len(alerts),
            'all_clear': len(alerts) == 0
        }
        
        logger.info(f"✅ Weather alerts retrieved: {len(alerts)} active")
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"❌ Weather alerts error: {e}")
        return jsonify({
            'error': 'Failed to retrieve weather alerts',
            'details': str(e)
        }), 500


# ============================================================
# INTEGRATED ANALYSIS ENDPOINT
# ============================================================

@app.route('/api/weather/integrated', methods=['GET'])
def get_integrated_analysis():
    """
    Get integrated Weather + Soil + NDVI analysis
    
    URL: /api/weather/integrated?lat=<latitude>&lng=<longitude>&include_soil=true&include_ndvi=true
    Method: GET
    
    Returns:
        JSON with integrated analysis
    """
    try:
        lat = request.args.get('lat', type=float)
        lng = request.args.get('lng', type=float)

        if lat is None or lng is None:
            return jsonify({'error': 'lat and lng query parameters are required'}), 400

        if not weather_collector:
            return jsonify({'error': 'Weather collector not initialized'}), 503
        
        # Get query parameters
        include_soil = request.args.get('include_soil', 'true').lower() == 'true'
        include_ndvi = request.args.get('include_ndvi', 'true').lower() == 'true'
        coordinate_source = request.args.get('coordinate_source', 'manual') # Default to 'manual' for API calls
        
        logger.info(f"🔗 Integrated analysis request: ({lat}, {lng}), source={coordinate_source}, soil={include_soil}, ndvi={include_ndvi}")
        
        # Get integrated analysis (pass booleans as keywords so they don't bind to a str parameter)
        integrated_data = weather_collector.get_integrated_analysis(
            lat, lng,
            coordinate_source=coordinate_source,
            include_soil=include_soil,
            include_ndvi=include_ndvi
        )
        
        if 'error' in integrated_data:
            return jsonify(integrated_data), 400
        
        logger.info(f"✅ Integrated analysis complete for ({lat}, {lng})")

        # NOTE: NDVI image serving has been disabled; we do not attach
        # `report_image_url` to responses anymore. If you wish to re-enable
        # image hosting, add a guarded static route and recreate the URL here.

        return jsonify(integrated_data), 200
        
    except Exception as e:
        logger.error(f"❌ Integrated analysis error: {e}")
        return jsonify({
            'error': 'Failed to perform integrated analysis',
            'details': str(e)
        }), 500


# ============================================================
# DEBUG ENDPOINT
# ============================================================

@app.route('/api/weather/debug', methods=['GET'])
def debug_info():
    """Debug information for troubleshooting"""
    try:
        debug_data = {
            'system_info': {
                'service': 'Weather Analysis Backend',
                'version': '1.0.0',
                'timestamp': datetime.now().isoformat(),
                'port': 5003
            },
            'modules': {
                'weather_collector': weather_collector is not None,
                'openweather_api': (getattr(weather_collector, 'openweather_api', None) is not None) if weather_collector else False,
                'copernicus_api': (getattr(weather_collector, 'copernicus_api', None) is not None) if weather_collector else False
            },
            'api_keys': {
                'openweather': bool(os.getenv('OPENWEATHER_API_KEY'))
            },
            'integration_endpoints': {
                'soil_api': (weather_collector and getattr(weather_collector, 'soil_api_url', None)),
                'ndvi_api': (weather_collector and getattr(weather_collector, 'ndvi_api_url', None))
            },
            'available_endpoints': [
                'GET /api/weather/health',
                'GET /api/weather/current',
                'GET /api/weather/hourly',
                'POST /api/weather/historical',
                'GET /api/weather/agricultural',
                'GET /api/weather/alerts',
                'GET /api/weather/integrated',
                'GET /api/weather/debug'
            ],
            'test_locations': [
                {'name': 'Punjab', 'lat': 30.3398, 'lng': 76.3869},
                {'name': 'Maharashtra', 'lat': 18.15, 'lng': 74.5777},
                {'name': 'California', 'lat': 36.7783, 'lng': -119.4179}
            ]
        }
        
        return jsonify(debug_data), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Debug info failed',
            'details': str(e)
        }), 500


# ============================================================
# MAIN ENTRY POINT
# ============================================================


# ============================================================
# RAW VS COMPUTED COMPARISON ENDPOINT
# ============================================================


@app.route('/api/weather/compare', methods=['GET'])
def compare_raw_and_computed():
    """Return raw API responses (when available) alongside computed agricultural context.

    Query parameters:
      lat (float) - latitude
      lng (float) - longitude
      include_soil (bool) - include soil call in integrated analysis (default true)
      include_ndvi (bool) - include ndvi call in integrated analysis (default true)

    Response JSON:
      {
        'location': { 'latitude': ..., 'longitude': ... },
        'raw': { 'current_weather': {...}, 'hourly': {...} },
        'computed': { 'agricultural_context': {...}, 'integrated': {...} }
      }
    """
    try:
        lat = request.args.get('lat', type=float)
        lng = request.args.get('lng', type=float)

        if lat is None or lng is None:
            return jsonify({'error': 'lat and lng query parameters are required'}), 400

        if not weather_collector:
            return jsonify({'error': 'Weather collector not initialized'}), 503

        include_soil = request.args.get('include_soil', 'true').lower() == 'true'
        include_ndvi = request.args.get('include_ndvi', 'true').lower() == 'true'

        # Fetch raw current weather (this returns the already-normalized structure from the collector)
        raw_current = weather_collector.get_current_weather(lat, lng)

        # Fetch hourly forecast raw
        raw_hourly = weather_collector.get_hourly_forecast(lat, lng, hours=24)

        # Computed agricultural context comes from the collector's helper (attached to current weather)
        computed_ag = raw_current.get('agricultural_context') if isinstance(raw_current, dict) else None

        # Also produce an integrated analysis (which will call soil/ndvi as requested)
        integrated = weather_collector.get_integrated_analysis(lat, lng, coordinate_source='api_compare', include_soil=include_soil, include_ndvi=include_ndvi)

        result = {
            'location': {'latitude': lat, 'longitude': lng},
            'raw': {
                'current_weather': raw_current,
                'hourly_24h': raw_hourly
            },
            'computed': {
                'agricultural_context': computed_ag,
                'integrated_analysis': integrated
            },
            'timestamp': datetime.now().isoformat()
        }

        return jsonify(result), 200

    except Exception as e:
        logger.error(f"❌ Comparison endpoint error: {e}")
        return jsonify({'error': 'Failed to produce comparison', 'details': str(e)}), 500


if __name__ == '__main__':
    # ASCII-only startup messages to avoid Windows console encoding errors
    print('=' * 80)
    print('WEATHER ANALYSIS BACKEND')
    print('=' * 80)
    print('\nAPI Endpoints (use query params for GET requests):')
    print('   GET    /api/weather/health')
    print('   GET    /api/weather/current?lat=...&lng=...')
    print('   GET    /api/weather/hourly?lat=...&lng=...')
    print('   POST   /api/weather/historical (with JSON body)')
    print('   GET    /api/weather/agricultural?lat=...&lng=...')
    print('   GET    /api/weather/alerts?lat=...&lng=...')
    print('   GET    /api/weather/integrated?lat=...&lng=...')
    print('   GET    /api/weather/debug')
    
    print('\nFeatures:')
    print('   - Real-time weather (OpenWeatherMap)')
    print('   - Historical data (Copernicus ERA5)')
    print('   - Agricultural indices (GDD, ET, Frost, Heat)')
    print('   - Weather-Soil integration')
    print('   - Weather-NDVI integration')
    
    print('\nIntegration:')
    print('   - Soil API: http://127.0.0.1:5002')
    print('   - NDVI API: http://127.0.0.1:5001')
    
    print('=' * 80)
    
    # Get port from environment or default to 5003
    port = int(os.getenv('WEATHER_PORT', 5003))
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    
    print(f"\nServer starting on http://{host}:{port}")
    print(f"Weather collector: {'Ready' if weather_collector else 'Not available'}")
    print('\n' + '=' * 80 + '\n')
    
    # Run Flask app
    app.run(host=host, port=port, debug=True)
