#!/usr/bin/env python3
"""
Soil Analysis Flask Backend - FINAL VERSION
Complete integration with Copernicus satellite data + GPS/Manual coordinate support
Location: D:\\CropEye1\\backend\\GIS\\Soil Analysis\\soil_flask_backend.py

Features:
- Copernicus satellite data integration
- GPS and manual coordinate support
- Enhanced unknown location handling
- NDVI-Soil correlation analysis
- Comprehensive soil recommendations
- Multi-location comparison
- Real-time health monitoring

Author: CropEye1 System
Date: October 18, 2025
"""

from dotenv import load_dotenv
load_dotenv(r"D:/CropEye1/backend/.env")

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
import time
import logging
from datetime import datetime
import json

# Import local modules
try:
    from env_credentials import env_creds
    from soil_data_collector import SoilDataCollector
    from ndvi_integration import ndvi_integration
except ImportError as e:
    logging.error(f"Failed to import modules: {e}")
    sys.exit(1)

# Flask app initialization
app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Set environment variables from root backend .env
env_creds.set_environment_variables()

# Initialize soil data collector with Copernicus integration
try:
    soil_collector = SoilDataCollector()
    logger.info("✅ Soil Data Collector initialized successfully")
except Exception as e:
    logger.error(f"❌ Failed to initialize Soil Data Collector: {e}")
    soil_collector = None


# ============================================================
# HEALTH CHECK ENDPOINT
# ============================================================
@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for system status
    Returns detailed status of all integrations
    """
    try:
        health_status = {
            'status': 'healthy',
            'service': 'Soil Analysis Backend with Copernicus Integration',
            'timestamp': datetime.now().isoformat(),
            'version': '2.0.0',
            'modules': {
                'soil_data_collector': 'active' if soil_collector else 'unavailable',
                'copernicus_integration': 'active' if (soil_collector and soil_collector.copernicus_downloader) else 'unavailable',
                'ndvi_integration': 'active' if (ndvi_integration and ndvi_integration.is_available()) else 'fallback',
                'soilgrids_api': 'available'
            },
            'data_sources': {
                'known_agricultural_locations': len(soil_collector.known_agricultural_locations) if soil_collector else 0,
                'copernicus_satellite': 'primary' if (soil_collector and soil_collector.copernicus_downloader) else 'unavailable',
                'soilgrids_250m': 'fallback',
                'regional_modeling': 'fallback'
            },
            'credentials': {
                'copernicus_username': bool(os.getenv('COPERNICUS_USERNAME')),
                'copernicus_password': bool(os.getenv('COPERNICUS_PASSWORD')),
                'copernicus_client_id': bool(os.getenv('COPERNICUS_CLIENT_ID'))
            },
            'features': {
                'unknown_location_support': 'enabled',
                'gps_coordinates': 'supported',
                'manual_coordinates': 'supported',
                'geographic_context': 'enabled',
                'climate_adjustment': 'enabled',
                'ndvi_correlation': 'enabled'
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
# MAIN SOIL ANALYSIS ENDPOINT
# ============================================================
@app.route('/api/soil/analyze', methods=['POST', 'OPTIONS'])
def analyze_soil():
    """
    Main soil analysis endpoint
    
    Expected JSON payload:
    {
        "latitude": 30.3398,
        "longitude": 76.3869,
        "coordinate_source": "gps",  # or "manual"
        "include_ndvi": true,
        "analysis_depth": "comprehensive"
    }
    
    Returns comprehensive soil analysis with satellite data
    """
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        return '', 200
    
    start_time = time.time()
    
    try:
        # Get request data
        data = request.get_json(force=True)
        
        # Validate required fields
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        if 'latitude' not in data or 'longitude' not in data:
            return jsonify({'error': 'Latitude and longitude required'}), 400
        
        # Extract parameters
        latitude = float(data['latitude'])
        longitude = float(data['longitude'])
        coordinate_source = data.get('coordinate_source', 'unknown')  # 'gps', 'manual', or 'unknown'
        include_ndvi = data.get('include_ndvi', True)
        analysis_depth = data.get('analysis_depth', 'comprehensive')
        
        # Validate coordinates
        if not (-90 <= latitude <= 90):
            return jsonify({'error': 'Invalid latitude', 'message': 'Latitude must be between -90 and 90'}), 400
        
        if not (-180 <= longitude <= 180):
            return jsonify({'error': 'Invalid longitude', 'message': 'Longitude must be between -180 and 180'}), 400
        
        # Check if collector is available
        if not soil_collector:
            return jsonify({'error': 'Soil collector not initialized'}), 500
        
        logger.info(f"🛰️ Soil analysis request: ({latitude}, {longitude}) [Source: {coordinate_source}]")
        
        # Perform soil analysis with new enhanced collector
        soil_result = soil_collector.get_soil_data(
            latitude=latitude,
            longitude=longitude,
            coordinate_source=coordinate_source,
            include_ndvi=include_ndvi
        )
        
        # Check for errors in result
        if 'error' in soil_result:
            return jsonify(soil_result), 400
        
        # Add API metadata
        soil_result['api_info'] = {
            'processing_time_sec': round(time.time() - start_time, 2),
            'server_timestamp': datetime.now().isoformat(),
            'api_version': '2.0.0',
            'coordinate_source': coordinate_source,
            'analysis_depth': analysis_depth
        }
        
        # Add management recommendations if comprehensive analysis
        if analysis_depth == 'comprehensive':
            soil_result['management_recommendations'] = _generate_management_recommendations(soil_result)
            soil_result['crop_suitability'] = _assess_crop_suitability(soil_result)
        
        logger.info(f"✅ Soil analysis complete: {soil_result.get('confidence_score', 0):.2f} confidence, {time.time() - start_time:.2f}s")
        
        return jsonify(soil_result), 200
        
    except ValueError as e:
        logger.error(f"Invalid input: {e}")
        return jsonify({
            'error': 'Invalid coordinates',
            'details': str(e),
            'message': 'Coordinates must be numeric values'
        }), 400
        
    except Exception as e:
        logger.error(f"❌ Soil analysis failed: {e}")
        return jsonify({
            'error': 'Soil analysis failed',
            'details': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500


# ============================================================
# SOIL COMPARISON ENDPOINT
# ============================================================
@app.route('/api/soil/compare', methods=['POST'])
def compare_soil_locations():
    """
    Compare soil properties between multiple locations
    
    Expected JSON payload:
    {
        "locations": [
            {"name": "Punjab Field", "latitude": 30.3398, "longitude": 76.3869},
            {"name": "Maharashtra Field", "latitude": 18.15, "longitude": 74.5777}
        ],
        "properties": ["ph", "nitrogen", "organic_carbon"],
        "include_ndvi": true
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'locations' not in data:
            return jsonify({'error': 'Locations array required'}), 400
        
        locations = data['locations']
        properties = data.get('properties', ['ph', 'organic_carbon', 'nitrogen', 'phosphorus', 'potassium'])
        include_ndvi = data.get('include_ndvi', True)
        
        if len(locations) < 2:
            return jsonify({'error': 'At least 2 locations required for comparison'}), 400
        
        if not soil_collector:
            return jsonify({'error': 'Soil collector not initialized'}), 500
        
        logger.info(f"🔍 Comparing soil at {len(locations)} locations")
        
        # Analyze each location
        comparison_results = {
            'comparison_date': datetime.now().isoformat(),
            'locations_analyzed': [],
            'property_comparison': {},
            'ndvi_comparison': {} if include_ndvi else None,
            'recommendations': []
        }
        
        soil_data = {}
        
        for location in locations:
            if 'latitude' not in location or 'longitude' not in location:
                continue
            
            lat = float(location['latitude'])
            lng = float(location['longitude'])
            name = location.get('name', f"Location ({lat:.4f}, {lng:.4f})")
            
            # Get soil data for this location
            result = soil_collector.get_soil_data(
                latitude=lat,
                longitude=lng,
                coordinate_source='manual',
                include_ndvi=include_ndvi
            )
            
            if result and 'soil_properties' in result:
                soil_data[name] = result
                
                location_summary = {
                    'name': name,
                    'coordinates': {'latitude': lat, 'longitude': lng},
                    'location_type': result['coordinates'].get('location_type', 'unknown'),
                    'soil_type': result.get('location_info', {}).get('soil_type', 'Unknown'),
                    'confidence': result.get('confidence_score', 0),
                    'data_sources': result.get('data_sources', [])
                }
                
                # Add geographic context if unknown location
                if 'geographic_context' in result:
                    location_summary['region'] = result['geographic_context'].get('region', 'Unknown')
                    location_summary['climate_zone'] = result['geographic_context'].get('climate_zone', 'Unknown')
                
                # Add NDVI info if available
                if include_ndvi and result.get('ndvi_correlation'):
                    ndvi_data = result['ndvi_correlation']
                    location_summary['ndvi_value'] = ndvi_data.get('ndvi_value')
                    location_summary['vegetation_health'] = ndvi_data.get('health_analysis', {}).get('category')
                
                comparison_results['locations_analyzed'].append(location_summary)
        
        # Compare properties across locations
        for prop in properties:
            if prop in ['texture']:  # Skip non-numeric properties
                continue
            
            prop_comparison = {
                'property': prop,
                'values': {},
                'statistics': {}
            }
            
            values = []
            for name, data in soil_data.items():
                if prop in data.get('soil_properties', {}):
                    value = data['soil_properties'][prop].get('value')
                    if value is not None:
                        prop_comparison['values'][name] = {
                            'value': value,
                            'unit': data['soil_properties'][prop].get('unit', ''),
                            'classification': data['soil_properties'][prop].get('classification', '')
                        }
                        values.append(value)
            
            if len(values) > 1:
                prop_comparison['statistics'] = {
                    'min': min(values),
                    'max': max(values),
                    'mean': round(sum(values) / len(values), 2),
                    'range': round(max(values) - min(values), 2),
                    'variation': 'High' if (max(values) - min(values)) / (sum(values) / len(values)) > 0.5 else 'Low'
                }
            
            comparison_results['property_comparison'][prop] = prop_comparison
        
        # NDVI comparison if requested
        if include_ndvi:
            ndvi_values = []
            ndvi_comparison = {'values': {}, 'statistics': {}}
            
            for name, data in soil_data.items():
                ndvi_corr = data.get('ndvi_correlation')
                if ndvi_corr and ndvi_corr.get('ndvi_value') is not None:
                    ndvi_val = ndvi_corr['ndvi_value']
                    ndvi_values.append(ndvi_val)
                    ndvi_comparison['values'][name] = {
                        'ndvi_value': ndvi_val,
                        'vegetation_health': ndvi_corr.get('health_analysis', {}).get('category', 'Unknown'),
                        'data_source': ndvi_corr.get('ndvi_data_source', 'Unknown')
                    }
            
            if len(ndvi_values) > 1:
                ndvi_comparison['statistics'] = {
                    'min': round(min(ndvi_values), 3),
                    'max': round(max(ndvi_values), 3),
                    'mean': round(sum(ndvi_values) / len(ndvi_values), 3),
                    'range': round(max(ndvi_values) - min(ndvi_values), 3)
                }
            
            comparison_results['ndvi_comparison'] = ndvi_comparison
        
        # Generate comparison recommendations
        comparison_results['recommendations'] = _generate_comparison_recommendations(
            comparison_results, soil_data
        )
        
        logger.info(f"✅ Soil comparison complete for {len(soil_data)} locations")
        
        return jsonify(comparison_results), 200
        
    except Exception as e:
        logger.error(f"❌ Soil comparison error: {e}")
        return jsonify({
            'error': 'Soil comparison failed',
            'details': str(e)
        }), 500


# ============================================================
# RECOMMENDATIONS ENDPOINT
# ============================================================
@app.route('/api/soil/recommendations/<float:lat>/<float:lng>', methods=['GET'])
def get_soil_recommendations(lat, lng):
    """
    Get detailed soil management recommendations for specific coordinates
    """
    try:
        if not soil_collector:
            return jsonify({'error': 'Soil collector not initialized'}), 500
        
        logger.info(f"🌾 Getting recommendations for {lat}, {lng}")
        
        # Get soil data with NDVI integration
        soil_result = soil_collector.get_soil_data(
            latitude=lat,
            longitude=lng,
            coordinate_source='unknown',
            include_ndvi=True
        )
        
        if 'error' in soil_result:
            return jsonify(soil_result), 400
        
        # Generate comprehensive recommendations
        recommendations = {
            'coordinates': {'latitude': lat, 'longitude': lng},
            'location_type': soil_result['coordinates'].get('location_type', 'unknown'),
            'analysis_date': datetime.now().isoformat(),
            'soil_health_score': _calculate_soil_health_score(soil_result),
            'immediate_actions': [],
            'fertilizer_recommendations': {},
            'irrigation_advice': {},
            'seasonal_recommendations': {},
            'long_term_improvements': []
        }
        
        # Add geographic context if unknown location
        if 'geographic_context' in soil_result:
            recommendations['location_context'] = {
                'region': soil_result['geographic_context'].get('region'),
                'climate_zone': soil_result['geographic_context'].get('climate_zone'),
                'agricultural_potential': soil_result['geographic_context'].get('agricultural_potential')
            }
        
        # Generate specific recommendations based on soil properties
        if 'soil_properties' in soil_result:
            props = soil_result['soil_properties']
            
            # pH recommendations
            if 'ph' in props:
                ph_value = props['ph']['value']
                if ph_value < 6.0:
                    recommendations['immediate_actions'].append({
                        'action': 'Lime Application',
                        'reason': f'Soil pH is acidic ({ph_value})',
                        'recommendation': 'Apply agricultural lime at 2-4 tons/hectare',
                        'timing': 'Before next planting season',
                        'priority': 'High'
                    })
                elif ph_value > 8.0:
                    recommendations['immediate_actions'].append({
                        'action': 'Sulfur Application',
                        'reason': f'Soil pH is alkaline ({ph_value})',
                        'recommendation': 'Apply sulfur at 500-1000 kg/hectare',
                        'timing': '2-3 months before planting',
                        'priority': 'High'
                    })
            
            # Nutrient recommendations
            nutrients = ['nitrogen', 'phosphorus', 'potassium']
            for nutrient in nutrients:
                if nutrient in props:
                    n_value = props[nutrient]['value']
                    n_class = props[nutrient]['classification']
                    
                    if 'Low' in n_class:
                        if nutrient == 'nitrogen':
                            recommendations['fertilizer_recommendations'][nutrient] = {
                                'status': 'Deficient',
                                'current_level': f"{n_value} ppm",
                                'recommended_application': '120-150 kg N/hectare',
                                'sources': ['Urea', 'Ammonium Sulfate', 'Compost'],
                                'timing': 'Split application - 50% at sowing, 25% at tillering, 25% at flowering'
                            }
                        elif nutrient == 'phosphorus':
                            recommendations['fertilizer_recommendations'][nutrient] = {
                                'status': 'Deficient',
                                'current_level': f"{n_value} ppm",
                                'recommended_application': '60-80 kg P2O5/hectare',
                                'sources': ['DAP', 'SSP', 'Rock Phosphate'],
                                'timing': 'Full dose at sowing'
                            }
                        elif nutrient == 'potassium':
                            recommendations['fertilizer_recommendations'][nutrient] = {
                                'status': 'Deficient',
                                'current_level': f"{n_value} ppm",
                                'recommended_application': '80-100 kg K2O/hectare',
                                'sources': ['MOP', 'SOP'],
                                'timing': '50% at sowing, 50% at active growth'
                            }
        
        # NDVI-based recommendations
        if soil_result.get('ndvi_correlation'):
            ndvi_data = soil_result['ndvi_correlation']
            recommendations['ndvi_insights'] = {
                'ndvi_value': ndvi_data.get('ndvi_value'),
                'vegetation_health': ndvi_data.get('health_analysis', {}).get('category'),
                'soil_vegetation_correlation': ndvi_data.get('soil_ndvi_correlation', {})
            }
            
            if ndvi_data.get('ndvi_value', 0) < 0.4:
                recommendations['immediate_actions'].append({
                    'action': 'Vegetation Health Assessment',
                    'reason': f'Low NDVI value ({ndvi_data.get("ndvi_value", 0):.3f})',
                    'recommendation': 'Investigate pest/disease issues and nutrient deficiencies',
                    'timing': 'Immediately',
                    'priority': 'High'
                })
        
        return jsonify(recommendations), 200
        
    except Exception as e:
        logger.error(f"❌ Recommendations error: {e}")
        return jsonify({
            'error': 'Recommendations generation failed',
            'details': str(e)
        }), 500


# ============================================================
# KNOWN LOCATIONS ENDPOINT
# ============================================================
@app.route('/api/soil/known-locations', methods=['GET'])
def get_known_locations():
    """Get list of known agricultural locations with verified data"""
    try:
        if not soil_collector:
            return jsonify({'error': 'Soil collector not initialized'}), 500
        
        locations = []
        for coord_key, data in soil_collector.known_agricultural_locations.items():
            lat_str, lng_str = coord_key.split(',')
            locations.append({
                'name': data['location_name'],
                'coordinates': {
                    'latitude': float(lat_str),
                    'longitude': float(lng_str)
                },
                'soil_type': data['soil_type'],
                'confidence': data['confidence'],
                'sample_date': data['sample_date'],
                'data_source': data['data_source'],
                'key_properties': {
                    'pH': data['ph'],
                    'organic_carbon': data['organic_carbon_percent'],
                    'texture': data['texture']
                }
            })
        
        return jsonify({
            'known_locations': locations,
            'total_locations': len(locations),
            'message': 'Verified agricultural survey data available'
        }), 200
        
    except Exception as e:
        logger.error(f"❌ Known locations error: {e}")
        return jsonify({
            'error': 'Failed to retrieve known locations',
            'details': str(e)
        }), 500


# ============================================================
# INTEGRATION STATUS ENDPOINT
# ============================================================
@app.route('/api/soil/integration-status', methods=['GET'])
def get_integration_status():
    """Get detailed integration status"""
    try:
        status = {
            'timestamp': datetime.now().isoformat(),
            'soil_module': 'active' if soil_collector else 'unavailable',
            'copernicus_integration': {
                'available': bool(soil_collector and soil_collector.copernicus_downloader),
                'status': 'primary' if (soil_collector and soil_collector.copernicus_downloader) else 'unavailable'
            },
            'ndvi_integration': {
                'available': ndvi_integration.is_available() if ndvi_integration else False,
                'status': ndvi_integration.get_status() if ndvi_integration else {}
            },
            'credentials': {
                'copernicus_configured': bool(os.getenv('COPERNICUS_USERNAME') and os.getenv('COPERNICUS_PASSWORD')),
                'client_credentials': bool(os.getenv('COPERNICUS_CLIENT_ID') and os.getenv('COPERNICUS_CLIENT_SECRET'))
            },
            'data_sources': {
                'known_locations': len(soil_collector.known_agricultural_locations) if soil_collector else 0,
                'soilgrids_api': 'fallback',
                'regional_modeling': 'fallback'
            }
        }
        
        return jsonify(status), 200
        
    except Exception as e:
        logger.error(f"❌ Integration status error: {e}")
        return jsonify({
            'error': 'Status check failed',
            'details': str(e)
        }), 500


# ============================================================
# DEBUG ENDPOINT
# ============================================================
@app.route('/api/soil/debug', methods=['GET'])
def debug_info():
    """Debug information for troubleshooting"""
    try:
        debug_data = {
            'system_info': {
                'working_directory': os.getcwd(),
                'python_version': sys.version,
                'timestamp': datetime.now().isoformat()
            },
            'environment': {
                'COPERNICUS_USERNAME': bool(os.getenv('COPERNICUS_USERNAME')),
                'COPERNICUS_PASSWORD': bool(os.getenv('COPERNICUS_PASSWORD')),
                'COPERNICUS_CLIENT_ID': bool(os.getenv('COPERNICUS_CLIENT_ID')),
                'COPERNICUS_CLIENT_SECRET': bool(os.getenv('COPERNICUS_CLIENT_SECRET'))
            },
            'modules': {
                'soil_collector': soil_collector is not None,
                'copernicus_downloader': soil_collector.copernicus_downloader is not None if soil_collector else False,
                'ndvi_integration': ndvi_integration.is_available() if ndvi_integration else False
            },
            'known_locations': list(soil_collector.known_agricultural_locations.keys()) if soil_collector else [],
            'test_coordinates': [
                {'name': 'Punjab Wheat', 'lat': 30.3398, 'lng': 76.3869},
                {'name': 'Maharashtra Sugarcane', 'lat': 18.15, 'lng': 74.5777},
                {'name': 'California Central Valley', 'lat': 36.7783, 'lng': -119.4179},
                {'name': 'Iowa Corn Farm', 'lat': 41.5868, 'lng': -93.6250},
                {'name': 'Karnataka Coffee', 'lat': 13.3409, 'lng': 75.7131}
            ]
        }
        
        return jsonify(debug_data), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Debug info failed',
            'details': str(e)
        }), 500


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def _generate_management_recommendations(soil_result):
    """Generate basic soil management recommendations"""
    recommendations = {
        'immediate': [],
        'seasonal': [],
        'long_term': []
    }
    
    if not soil_result.get('soil_properties'):
        return recommendations
    
    props = soil_result['soil_properties']
    
    # pH-based recommendations
    if 'ph' in props:
        ph_val = props['ph']['value']
        ph_class = props['ph']['classification']
        
        if 'Acidic' in ph_class:
            recommendations['immediate'].append(f"Apply lime to raise pH from {ph_val} to 6.5-7.0 range")
        elif 'Alkaline' in ph_class:
            recommendations['immediate'].append(f"Apply sulfur to lower pH from {ph_val} to 6.5-7.0 range")
    
    # Organic matter recommendations
    if 'organic_carbon' in props:
        oc_class = props['organic_carbon']['classification']
        
        if 'Low' in oc_class:
            recommendations['long_term'].append("Increase organic matter through composting or cover crops")
    
    return recommendations


def _assess_crop_suitability(soil_result):
    """Assess crop suitability based on soil properties"""
    suitability = {
        'highly_suitable': [],
        'moderately_suitable': [],
        'not_suitable': []
    }
    
    if not soil_result.get('soil_properties'):
        return suitability
    
    props = soil_result['soil_properties']
    ph_val = props.get('ph', {}).get('value', 7.0)
    texture = props.get('texture', {}).get('value', 'Loam')
    
    # Simple crop suitability logic
    if 5.5 <= ph_val <= 7.0 and texture in ['Clay', 'Silty Clay', 'Clay Loam']:
        suitability['highly_suitable'].append('Rice')
    
    if 6.0 <= ph_val <= 7.5 and texture in ['Loam', 'Clay Loam', 'Sandy Loam']:
        suitability['highly_suitable'].append('Wheat')
    
    if 6.0 <= ph_val <= 7.0 and texture in ['Loam', 'Silty Clay Loam']:
        suitability['highly_suitable'].append('Corn/Maize')
    
    return suitability


def _generate_comparison_recommendations(comparison_results, soil_data):
    """Generate recommendations based on soil comparison"""
    recommendations = []
    
    # Check for large variations in key properties
    for prop, comparison in comparison_results.get('property_comparison', {}).items():
        stats = comparison.get('statistics', {})
        if stats.get('variation') == 'High':
            recommendations.append(f"High variation in {prop} - consider site-specific management")
    
    # NDVI-based comparison recommendations
    if comparison_results.get('ndvi_comparison'):
        ndvi_stats = comparison_results['ndvi_comparison'].get('statistics', {})
        if ndvi_stats.get('range', 0) > 0.3:
            recommendations.append("Significant NDVI variation - investigate vegetation health differences")
    
    return recommendations


def _calculate_soil_health_score(soil_result):
    """Calculate overall soil health score (0-100)"""
    if not soil_result.get('soil_properties'):
        return 50
    
    score = 0
    factors = 0
    props = soil_result['soil_properties']
    
    # pH score (optimal 6.0-7.5)
    if 'ph' in props:
        ph_val = props['ph']['value']
        if 6.0 <= ph_val <= 7.5:
            score += 25
        elif 5.5 <= ph_val <= 8.0:
            score += 20
        elif 5.0 <= ph_val <= 8.5:
            score += 15
        else:
            score += 5
        factors += 1
    
    # Organic carbon score
    if 'organic_carbon' in props:
        oc_val = props['organic_carbon']['value']
        if oc_val >= 3.0:
            score += 25
        elif oc_val >= 2.0:
            score += 20
        elif oc_val >= 1.0:
            score += 15
        else:
            score += 5
        factors += 1
    
    # Nutrient scores
    for nutrient in ['nitrogen', 'phosphorus', 'potassium']:
        if nutrient in props:
            classification = props[nutrient].get('classification', '')
            if 'High' in classification:
                score += 15
            elif 'Medium' in classification:
                score += 12
            elif 'Low' in classification:
                score += 8
            else:
                score += 4
            factors += 1
    
    return min(100, score) if factors > 0 else 50


# ============================================================
# MAIN ENTRY POINT
# ============================================================

if __name__ == '__main__':
    # ASCII-only startup messages to avoid Windows console encoding errors
    print('=' * 80)
    print('SOIL ANALYSIS BACKEND - FINAL VERSION')
    print('=' * 80)
    print('\nAPI Endpoints:')
    print('   POST   /api/soil/analyze              - Comprehensive soil analysis')
    print('   POST   /api/soil/compare              - Compare multiple locations')
    print('   GET    /api/soil/recommendations/<lat>/<lng> - Detailed recommendations')
    print('   GET    /api/soil/known-locations      - Known agricultural sites')
    print('   GET    /api/soil/integration-status   - Integration status check')
    print('   GET    /api/health                    - Health check')
    print('   GET    /api/soil/debug                - Debug information')
    print('\nKey Features:')
    print('   - Copernicus satellite data integration')
    print('   - GPS and manual coordinate support')
    print('   - Enhanced unknown location handling')
    print('   - Geographic context analysis')
    print('   - Climate-adjusted estimates')
    print('   - NDVI-Soil correlation analysis')
    print('   - Comprehensive recommendations')
    print('\nData Sources:')
    print('   1. Known Survey Data (95% confidence)')
    print('   2. Copernicus Satellite (70-85% confidence)')
    print('   3. SoilGrids API (72% confidence)')
    print('   4. Regional Modeling (62% confidence)')
    print('=' * 80)
    
    # Get port from environment or default to 5002
    port = int(os.getenv('FLASK_PORT', 5002))
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    
    print(f"\nServer starting on http://{host}:{port}")
    print(f"NDVI module integration: {'Active' if (ndvi_integration and ndvi_integration.is_available()) else 'Fallback'}")
    print(f"Copernicus integration: {'Active' if (soil_collector and soil_collector.copernicus_downloader) else 'Unavailable'}")
    print('\n' + '=' * 80 + '\n')
    
    # Run Flask app
    app.run(host=host, port=port, debug=True)
