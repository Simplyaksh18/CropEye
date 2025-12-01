#!/usr/bin/env python3
"""
Crop Recommendation Flask API Backend
Port: 5004

Provides REST API endpoints for crop recommendation system
Integrates with Soil (5002), Weather (5003), NDVI (5001) modules

Location: D:\\CropEye1\\backend\\GIS\\CropRecommendation\\crop_flask_backend.py

Author: CropEye1 System
Date: October 19, 2025
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import os
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv("file.env")

# Import crop recommendation module
try:
    from crop_recomendation import CropRecommender
except ImportError:
    print("ERROR: crop_recommendation.py not found in current directory")
    exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize recommender with crop database (use path relative to this file)
CROP_DIR = os.path.dirname(__file__)
CROP_DATA_PATH = os.path.join(CROP_DIR, 'data', 'crop_params_india.json')
if not os.path.exists(CROP_DATA_PATH):
    logger.error(f"Crop database not found at {CROP_DATA_PATH}")
    # Create data directory if needed (create under module data path)
    os.makedirs(os.path.join(CROP_DIR, 'data'), exist_ok=True)
    logger.warning(f"Please add crop_params_india.json to {os.path.join(CROP_DIR,'data')} directory")

try:
    recommender = CropRecommender(crop_table_path=CROP_DATA_PATH)
    logger.info("✅ Crop Recommender initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Crop Recommender: {e}")
    recommender = None

# External module URLs
SOIL_API_URL = os.getenv('SOIL_API_URL', 'http://127.0.0.1:5002')
WEATHER_API_URL = os.getenv('WEATHER_API_URL', 'http://127.0.0.1:5003')
NDVI_API_URL = os.getenv('NDVI_API_URL', 'http://127.0.0.1:5001')


# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Crop Recommendation API',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat(),
        'recommender_loaded': recommender is not None
    }), 200


# ============================================================================
# CROP RECOMMENDATION ENDPOINTS
# ============================================================================

@app.route('/api/crop/recommend', methods=['POST'])
def recommend_crops():
    """
    Recommend crops based on input parameters
    
    Request Body:
    {
        "latitude": 30.8,
        "longitude": 75.8,
        "ph": 7.1,
        "rainfall": 900,
        "temp_mean": 30,
        "ndvi": 0.62
    }
    
    Returns ranked crop recommendations
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['latitude', 'longitude', 'ph', 'rainfall', 'temp_mean']
        missing_fields = [f for f in required_fields if f not in data]
        
        if missing_fields:
            return jsonify({
                'success': False,
                'error': f'Missing required fields: {", ".join(missing_fields)}',
                'timestamp': datetime.now().isoformat()
            }), 400
        
        if not recommender:
            return jsonify({
                'success': False,
                'error': 'Crop recommender not initialized. Check crop database.',
                'timestamp': datetime.now().isoformat()
            }), 503
        
        # Prepare input for recommender
        input_params = {
            'latitude': float(data['latitude']),
            'longitude': float(data['longitude']),
            'ph': float(data['ph']),
            'rainfall': float(data['rainfall']),
            'temp_mean': float(data['temp_mean']),
            'ndvi': float(data.get('ndvi', 0.5))
        }
        
        logger.info(f"📊 Crop recommendation request: {input_params}")
        
        # Get recommendations
        recommendations = recommender.recommend(input_params)
        
        # Format response
        response = {
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'location': {
                'latitude': input_params['latitude'],
                'longitude': input_params['longitude']
            },
            'input_parameters': input_params,
            'recommendations': recommendations[:10],  # Top 10 crops
            'total_crops_analyzed': len(recommendations)
        }
        
        logger.info(f"✅ Top recommendation: {recommendations[0]['crop']} (score: {recommendations[0]['score']})")
        
        return jsonify(response), 200
        
    except ValueError as e:
        logger.error(f"❌ Invalid input: {e}")
        return jsonify({
            'success': False,
            'error': f'Invalid input parameters: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 400
        
    except Exception as e:
        logger.error(f"❌ Error in crop recommendation: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500


@app.route('/api/crop/recommend/integrated', methods=['POST'])
def recommend_crops_integrated():
    """
    Get crop recommendations with integrated data from Soil, Weather, and NDVI modules
    
    Request Body:
    {
        "latitude": 30.8,
        "longitude": 75.8
    }
    
    Fetches data from other modules and provides comprehensive recommendations
    """
    try:
        data = request.get_json()
        
        # Validate coordinates
        if 'latitude' not in data or 'longitude' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing latitude or longitude',
                'timestamp': datetime.now().isoformat()
            }), 400
        
        lat = float(data['latitude'])
        lng = float(data['longitude'])
        
        logger.info(f"🌍 Integrated crop recommendation for ({lat}, {lng})")
        
        # Initialize result
        result = {
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'location': {'latitude': lat, 'longitude': lng},
            'data_sources': [],
            'recommendations': None
        }
        
        # Fetch soil data
        soil_data = None
        try:
            soil_response = requests.post(
                f"{SOIL_API_URL}/api/soil/analyze",
                json={'latitude': lat, 'longitude': lng},
                timeout=10
            )
            if soil_response.status_code == 200:
                soil_data = soil_response.json()
                result['data_sources'].append('soil')
                logger.info("✅ Soil data retrieved")
        except Exception as e:
            logger.warning(f"⚠️ Could not fetch soil data: {e}")
        
        # Fetch weather data
        weather_data = None
        try:
            # Weather endpoint is GET with query params
            weather_response = requests.get(
                f"{WEATHER_API_URL}/api/weather/current",
                params={'lat': lat, 'lng': lng},
                timeout=10
            )
            if weather_response.status_code == 200:
                try:
                    weather_data = weather_response.json()
                except Exception:
                    weather_data = None
                if weather_data:
                    result['data_sources'].append('weather')
                    logger.info("✅ Weather data retrieved")
                    logger.debug(f"Weather payload snippet: {str(weather_data)[:300]}")
        except requests.RequestException as e:
            logger.warning(f"⚠️ Could not fetch weather data: {e}")
        
        # Fetch NDVI data
        ndvi_data = None
        try:
            ndvi_response = requests.post(
                f"{NDVI_API_URL}/api/ndvi/analyze",
                json={'latitude': lat, 'longitude': lng, 'use_real_data': True},
                timeout=10
            )
            if ndvi_response.status_code == 200:
                try:
                    ndvi_data = ndvi_response.json()
                except Exception:
                    ndvi_data = None
                if ndvi_data:
                    result['data_sources'].append('ndvi')
                    logger.info("✅ NDVI data retrieved")
                    logger.debug(f"NDVI payload snippet: {str(ndvi_data)[:300]}")
        except requests.RequestException as e:
            logger.warning(f"⚠️ Could not fetch NDVI data: {e}")
        
        # Extract parameters for recommendation with robust parsing
        input_params = {
            'latitude': lat,
            'longitude': lng,
            'ph': 6.5,  # Default
            'rainfall': 700,  # Default
            'temp_mean': 25,  # Default
            'ndvi': 0.5  # Default
        }

        # Helper: robust NDVI extractor (handles several response shapes)
        def _extract_ndvi(payload):
            try:
                if payload is None:
                    return None
                # Common wrapper: {'status':..., 'data': {...}}
                if isinstance(payload, dict) and 'data' in payload:
                    payload = payload['data']

                if isinstance(payload, dict):
                    # Case: {'ndvi': 0.5} or {'ndvi': {'value': 0.5}}
                    if 'ndvi' in payload:
                        v = payload['ndvi']
                        if isinstance(v, dict) and 'value' in v:
                            return float(v['value'])
                        try:
                            return float(v)
                        except Exception:
                            pass
                    # Case: payload directly contains 'value' key
                    if 'value' in payload:
                        try:
                            return float(payload['value'])
                        except Exception:
                            pass
                return None
            except Exception:
                return None

        # Helper: robust weather extractor
        def _extract_weather(payload):
            temp = None
            rain = None
            try:
                if payload is None:
                    return {'temp': None, 'rain': None}
                # If wrapper exists
                if isinstance(payload, dict):
                    # Direct keys
                    if 'temperature' in payload and isinstance(payload['temperature'], dict):
                        temp = payload['temperature'].get('current')
                    if 'temp' in payload:
                        try:
                            temp = float(payload['temp'])
                        except Exception:
                            pass
                    # agricultural_context.et.temperature
                    ac = payload.get('agricultural_context') or payload.get('agri')
                    if isinstance(ac, dict):
                        # some services nest ET data
                        et = ac.get('et') or ac.get('et_mm')
                        if isinstance(et, dict) and 'temperature' in et:
                            temp = et.get('temperature')
                        # rainfall may be under 'rain' or 'rainfall'
                        rain = payload.get('rain') or payload.get('rainfall') or ac.get('rain') or ac.get('rainfall')
                    # top-level rain keys
                    if rain is None:
                        rain = payload.get('rain') or payload.get('rainfall') or payload.get('precipitation')
                return {'temp': (float(temp) if temp is not None else None), 'rain': (float(rain) if rain is not None else None)}
            except Exception:
                return {'temp': None, 'rain': None}

        # Override with actual data
        if soil_data:
            result['soil_data'] = soil_data
            # Try multiple soil schemas
            try:
                # 1) soil_data['soil_properties']['ph']['value']
                if isinstance(soil_data, dict):
                    sp = soil_data.get('soil_properties') or soil_data.get('properties') or soil_data
                    if isinstance(sp, dict):
                        ph_val = None
                        if 'ph' in sp and isinstance(sp['ph'], dict):
                            ph_val = sp['ph'].get('value')
                        elif 'ph' in sp:
                            ph_val = sp.get('ph')
                        if ph_val is not None:
                            try:
                                input_params['ph'] = float(ph_val)
                            except Exception:
                                pass
            except Exception:
                pass

        if weather_data:
            result['weather_data'] = weather_data
            w = _extract_weather(weather_data)
            if w.get('temp') is not None:
                input_params['temp_mean'] = w['temp']
            if w.get('rain') is not None:
                input_params['rainfall'] = w['rain']

        if ndvi_data:
            result['ndvi_data'] = ndvi_data
            ndv = _extract_ndvi(ndvi_data)
            if ndv is not None:
                input_params['ndvi'] = ndv
        
        # Get recommendations
        if recommender:
            recommendations = recommender.recommend(input_params)
            result['recommendations'] = recommendations[:10]
            result['input_parameters'] = input_params
            logger.info(f"✅ Top crop: {recommendations[0]['crop']}")
        else:
            result['success'] = False
            result['error'] = 'Recommender not available'
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"❌ Error in integrated recommendation: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500


@app.route('/api/crop/list', methods=['GET'])
def list_crops():
    """List all available crops in the database"""
    try:
        if not recommender or not recommender.crop_table:
            return jsonify({
                'success': False,
                'error': 'Crop database not loaded',
                'timestamp': datetime.now().isoformat()
            }), 503
        
        crops = []
        for crop_name, params in recommender.crop_table.items():
            crops.append({
                'name': crop_name,
                'ph_range': [params['ph_min'], params['ph_max']],
                'rainfall_range_mm': [params['rain_min_mm'], params['rain_max_mm']],
                'temp_range_c': [params['tmin'], params['tmax']]
            })
        
        return jsonify({
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'total_crops': len(crops),
            'crops': crops
        }), 200
        
    except Exception as e:
        logger.error(f"❌ Error listing crops: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found',
        'timestamp': datetime.now().isoformat()
    }), 404


@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({
        'success': False,
        'error': 'Internal server error',
        'timestamp': datetime.now().isoformat()
    }), 500


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    logger.info("=" * 80)
    logger.info("🌾 CROP RECOMMENDATION API STARTING")
    logger.info("=" * 80)
    logger.info("")
    logger.info("📡 Integration URLs:")
    logger.info(f"   • Soil API:    {SOIL_API_URL}")
    logger.info(f"   • Weather API: {WEATHER_API_URL}")
    logger.info(f"   • NDVI API:    {NDVI_API_URL}")
    logger.info("")
    logger.info("🌐 Endpoints:")
    logger.info("   • Health:      GET  /api/health")
    logger.info("   • Recommend:   POST /api/crop/recommend")
    logger.info("   • Integrated:  POST /api/crop/recommend/integrated")
    logger.info("   • List Crops:  GET  /api/crop/list")
    logger.info("")
    logger.info("=" * 80)
    logger.info("")
    
    app.run(
        host='0.0.0.0',
        port=5004,
        debug=True,
        threaded=True
    )
