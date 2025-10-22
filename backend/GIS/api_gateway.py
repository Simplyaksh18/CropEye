#!/usr/bin/env python3
"""
CropEye1 Unified API Gateway
Single entry point for all agricultural analysis modules

Location: D:\\CropEye1\\backend\\api_gateway.py
Port: 5000

Features:
- Routes to NDVI (5001), Soil (5002), Weather (5003)
- Comprehensive analysis endpoint
- Health monitoring
- Error handling
- Request/Response formatting
- CORS support
- Logging

API Endpoints:
- GET  /api/v1/health                           - System health
- GET  /api/v1/health/detailed                  - Detailed health check
- POST /api/v1/analysis/comprehensive           - All modules
- GET  /api/v1/ndvi/:lat/:lng                   - NDVI analysis
- GET  /api/v1/soil/:lat/:lng                   - Soil analysis
- GET  /api/v1/weather/:lat/:lng                - Weather analysis
- POST /api/v1/batch/analyze                    - Batch processing

Author: CropEye1 System
Date: October 19, 2025
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import logging
from datetime import datetime
from typing import Dict, List, Optional
import traceback
import time
from functools import wraps

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Module endpoints
MODULES = {
    'ndvi': {
        'url': 'http://127.0.0.1:5001',
        'name': 'NDVI Analysis Module',
        'endpoints': {
            'calculate': '/api/ndvi/calculate',
            'health': '/api/health'
        }
    },
    'soil': {
        'url': 'http://127.0.0.1:5002',
        'name': 'Soil Analysis Module',
        'endpoints': {
            'analyze': '/api/soil/analyze',
            'health': '/api/health'
        }
    },
    'weather': {
        'url': 'http://127.0.0.1:5003',
        'name': 'Weather Analysis Module',
        'endpoints': {
            'current': '/api/weather/current',
            'forecast': '/api/weather/forecast',
            'historical': '/api/weather/historical',
            'health': '/api/health'
        }
    }
}

# Add water microservice
MODULES['water'] = {
    'url': 'http://127.0.0.1:5005',
    'name': 'Water Management Module',
    'endpoints': {
        'integrated': '/api/water/irrigation/integrated',
        'calculate': '/api/water/irrigation/calculate',
        'et0': '/api/water/et0/calculate',
        'stress': '/api/water/stress/calculate',
        'crops': '/api/water/crops',
        'health': '/api/health'
    }
}

# Request timeout
REQUEST_TIMEOUT = 30


# ============================================================================
# DECORATORS
# ============================================================================

def log_request(f):
    """Decorator to log all requests"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time.time()
        logger.info(f"📥 {request.method} {request.path} from {request.remote_addr}")
        
        try:
            response = f(*args, **kwargs)
            elapsed = time.time() - start_time
            logger.info(f"✅ {request.method} {request.path} completed in {elapsed:.3f}s")
            return response
        except Exception as e:
            elapsed = time.time() - start_time
            logger.error(f"❌ {request.method} {request.path} failed in {elapsed:.3f}s: {e}")
            raise
    
    return decorated_function


def validate_coordinates(f):
    """Decorator to validate latitude and longitude"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Safely obtain JSON body (may be None for GET requests)
        json_body = request.get_json(silent=True) or {}

        # Priority: path params (kwargs) > JSON body > query params
        lat = kwargs.get('lat') if kwargs.get('lat') is not None else json_body.get('latitude') or request.args.get('lat') or request.args.get('latitude')
        lng = kwargs.get('lng') if kwargs.get('lng') is not None else json_body.get('longitude') or request.args.get('lng') or request.args.get('longitude')

        try:
            if lat is None or lng is None:
                return error_response(
                    "Latitude and longitude are required.",
                    status_code=400
                )
            lat_f = float(lat)
            lng_f = float(lng)
            
            if not (-90 <= lat_f <= 90):
                return error_response(
                    "Invalid latitude. Must be between -90 and 90",
                    status_code=400
                )
            
            if not (-180 <= lng_f <= 180):
                return error_response(
                    "Invalid longitude. Must be between -180 and 180",
                    status_code=400
                )
            
            # Add validated coordinates to kwargs
            kwargs['lat'] = lat_f
            kwargs['lng'] = lng_f
            
            return f(*args, **kwargs)
            
        except (ValueError, TypeError) as e:
            return error_response(
                f"Invalid coordinates format: {e}",
                status_code=400
            )
    
    return decorated_function


# ============================================================================
# RESPONSE FORMATTERS
# ============================================================================

def success_response(data: Dict, message: str = "Success", metadata: Optional[Dict] = None) -> tuple:
    """Format successful response"""
    response = {
        'success': True,
        'message': message,
        'timestamp': datetime.now().isoformat(),
        'data': data
    }
    
    if metadata:
        response['metadata'] = metadata
    
    return jsonify(response), 200


def error_response(message: str, error_details: Optional[str] = None, status_code: int = 500) -> tuple:
    """Format error response"""
    response = {
        'success': False,
        'message': message,
        'timestamp': datetime.now().isoformat(),
        'error': {
            'code': status_code,
            'details': error_details
        }
    }
    
    return jsonify(response), status_code


# ============================================================================
# MODULE COMMUNICATION
# ============================================================================

def call_module(module: str, endpoint: str, method: str = 'POST', 
                data: Optional[Dict] = None, timeout: int = REQUEST_TIMEOUT) -> Optional[Dict]:
    """Call a backend module"""
    
    if module not in MODULES:
        logger.error(f"Unknown module: {module}")
        return None
    
    module_info = MODULES[module]
    url = f"{module_info['url']}{endpoint}"
    
    try:
        logger.info(f"📡 Calling {module_info['name']} at {url}")
        
        if method == 'POST':
            response = requests.post(url, json=data, timeout=timeout)
        elif method == 'GET':
            response = requests.get(url, params=data, timeout=timeout)
        else:
            logger.error(f"Unsupported method: {method}")
            return None
        
        response.raise_for_status()
        payload = response.json()
        # annotate that this is a live response (no fallback)
        if isinstance(payload, dict):
            payload.setdefault('used_fallback', False)
        return payload
        
    except requests.exceptions.Timeout:
        logger.error(f"⏰ Timeout calling {module_info['name']}")
        # Return a lightweight fallback to keep gateway responsive in dev
        fb = fallback_response_for_module(module, reason='timeout')
        fb['used_fallback'] = True
        return fb
    
    except requests.exceptions.ConnectionError:
        logger.error(f"🔌 Connection error to {module_info['name']}")
        fb = fallback_response_for_module(module, reason='connection')
        fb['used_fallback'] = True
        return fb
    
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Error calling {module_info['name']}: {e}")
        return {'error': 'request_failed', 'message': str(e), 'used_fallback': False}
    
    except Exception as e:
        logger.error(f"❌ Unexpected error calling {module_info['name']}: {e}")
        fb = fallback_response_for_module(module, reason='unexpected', details=str(e))
        fb['used_fallback'] = True
        return fb


def check_module_health(module: str) -> Dict:
    """Check health of a backend module"""
    
    if module not in MODULES:
        return {'status': 'unknown', 'message': 'Unknown module'}
    
    module_info = MODULES[module]
    url = f"{module_info['url']}{module_info['endpoints']['health']}"
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return {
            'status': 'healthy',
            'name': module_info['name'],
            'response_time': response.elapsed.total_seconds(),
            'data': response.json(),
            'fallback_used': False
        }
    except Exception as e:
        # Return unhealthy but include fallback payload when possible
        fb = fallback_response_for_module(module, reason='health_check')
        return {
            'status': 'unhealthy',
            'name': module_info['name'],
            'error': str(e),
            'fallback': fb,
            'fallback_used': bool(fb.get('fallback_used', False))
        }


def fallback_response_for_module(module: str, reason: str = 'unavailable', details: Optional[str] = None) -> Dict:
    """Return a small, deterministic fallback payload for a missing/down module."""
    reason = reason or 'unavailable'
    if module == 'ndvi':
        return {
            'success': True,
            'ndvi_value': 0.55,
            'ndvi_history': [],
            'source': 'fallback',
            'reason': reason,
            'fallback_used': True
        }
    if module == 'soil':
        return {
            'success': True,
            'soil_properties': {
                'texture': {'value': 'loam'},
                'moisture': {'value': 45},
                'ph': 6.5
            },
            'source': 'fallback',
            'reason': reason,
            'fallback_used': True
        }
    if module == 'weather':
        return {
            'success': True,
            'temperature': {'current': 28, 'max': 32, 'min': 22},
            'humidity': 65,
            'wind': {'speed': 2.0},
            'solar_radiation': 20,
            'source': 'fallback',
            'reason': reason,
            'fallback_used': True
        }
    if module == 'water':
        return {
            'success': True,
            'schedule': {
                'irrigation': {
                    'gross_irrigation_mm': 0.0,
                    'net_irrigation_mm': 0.0
                }
            },
            'source': 'fallback',
            'reason': reason,
            'fallback_used': True
        }
    # Generic fallback
    return {'success': False, 'error': 'module_unavailable', 'reason': reason, 'details': details, 'fallback_used': True}


# ============================================================================
# HEALTH CHECK ENDPOINTS
# ============================================================================

@app.route('/api/v1/health', methods=['GET'])
@log_request
def health_check():
    """Basic health check"""
    return success_response(
        data={
            'status': 'healthy',
            'service': 'CropEye1 API Gateway',
            'version': '1.0.0',
            'uptime': 'running'
        },
        message="API Gateway is healthy"
    )


@app.route('/api/v1/health/detailed', methods=['GET'])
@log_request
def detailed_health_check():
    """Detailed health check of all modules"""
    
    health_status = {
        'gateway': {
            'status': 'healthy',
            'version': '1.0.0',
            'timestamp': datetime.now().isoformat()
        },
        'modules': {}
    }
    
    # Check each module
    for module_name in MODULES:
        health_status['modules'][module_name] = check_module_health(module_name)
    
    # Determine overall status
    all_healthy = all(
        module['status'] == 'healthy' 
        for module in health_status['modules'].values()
    )
    
    overall_status = 'healthy' if all_healthy else 'degraded'
    
    return success_response(
        data=health_status,
        message=f"System status: {overall_status}",
        metadata={'overall_status': overall_status}
    )


# ============================================================================
# INDIVIDUAL MODULE ENDPOINTS
# ============================================================================

@app.route('/api/v1/ndvi/<float:lat>/<float:lng>', methods=['GET'])
@log_request
@validate_coordinates
def get_ndvi(lat: float, lng: float):
    """Get NDVI analysis for location"""
    
    # Call NDVI module
    result = call_module(
        'ndvi',
        MODULES['ndvi']['endpoints']['calculate'],
        method='POST',
        data={'latitude': lat, 'longitude': lng}
    )
    
    if not result or 'error' in result:
        return error_response(
            "NDVI analysis failed",
            error_details=result.get('message') if result else 'No response',
            status_code=503
        )
    
    return success_response(
        data=result,
        message="NDVI analysis completed",
        metadata={'module': 'ndvi', 'location': {'lat': lat, 'lng': lng}}
    )


@app.route('/api/v1/soil/<float:lat>/<float:lng>', methods=['GET'])
@log_request
@validate_coordinates
def get_soil(lat: float, lng: float):
    """Get soil analysis for location"""
    
    # Call Soil module
    result = call_module(
        'soil',
        MODULES['soil']['endpoints']['analyze'],
        method='POST',
        data={'latitude': lat, 'longitude': lng}
    )
    
    if not result or 'error' in result:
        return error_response(
            "Soil analysis failed",
            error_details=result.get('message') if result else 'No response',
            status_code=503
        )
    
    return success_response(
        data=result,
        message="Soil analysis completed",
        metadata={'module': 'soil', 'location': {'lat': lat, 'lng': lng}}
    )


@app.route('/api/v1/weather/<float:lat>/<float:lng>', methods=['GET'])
@log_request
@validate_coordinates
def get_weather(lat: float, lng: float):
    """Get weather analysis for location"""
    
    # Call Weather module
    result = call_module(
        'weather',
        MODULES['weather']['endpoints']['current'],
        method='POST',
        data={'latitude': lat, 'longitude': lng}
    )
    
    if not result or 'error' in result:
        return error_response(
            "Weather analysis failed",
            error_details=result.get('message') if result else 'No response',
            status_code=503
        )
    
    return success_response(
        data=result,
        message="Weather analysis completed",
        metadata={'module': 'weather', 'location': {'lat': lat, 'lng': lng}}
    )


@app.route('/api/v1/water/<float:lat>/<float:lng>', methods=['GET'])
@log_request
@validate_coordinates
def get_water(lat: float, lng: float):
    """Get integrated water/irrigation analysis for location"""
    # Call Water module (integrated)
    result = call_module(
        'water',
        MODULES['water']['endpoints']['integrated'],
        method='POST',
        data={'latitude': lat, 'longitude': lng}
    )

    if not result or 'error' in result:
        return error_response(
            "Water analysis failed",
            error_details=result.get('message') if result else 'No response',
            status_code=503
        )

    return success_response(
        data=result,
        message="Water analysis completed",
        metadata={'module': 'water', 'location': {'lat': lat, 'lng': lng}}
    )


# ============================================================================
# COMPREHENSIVE ANALYSIS ENDPOINT
# ============================================================================

@app.route('/api/v1/analysis/comprehensive', methods=['POST'])
@log_request
@validate_coordinates
def comprehensive_analysis(lat: Optional[float] = None, lng: Optional[float] = None):
    """
    Get comprehensive analysis from all modules
    
    Request body:
    {
        "latitude": 30.3398,
        "longitude": 76.3869,
        "include_ndvi": true (optional),
        "include_soil": true (optional),
        "include_weather": true (optional),
        "weather_forecast_hours": 48 (optional)
    }
    """
    
    data = request.get_json(silent=True) or {}
    lat = lat or data.get('latitude')
    lng = lng or data.get('longitude')
    
    # Options
    include_ndvi = data.get('include_ndvi', True)
    include_soil = data.get('include_soil', True)
    include_weather = data.get('include_weather', True)
    
    logger.info(f"🌍 Comprehensive analysis for ({lat}, {lng})")
    
    results = {
        'location': {'latitude': lat, 'longitude': lng},
        'analysis_timestamp': datetime.now().isoformat(),
        'modules_requested': [],
        'modules_completed': [],
        'modules_failed': []
    }
    
    # NDVI Analysis
    if include_ndvi:
        results['modules_requested'].append('ndvi')
        logger.info("📊 Running NDVI analysis...")
        
        ndvi_result = call_module(
            'ndvi',
            MODULES['ndvi']['endpoints']['calculate'],
            method='POST',
            data={'latitude': lat, 'longitude': lng}
        )
        
        if ndvi_result and 'error' not in ndvi_result:
            results['ndvi'] = ndvi_result
            results['modules_completed'].append('ndvi')
            logger.info("✅ NDVI analysis completed")
        else:
            results['modules_failed'].append('ndvi')
            logger.warning("⚠️ NDVI analysis failed")
    
    # Soil Analysis
    if include_soil:
        results['modules_requested'].append('soil')
        logger.info("🌱 Running Soil analysis...")
        
        soil_result = call_module(
            'soil',
            MODULES['soil']['endpoints']['analyze'],
            method='POST',
            data={'latitude': lat, 'longitude': lng}
        )
        
        if soil_result and 'error' not in soil_result:
            results['soil'] = soil_result
            results['modules_completed'].append('soil')
            logger.info("✅ Soil analysis completed")
        else:
            results['modules_failed'].append('soil')
            logger.warning("⚠️ Soil analysis failed")
    
    # Weather Analysis
    if include_weather:
        results['modules_requested'].append('weather')
        logger.info("🌤️ Running Weather analysis...")
        
        weather_result = call_module(
            'weather',
            MODULES['weather']['endpoints']['current'],
            method='POST',
            data={'latitude': lat, 'longitude': lng}
        )
        
        if weather_result and 'error' not in weather_result:
            results['weather'] = weather_result
            results['modules_completed'].append('weather')
            logger.info("✅ Weather analysis completed")
        else:
            results['modules_failed'].append('weather')
            logger.warning("⚠️ Weather analysis failed")

    # Water Analysis (integrated irrigation) - optional
    include_water = data.get('include_water', False)
    if include_water:
        results['modules_requested'].append('water')
        logger.info("💧 Running Water (integrated irrigation) analysis...")

        water_result = call_module(
            'water',
            MODULES['water']['endpoints']['integrated'],
            method='POST',
            data={'latitude': lat, 'longitude': lng}
        )

        if water_result and 'error' not in water_result:
            results['water'] = water_result
            results['modules_completed'].append('water')
            logger.info("✅ Water analysis completed")
        else:
            results['modules_failed'].append('water')
            logger.warning("⚠️ Water analysis failed")
    
    # Generate integrated recommendations
    if len(results['modules_completed']) > 0:
        results['recommendations'] = generate_recommendations(results)
    
    # Success if at least one module completed
    if len(results['modules_completed']) > 0:
        return success_response(
            data=results,
            message=f"Comprehensive analysis completed ({len(results['modules_completed'])}/{len(results['modules_requested'])} modules)",
            metadata={
                'modules_completed': len(results['modules_completed']),
                'modules_failed': len(results['modules_failed'])
            }
        )
    else:
        return error_response(
            "All modules failed to respond",
            error_details="No data could be retrieved",
            status_code=503
        )


# ============================================================================
# BATCH PROCESSING ENDPOINT
# ============================================================================

@app.route('/api/v1/batch/analyze', methods=['POST'])
@log_request
def batch_analyze():
    """
    Batch analysis for multiple locations
    
    Request body:
    {
        "locations": [
            {"latitude": 30.3398, "longitude": 76.3869, "name": "Location 1"},
            {"latitude": 28.6139, "longitude": 77.2090, "name": "Location 2"}
        ],
        "include_ndvi": true,
        "include_soil": true,
        "include_weather": true
    }
    """
    
    data = request.get_json(silent=True) or {}
    locations = data.get('locations', [])
    
    if not locations:
        return error_response(
            "No locations provided",
            error_details="Please provide an array of locations",
            status_code=400
        )
    
    if len(locations) > 50:
        return error_response(
            "Too many locations",
            error_details="Maximum 50 locations per batch request",
            status_code=400
        )
    
    logger.info(f"🔄 Batch analysis for {len(locations)} locations")
    
    results = {
        'batch_id': f"batch_{int(time.time())}",
        'total_locations': len(locations),
        'completed': 0,
        'failed': 0,
        'results': []
    }
    
    for location in locations:
        lat = location.get('latitude')
        lng = location.get('longitude')
        name = location.get('name', f"Location ({lat}, {lng})")
        
        try:
            # Validate coordinates
            if not lat or not lng:
                results['failed'] += 1
                results['results'].append({
                    'location': name,
                    'status': 'failed',
                    'error': 'Missing coordinates'
                })
                continue
            
            # Run comprehensive analysis
            analysis = {}
            
            if data.get('include_ndvi', True):
                ndvi_result = call_module('ndvi', MODULES['ndvi']['endpoints']['calculate'],
                                         method='POST', data={'latitude': lat, 'longitude': lng})
                if ndvi_result and 'error' not in ndvi_result:
                    analysis['ndvi'] = ndvi_result
            
            if data.get('include_soil', True):
                soil_result = call_module('soil', MODULES['soil']['endpoints']['analyze'],
                                         method='POST', data={'latitude': lat, 'longitude': lng})
                if soil_result and 'error' not in soil_result:
                    analysis['soil'] = soil_result
            
            if data.get('include_weather', True):
                weather_result = call_module('weather', MODULES['weather']['endpoints']['current'],
                                            method='POST', data={'latitude': lat, 'longitude': lng})
                if weather_result and 'error' not in weather_result:
                    analysis['weather'] = weather_result
            
            results['completed'] += 1
            results['results'].append({
                'location': name,
                'coordinates': {'latitude': lat, 'longitude': lng},
                'status': 'completed',
                'data': analysis
            })
            
        except Exception as e:
            results['failed'] += 1
            results['results'].append({
                'location': name,
                'status': 'failed',
                'error': str(e)
            })
    
    return success_response(
        data=results,
        message=f"Batch analysis completed ({results['completed']}/{results['total_locations']} successful)",
        metadata={
            'batch_id': results['batch_id'],
            'success_rate': f"{(results['completed']/results['total_locations']*100):.1f}%"
        }
    )


# ============================================================================
# RECOMMENDATION ENGINE
# ============================================================================

def generate_recommendations(analysis_data: Dict) -> List[Dict]:
    """Generate integrated recommendations from all modules"""
    
    recommendations = []
    
    # Extract data from modules
    ndvi_data = analysis_data.get('ndvi', {})
    soil_data = analysis_data.get('soil', {})
    weather_data = analysis_data.get('weather', {})
    
    # NDVI-based recommendations
    if ndvi_data:
        ndvi_value = ndvi_data.get('ndvi_value', 0)
        
        if ndvi_value < 0.3:
            recommendations.append({
                'category': 'vegetation',
                'priority': 'high',
                'title': 'Low Vegetation Health',
                'message': 'NDVI indicates poor vegetation. Consider irrigation and nutrient management.',
                'source': 'ndvi'
            })
        elif ndvi_value > 0.7:
            recommendations.append({
                'category': 'vegetation',
                'priority': 'low',
                'title': 'Healthy Vegetation',
                'message': 'Excellent vegetation health detected. Maintain current practices.',
                'source': 'ndvi'
            })
    
    # Soil-based recommendations
    if soil_data:
        soil_props = soil_data.get('soil_properties', {})
        moisture = soil_props.get('moisture', {}).get('value', 50)
        
        if moisture < 20:
            recommendations.append({
                'category': 'irrigation',
                'priority': 'high',
                'title': 'Low Soil Moisture',
                'message': 'Soil moisture is critically low. Immediate irrigation recommended.',
                'source': 'soil'
            })
    
    # Weather-based recommendations
    if weather_data:
        temp = weather_data.get('temperature', {}).get('current', 25)
        
        if temp > 35:
            recommendations.append({
                'category': 'heat_stress',
                'priority': 'high',
                'title': 'High Temperature Alert',
                'message': 'Temperatures are high. Increase irrigation and monitor crops closely.',
                'source': 'weather'
            })
    
    # If no specific recommendations, add general one
    if not recommendations:
        recommendations.append({
            'category': 'general',
            'priority': 'low',
            'title': 'Conditions Normal',
            'message': 'All parameters are within normal range. Continue regular monitoring.',
            'source': 'integrated'
        })
    
    return recommendations


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return error_response(
        "Endpoint not found",
        error_details=f"The requested endpoint does not exist: {request.path}",
        status_code=404
    )


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal error: {error}")
    logger.error(traceback.format_exc())
    return error_response(
        "Internal server error",
        error_details="An unexpected error occurred",
        status_code=500
    )


@app.errorhandler(Exception)
def handle_exception(error):
    """Handle all unhandled exceptions"""
    logger.error(f"Unhandled exception: {error}")
    logger.error(traceback.format_exc())
    return error_response(
        "An error occurred",
        error_details=str(error),
        status_code=500
    )


# ============================================================================
# ROOT ENDPOINT
# ============================================================================

@app.route('/', methods=['GET'])
def root():
    """Root endpoint with API information"""
    return jsonify({
        'service': 'CropEye1 API Gateway',
        'version': '1.0.0',
        'description': 'Unified API Gateway for Agricultural Analysis',
        'documentation': '/api/v1/docs',
        'health': '/api/v1/health',
        'endpoints': {
            'health': '/api/v1/health',
            'detailed_health': '/api/v1/health/detailed',
            'comprehensive': '/api/v1/analysis/comprehensive',
            'ndvi': '/api/v1/ndvi/<lat>/<lng>',
            'soil': '/api/v1/soil/<lat>/<lng>',
            'weather': '/api/v1/weather/<lat>/<lng>',
            'water': '/api/v1/water/<lat>/<lng>',
            'batch': '/api/v1/batch/analyze'
        }
    })


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == '__main__':
    logger.info("=" * 80)
    logger.info("🚀 CROPEYE1 API GATEWAY STARTING")
    logger.info("=" * 80)
    logger.info("")
    logger.info("📡 Backend Modules:")
    for module_name, module_info in MODULES.items():
        logger.info(f"   • {module_info['name']}: {module_info['url']}")
    logger.info("")
    logger.info("🌐 API Endpoints:")
    logger.info("   • Root:          http://localhost:5000/")
    logger.info("   • Health:        http://localhost:5000/api/v1/health")
    logger.info("   • Comprehensive: POST http://localhost:5000/api/v1/analysis/comprehensive")
    logger.info("   • NDVI:          GET  http://localhost:5000/api/v1/ndvi/<lat>/<lng>")
    logger.info("   • Soil:          GET  http://localhost:5000/api/v1/soil/<lat>/<lng>")
    logger.info("   • Weather:       GET  http://localhost:5000/api/v1/weather/<lat>/<lng>")
    logger.info("   • Batch:         POST http://localhost:5000/api/v1/batch/analyze")
    logger.info("")
    logger.info("=" * 80)
    logger.info("")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True
    )
