#!/usr/bin/env python3
"""
Water Management Flask API Backend
Port: 5005

Provides REST API endpoints for water management and irrigation scheduling
Integrates with Soil (5002) and Weather (5003) modules

Location: D:\\CropEye1\\backend\\GIS\\WaterManagement\\water_flask_backend.py

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

# Load .env from the root of the 'backend' directory for consistency
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
load_dotenv(dotenv_path=os.path.join(backend_dir, '.env'))

# Import water management module
try:
    from water_management import WaterManagementSystem, calculate_irrigation_schedule
except ImportError:
    print("ERROR: water_management.py not found in current directory")
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

# Initialize Water Management System
try:
    wms = WaterManagementSystem()
    logger.info("✅ Water Management System initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Water Management System: {e}")
    wms = None

# External module URLs
SOIL_API_URL = os.getenv('SOIL_API_URL', 'http://127.0.0.1:5002')
WEATHER_API_URL = os.getenv('WEATHER_API_URL', 'http://127.0.0.1:5003')


# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Water Management API',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat(),
        'wms_loaded': wms is not None
    }), 200


# ============================================================================
# WATER MANAGEMENT ENDPOINTS
# ============================================================================

@app.route('/api/water/et0/calculate', methods=['POST'])
def calculate_et0():
    """
    Calculate reference evapotranspiration (ET0) using Penman-Monteith
    
    Request Body:
    {
        "temp_max": 32,
        "temp_min": 22,
        "rh_mean": 65,
        "wind_speed": 2.5,
        "solar_radiation": 22,
        "elevation": 200
    }
    """
    try:
        data = request.get_json()
        
        if not wms:
            return jsonify({
                'success': False,
                'error': 'Water Management System not initialized',
                'timestamp': datetime.now().isoformat()
            }), 503
        
        # Get parameters
        temp_max = float(data.get('temp_max', 30))
        temp_min = float(data.get('temp_min', 20))
        rh_mean = float(data.get('rh_mean', 65))
        wind_speed = float(data.get('wind_speed', 2.0))
        solar_radiation = float(data.get('solar_radiation', 20))
        elevation = int(round(float(data.get('elevation', 100))))
        
        # Calculate ET0
        et0 = wms.calculate_et0_penman_monteith(
            temp_max=temp_max,
            temp_min=temp_min,
            rh_mean=rh_mean,
            wind_speed=wind_speed,
            solar_radiation=solar_radiation,
            elevation=elevation
        )
        
        logger.info(f"📊 ET0 calculated: {et0:.2f} mm/day")
        
        return jsonify({
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'et0_mm_day': round(et0, 2),
            'input_parameters': {
                'temp_max': temp_max,
                'temp_min': temp_min,
                'rh_mean': rh_mean,
                'wind_speed': wind_speed,
                'solar_radiation': solar_radiation,
                'elevation': elevation
            }
        }), 200
        
    except Exception as e:
        logger.error(f"❌ Error calculating ET0: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500


@app.route('/api/water/irrigation/calculate', methods=['POST'])
def calculate_irrigation():
    """
    Calculate irrigation requirements
    
    Request Body:
    {
        "crop_type": "wheat",
        "growth_stage": "mid",
        "weather_data": {
            "temp_max": 32,
            "temp_min": 22,
            "rh_mean": 65,
            "wind_speed": 2.5,
            "solar_radiation": 22
        },
        "soil_data": {
            "soil_type": "loam",
            "moisture": 0.5,
            "rainfall": 10
        }
    }
    """
    try:
        data = request.get_json()
        
        if not wms:
            return jsonify({
                'success': False,
                'error': 'Water Management System not initialized',
                'timestamp': datetime.now().isoformat()
            }), 503
        
        crop_type = data.get('crop_type', 'wheat')
        growth_stage = data.get('growth_stage', 'mid')
        weather_data = data.get('weather_data', {})
        soil_data = data.get('soil_data', {})
        
        # Calculate irrigation schedule
        schedule = calculate_irrigation_schedule(
            weather_data=weather_data,
            soil_data=soil_data,
            crop_type=crop_type,
            growth_stage=growth_stage
        )
        
        logger.info(f"💧 Irrigation calculated for {crop_type}: {schedule['irrigation']['gross_irrigation_mm']}mm")
        
        return jsonify({
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'crop_type': crop_type,
            'growth_stage': growth_stage,
            'schedule': schedule
        }), 200
        
    except Exception as e:
        logger.error(f"❌ Error calculating irrigation: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500


@app.route('/api/water/irrigation/integrated', methods=['POST'])
def irrigation_integrated():
    """
    Calculate irrigation with integrated data from Soil and Weather modules
    
    Request Body:
    {
        "latitude": 30.8,
        "longitude": 75.8,
        "crop_type": "wheat",
        "growth_stage": "mid"
    }
    """
    try:
        data = request.get_json()
        
        if 'latitude' not in data or 'longitude' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing latitude or longitude',
                'timestamp': datetime.now().isoformat()
            }), 400
        
        lat = float(data['latitude'])
        lng = float(data['longitude'])
        crop_type = data.get('crop_type', 'wheat')
        growth_stage = data.get('growth_stage', 'mid')
        
        logger.info(f"🌍 Integrated irrigation for ({lat}, {lng}), crop: {crop_type}")
        
        result = {
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'location': {'latitude': lat, 'longitude': lng},
            'crop_type': crop_type,
            'growth_stage': growth_stage,
            'data_sources': []
        }
        # keep fallback reasons per upstream service to avoid overwriting
        result['used_fallback_reason'] = {}
        
        # Fetch weather data (honor USE_REAL_WEATHER env flag)
        weather_data = {}
        use_real_weather = str(os.getenv('USE_REAL_WEATHER', 'true')).lower() in ('1', 'true', 'yes')
        result['used_weather_service'] = False
        if use_real_weather:
            try:
                # Weather backend exposes current weather via GET with lat/lng query params
                weather_response = requests.get(
                    f"{WEATHER_API_URL}/api/weather/current",
                    params={'lat': lat, 'lng': lng},
                    timeout=10
                )
                if weather_response.status_code == 200:
                    weather_json = weather_response.json()
                    result['data_sources'].append('weather')
                    # Extract weather parameters
                    weather_data = {
                        'temp_max': weather_json.get('temperature', {}).get('max', 30),
                        'temp_min': weather_json.get('temperature', {}).get('min', 20),
                        'rh_mean': weather_json.get('humidity', 65),
                        'wind_speed': weather_json.get('wind', {}).get('speed', 2.0),
                        'solar_radiation': weather_json.get('solar_radiation', 20) # Get from weather service or use default
                    }
                    result['used_weather_service'] = True
                    logger.info("Weather data retrieved from service")
                else:
                    reason = f"weather_status_{weather_response.status_code}"
                    result['used_fallback_reason']['weather'] = reason
                    logger.warning(f"Weather service returned status {weather_response.status_code}")
                    weather_data = {
                        'temp_max': 30, 'temp_min': 20, 'rh_mean': 65,
                        'wind_speed': 2.0, 'solar_radiation': 20
                    }
            except Exception as e:
                result['used_fallback_reason']['weather'] = str(e)
                logger.warning(f"Could not fetch weather data: {e}")
                weather_data = {
                    'temp_max': 30, 'temp_min': 20, 'rh_mean': 65,
                    'wind_speed': 2.0, 'solar_radiation': 20
                }
        else:
            result['used_fallback_reason']['weather'] = 'USE_REAL_WEATHER=false'
            logger.info('Skipping weather service call (USE_REAL_WEATHER=false)')
            weather_data = {
                'temp_max': 30, 'temp_min': 20, 'rh_mean': 65,
                'wind_speed': 2.0, 'solar_radiation': 20
            }
        
        # Fetch soil data (honor USE_REAL_SOIL env flag)
        soil_data = {}
        use_real_soil = str(os.getenv('USE_REAL_SOIL', 'true')).lower() in ('1', 'true', 'yes')
        result['used_soil_service'] = False
        if use_real_soil:
            try:
                # Soil analyze endpoint accepts POST and expects latitude/longitude
                soil_response = requests.post(
                    f"{SOIL_API_URL}/api/soil/analyze",
                    json={'latitude': lat, 'longitude': lng},
                    timeout=10
                )
                if soil_response.status_code == 200:
                    soil_json = soil_response.json()
                    result['data_sources'].append('soil')
                    # Extract soil parameters
                    soil_props = soil_json.get('soil_properties', {})
                    soil_texture = soil_props.get('texture', {}).get('value', 'loam')
                    soil_data = {
                        'soil_type': soil_texture,
                        'moisture': soil_props.get('moisture', {}).get('value', 0.5), # Use moisture if available
                        'rainfall': 0  # Recent rainfall, assume 0 for this call
                    }
                    result['used_soil_service'] = True
                    logger.info("Soil data retrieved from service")
                else:
                    reason = f"soil_status_{soil_response.status_code}"
                    result['used_fallback_reason']['soil'] = reason
                    logger.warning(f"Soil service returned status {soil_response.status_code}")
                    soil_data = {
                        'soil_type': 'loam',
                        'moisture': 0.5,
                        'rainfall': 0
                    }
            except Exception as e:
                result['used_fallback_reason']['soil'] = str(e)
                logger.warning(f"Could not fetch soil data: {e}")
                soil_data = {
                    'soil_type': 'loam',
                    'moisture': 0.5,
                    'rainfall': 0
                }
        else:
            result['used_fallback_reason']['soil'] = 'USE_REAL_SOIL=false'
            logger.info('Skipping soil service call (USE_REAL_SOIL=false)')
            soil_data = {
                'soil_type': 'loam',
                'moisture': 0.5,
                'rainfall': 0
            }
        
        # Calculate irrigation schedule
        if wms:
            schedule = calculate_irrigation_schedule(
                weather_data=weather_data,
                soil_data=soil_data,
                crop_type=crop_type,
                growth_stage=growth_stage
            )
            result['schedule'] = schedule
            result['weather_data'] = weather_data
            result['soil_data'] = soil_data
            logger.info(f"✅ Irrigation: {schedule['irrigation']['gross_irrigation_mm']}mm recommended")
        else:
            result['success'] = False
            result['error'] = 'Water Management System not available'
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"❌ Error in integrated irrigation: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500


@app.route('/api/water/stress/calculate', methods=['POST'])
def calculate_stress():
    """
    Calculate water stress index
    
    Request Body:
    {
        "current_moisture": 0.5,
        "field_capacity": 1.0
    }
    """
    try:
        data = request.get_json()
        
        if not wms:
            return jsonify({
                'success': False,
                'error': 'Water Management System not initialized',
                'timestamp': datetime.now().isoformat()
            }), 503
        
        current_moisture = float(data.get('current_moisture', 0.5))
        field_capacity = float(data.get('field_capacity', 1.0))
        
        # Calculate water stress index as ratio of current_moisture to field_capacity
        if field_capacity == 0:
            raise ValueError("Field capacity cannot be zero")
        stress_index = current_moisture / field_capacity
        
        # Determine stress level
        if stress_index < 0.3:
            stress_level = "Low"
        elif stress_index < 0.6:
            stress_level = "Moderate"
        else:
            stress_level = "High"
        
        return jsonify({
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'water_stress_index': stress_index,
            'stress_level': stress_level,
            'current_moisture': current_moisture,
            'field_capacity': field_capacity
        }), 200
        
    except Exception as e:
        logger.error(f"❌ Error calculating stress: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500


@app.route('/api/water/crops', methods=['GET'])
def list_crops():
    """List supported crops with their coefficients"""
    try:
        if not wms:
            return jsonify({
                'success': False,
                'error': 'Water Management System not initialized',
                'timestamp': datetime.now().isoformat()
            }), 503
        
        crops = []
        for crop_name, coefficients in wms.CROP_COEFFICIENTS.items():
            crops.append({
                'name': crop_name,
                'kc_initial': coefficients['initial'],
                'kc_mid': coefficients['mid'],
                'kc_late': coefficients['late']
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
    logger.info("💧 WATER MANAGEMENT API STARTING")
    logger.info("=" * 80)
    logger.info("")
    logger.info("📡 Integration URLs:")
    logger.info(f"   • Soil API:    {SOIL_API_URL}")
    logger.info(f"   • Weather API: {WEATHER_API_URL}")
    logger.info("")
    logger.info("🌐 Endpoints:")
    logger.info("   • Health:           GET  /api/health")
    logger.info("   • Calculate ET0:    POST /api/water/et0/calculate")
    logger.info("   • Calculate Irrig:  POST /api/water/irrigation/calculate")
    logger.info("   • Integrated:       POST /api/water/irrigation/integrated")
    logger.info("   • Water Stress:     POST /api/water/stress/calculate")
    logger.info("   • List Crops:       GET  /api/water/crops")
    logger.info("")
    logger.info("=" * 80)
    logger.info("")
    
    app.run(
        host='0.0.0.0',
        port=5005,
        debug=True,
        threaded=True,
        use_reloader=False
    )
