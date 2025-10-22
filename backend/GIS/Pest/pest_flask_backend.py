#!/usr/bin/env python3
"""
Pest & Disease Detection Flask API Backend
Port: 5006

Provides REST API endpoints for pest and disease detection and risk assessment
Integrates with Weather (5003) module

Location: D:\\CropEye1\\backend\\GIS\\PestDisease\\pest_flask_backend.py

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

# Import pest disease detection module
try:
    from pest_disease_detection import PestDiseaseDetector, detect_threats
except ImportError:
    print("ERROR: pest_disease_detection.py not found in current directory")
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

# Initialize Pest & Disease Detector
try:
    detector = PestDiseaseDetector()
    logger.info("✅ Pest & Disease Detector initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Pest & Disease Detector: {e}")
    detector = None

# External module URLs
WEATHER_API_URL = os.getenv('WEATHER_API_URL', 'http://127.0.0.1:5003')


# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Pest & Disease Detection API',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat(),
        'detector_loaded': detector is not None
    }), 200


# ============================================================================
# PEST & DISEASE ENDPOINTS
# ============================================================================

@app.route('/api/pest/detect', methods=['POST'])
def detect_pests():
    """
    Detect pest risks
    
    Request Body:
    {
        "temp": 25,
        "humidity": 70,
        "crop_type": "rice",
        "additional_factors": {
            "high_nitrogen": true,
            "flowering_stage": false
        }
    }
    """
    try:
        data = request.get_json()
        
        if not detector:
            return jsonify({
                'success': False,
                'error': 'Detector not initialized',
                'timestamp': datetime.now().isoformat()
            }), 503
        
        temp = float(data.get('temp', 25))
        humidity = float(data.get('humidity', 70))
        crop_type = data.get('crop_type', 'rice')
        additional_factors = data.get('additional_factors', {})
        
        pests = detector.assess_pest_risk(temp, humidity, crop_type, additional_factors)
        
        logger.info(f"🐛 Pest detection for {crop_type}: {len(pests)} threats found")
        
        return jsonify({
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'crop_type': crop_type,
            'conditions': {'temp': temp, 'humidity': humidity},
            'pests': pests,
            'total_pests': len(pests)
        }), 200
        
    except Exception as e:
        logger.error(f"❌ Error detecting pests: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500


@app.route('/api/disease/detect', methods=['POST'])
def detect_diseases():
    """
    Detect disease risks
    
    Request Body:
    {
        "temp": 26,
        "humidity": 85,
        "crop_type": "rice",
        "additional_factors": {
            "high_nitrogen": true,
            "night_dew": true
        }
    }
    """
    try:
        data = request.get_json()
        
        if not detector:
            return jsonify({
                'success': False,
                'error': 'Detector not initialized',
                'timestamp': datetime.now().isoformat()
            }), 503
        
        temp = float(data.get('temp', 25))
        humidity = float(data.get('humidity', 70))
        crop_type = data.get('crop_type', 'rice')
        additional_factors = data.get('additional_factors', {})
        
        diseases = detector.assess_disease_risk(temp, humidity, crop_type, additional_factors)
        
        logger.info(f"🦠 Disease detection for {crop_type}: {len(diseases)} threats found")
        
        return jsonify({
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'crop_type': crop_type,
            'conditions': {'temp': temp, 'humidity': humidity},
            'diseases': diseases,
            'total_diseases': len(diseases)
        }), 200
        
    except Exception as e:
        logger.error(f"❌ Error detecting diseases: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500


@app.route('/api/threats/comprehensive', methods=['POST'])
def comprehensive_assessment():
    """
    Comprehensive pest and disease assessment
    
    Request Body:
    {
        "temp": 26,
        "humidity": 80,
        "crop_type": "wheat",
        "additional_factors": {}
    }
    """
    try:
        data = request.get_json()
        
        if not detector:
            return jsonify({
                'success': False,
                'error': 'Detector not initialized',
                'timestamp': datetime.now().isoformat()
            }), 503
        
        temp = float(data.get('temp', 25))
        humidity = float(data.get('humidity', 70))
        crop_type = data.get('crop_type', 'rice')
        additional_factors = data.get('additional_factors', {})
        
        assessment = detector.comprehensive_assessment(temp, humidity, crop_type, additional_factors)
        
        logger.info(f"🔍 Comprehensive assessment for {crop_type}: {assessment['total_threats']} threats")
        
        return jsonify({
            'success': True,
            'crop_type': crop_type,
            'conditions': {'temp': temp, 'humidity': humidity},
            **assessment
        }), 200
        
    except Exception as e:
        logger.error(f"❌ Error in comprehensive assessment: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500


@app.route('/api/threats/integrated', methods=['POST'])
def integrated_assessment():
    """
    Integrated assessment with weather data
    
    Request Body:
    {
        "latitude": 30.8,
        "longitude": 75.8,
        "crop_type": "wheat",
        "additional_factors": {}
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
        crop_type = data.get('crop_type', 'rice')
        additional_factors = data.get('additional_factors', {})
        
        logger.info(f"🌍 Integrated threat assessment for ({lat}, {lng}), crop: {crop_type}")
        
        result = {
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'location': {'latitude': lat, 'longitude': lng},
            'crop_type': crop_type,
            'data_sources': []
        }
        # keep fallback reasons per upstream service to avoid overwriting
        result['used_fallback_reason'] = {}
        
        # Fetch weather data (respect USE_REAL_WEATHER env flag)
        weather_data = {}
        use_real_weather = str(os.getenv('USE_REAL_WEATHER', 'true')).lower() in ('1', 'true', 'yes')
        result['used_weather_service'] = False
        if use_real_weather:
            try:
                # Weather backend exposes current weather as GET /api/weather/current?lat=..&lng=..
                weather_response = requests.get(
                    f"{WEATHER_API_URL}/api/weather/current",
                    params={'lat': lat, 'lng': lng},
                    timeout=10
                )
                if weather_response.status_code == 200:
                    weather_json = weather_response.json()
                    result['data_sources'].append('weather')
                    weather_data = {
                        'temp': weather_json.get('temperature', {}).get('current', 25),
                        'humidity': weather_json.get('humidity', 70)
                    }
                    result['weather_data'] = weather_data
                    result['used_weather_service'] = True
                    logger.info("Weather data retrieved from service")
                else:
                    reason = f"service_status_{weather_response.status_code}"
                    result['used_fallback_reason']['weather'] = reason
                    logger.warning(f"Weather service returned status {weather_response.status_code}")
                    weather_data = {'temp': 25, 'humidity': 70}
            except Exception as e:
                result['used_fallback_reason']['weather'] = str(e)
                logger.warning(f"Could not fetch weather data: {e}")
                weather_data = {'temp': 25, 'humidity': 70}
        else:
            # Explicitly configured to not use real weather
            result['used_fallback_reason']['weather'] = 'USE_REAL_WEATHER=false'
            logger.info('Skipping weather service call (USE_REAL_WEATHER=false)')
            weather_data = {'temp': 25, 'humidity': 70}
        
        # Perform assessment
        if detector:
            assessment = detector.comprehensive_assessment(
                temp=weather_data['temp'],
                humidity=weather_data['humidity'],
                crop_type=crop_type,
                additional_factors=additional_factors
            )
            result.update(assessment)
            logger.info(f"✅ Threats: {assessment['total_threats']} detected")
        else:
            result['success'] = False
            result['error'] = 'Detector not available'
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"❌ Error in integrated assessment: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500


@app.route('/api/pest/info/<pest_name>', methods=['GET'])
def get_pest_info(pest_name):
    """Get detailed information about a specific pest"""
    try:
        if not detector:
            return jsonify({
                'success': False,
                'error': 'Detector not initialized',
                'timestamp': datetime.now().isoformat()
            }), 503
        
        info = detector.get_pest_info(pest_name)
        
        if info:
            return jsonify({
                'success': True,
                'timestamp': datetime.now().isoformat(),
                'pest_name': pest_name,
                'info': info
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': f'Pest "{pest_name}" not found in database',
                'timestamp': datetime.now().isoformat()
            }), 404
            
    except Exception as e:
        logger.error(f"❌ Error getting pest info: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500


@app.route('/api/disease/info/<disease_name>', methods=['GET'])
def get_disease_info(disease_name):
    """Get detailed information about a specific disease"""
    try:
        if not detector:
            return jsonify({
                'success': False,
                'error': 'Detector not initialized',
                'timestamp': datetime.now().isoformat()
            }), 503
        
        info = detector.get_disease_info(disease_name)
        
        if info:
            return jsonify({
                'success': True,
                'timestamp': datetime.now().isoformat(),
                'disease_name': disease_name,
                'info': info
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': f'Disease "{disease_name}" not found in database',
                'timestamp': datetime.now().isoformat()
            }), 404
            
    except Exception as e:
        logger.error(f"❌ Error getting disease info: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500


@app.route('/api/database/list', methods=['GET'])
def list_database():
    """List all pests and diseases in database"""
    try:
        if not detector:
            return jsonify({
                'success': False,
                'error': 'Detector not initialized',
                'timestamp': datetime.now().isoformat()
            }), 503
        
        pests = list(detector.PEST_DATABASE.keys())
        diseases = list(detector.DISEASE_DATABASE.keys())
        
        return jsonify({
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'total_pests': len(pests),
            'total_diseases': len(diseases),
            'pests': pests,
            'diseases': diseases
        }), 200
        
    except Exception as e:
        logger.error(f"❌ Error listing database: {e}")
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
    logger.info("🐛 PEST & DISEASE DETECTION API STARTING")
    logger.info("=" * 80)
    logger.info("")
    logger.info("📡 Integration URLs:")
    logger.info(f"   • Weather API: {WEATHER_API_URL}")
    logger.info("")
    logger.info("🌐 Endpoints:")
    logger.info("   • Health:          GET  /api/health")
    logger.info("   • Detect Pests:    POST /api/pest/detect")
    logger.info("   • Detect Disease:  POST /api/disease/detect")
    logger.info("   • Comprehensive:   POST /api/threats/comprehensive")
    logger.info("   • Integrated:      POST /api/threats/integrated")
    logger.info("   • Pest Info:       GET  /api/pest/info/<name>")
    logger.info("   • Disease Info:    GET  /api/disease/info/<name>")
    logger.info("   • List Database:   GET  /api/database/list")
    logger.info("")
    logger.info("=" * 80)
    logger.info("")
    
    app.run(
        host='0.0.0.0',
        port=5006,
        debug=True,
        threaded=True
    )
