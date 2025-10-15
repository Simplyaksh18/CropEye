
"""
Soil Analysis Flask Backend
REST API for comprehensive soil analysis with NDVI integration
Uses existing NDVI module and root backend .env credentials
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import tempfile
import logging
from datetime import datetime
import json
import sys

# Import local modules
from env_credentials import env_creds
from soil_data_collector import SoilDataCollector
from ndvi_integration import ndvi_integration

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set environment variables from root backend .env
env_creds.set_environment_variables()

# Initialize soil data collector
soil_collector = SoilDataCollector()

@app.route('/api/health', methods=['GET'])
def health_check():
    """API health check"""
    return jsonify({
        'status': 'healthy',
        'service': 'Soil Analysis Backend with NDVI Integration',
        'timestamp': datetime.now().isoformat(),
        'modules': {
            'soil_data_collector': 'active',
            'ndvi_integration': 'active' if ndvi_integration.is_available() else 'fallback',
            'soilgrids_api': 'available'
        },
        'known_soil_locations': len(soil_collector.known_agricultural_locations),
        'ndvi_integration_status': ndvi_integration.get_status(),
        'credentials_status': {
            'copernicus': env_creds.has_copernicus_credentials(),
            'soilgrids': bool(env_creds.SOILGRIDS_API_KEY)
        },
        'message': 'Soil Analysis System Ready with NDVI Integration',
        'coordinates_supported': 'Both GPS-fetched and manual coordinates'
    })

@app.route('/api/soil/analyze', methods=['POST', 'OPTIONS'])
def analyze_soil():
    """
    Main soil analysis endpoint with NDVI integration

    Expected JSON payload:
    {
        "latitude": 30.3398,
        "longitude": 76.3869,
        "include_ndvi": true,
        "analysis_depth": "comprehensive"
    }
    """

    # Handle CORS preflight
    if request.method == 'OPTIONS':
        return '', 200

    try:
        data = request.get_json()

        # Validate input
        if not data or 'latitude' not in data or 'longitude' not in data:
            return jsonify({'error': 'Latitude and longitude required'}), 400

        lat = float(data['latitude'])
        lng = float(data['longitude'])
        include_ndvi = data.get('include_ndvi', True)
        analysis_depth = data.get('analysis_depth', 'comprehensive')

        logger.info(f"🌱 Comprehensive soil analysis: {lat}, {lng} (include_ndvi: {include_ndvi})")

        # Perform soil analysis with NDVI integration
        soil_result = soil_collector.get_soil_data(lat, lng, include_ndvi=include_ndvi)

        if not soil_result:
            return jsonify({'error': 'Soil analysis failed'}), 500

        # Add analysis metadata
        soil_result['request_parameters'] = {
            'latitude': lat,
            'longitude': lng,
            'include_ndvi': include_ndvi,
            'analysis_depth': analysis_depth,
            'coordinate_source': 'user_provided'  # Could be GPS or manual
        }

        # Add management recommendations
        soil_result['management_recommendations'] = _generate_management_recommendations(soil_result)

        # Add crop suitability if comprehensive analysis requested
        if analysis_depth == 'comprehensive':
            soil_result['crop_suitability'] = _assess_crop_suitability(soil_result)

        # Add integration status
        soil_result['integration_status'] = {
            'ndvi_module_available': ndvi_integration.is_available(),
            'soil_data_sources': soil_result.get('data_sources', []),
            'processing_method': 'comprehensive_analysis'
        }

        logger.info(f"✅ Comprehensive soil analysis complete: {soil_result.get('confidence_score', 0):.2f} confidence")
        return jsonify(soil_result)

    except ValueError as e:
        logger.error(f"Invalid input: {e}")
        return jsonify({'error': f'Invalid coordinates: {str(e)}'}), 400

    except Exception as e:
        logger.error(f"Soil analysis error: {e}")
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

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
        properties = data.get('properties', ['ph', 'nitrogen', 'phosphorus', 'potassium', 'organic_carbon'])
        include_ndvi = data.get('include_ndvi', True)

        if len(locations) < 2:
            return jsonify({'error': 'At least 2 locations required for comparison'}), 400

        logger.info(f"🔍 Comparing soil at {len(locations)} locations")

        # Analyze each location
        comparison_results = {
            'comparison_date': datetime.now().isoformat(),
            'locations': [],
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
            result = soil_collector.get_soil_data(lat, lng, include_ndvi=include_ndvi)

            if result and result.get('soil_properties'):
                soil_data[name] = result

                location_summary = {
                    'name': name,
                    'coordinates': {'latitude': lat, 'longitude': lng},
                    'soil_type': result.get('location_info', {}).get('soil_type', 'Unknown'),
                    'confidence': result.get('confidence_score', 0),
                    'data_sources': result.get('data_sources', [])
                }

                # Add NDVI info if available
                if include_ndvi and result.get('ndvi_correlation'):
                    ndvi_data = result['ndvi_correlation']
                    location_summary['ndvi_value'] = ndvi_data.get('ndvi_value')
                    location_summary['ndvi_source'] = ndvi_data.get('ndvi_data_source')
                    location_summary['vegetation_health'] = ndvi_data.get('health_analysis', {}).get('category')

                comparison_results['locations'].append(location_summary)

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
                    'mean': sum(values) / len(values),
                    'range': max(values) - min(values),
                    'variation': 'High' if (max(values) - min(values)) / (sum(values) / len(values)) > 0.5 else 'Low'
                }

                comparison_results['property_comparison'][prop] = prop_comparison

        # NDVI comparison if requested
        if include_ndvi:
            ndvi_values = []
            ndvi_comparison = {
                'values': {},
                'statistics': {},
                'soil_vegetation_correlation': []
            }

            for name, data in soil_data.items():
                if data.get('ndvi_correlation') and data['ndvi_correlation'].get('ndvi_value') is not None:
                    ndvi_val = data['ndvi_correlation']['ndvi_value']
                    ndvi_values.append(ndvi_val)

                    ndvi_comparison['values'][name] = {
                        'ndvi_value': ndvi_val,
                        'vegetation_health': data['ndvi_correlation'].get('health_analysis', {}).get('category', 'Unknown'),
                        'data_source': data['ndvi_correlation'].get('ndvi_data_source', 'Unknown')
                    }

            if len(ndvi_values) > 1:
                ndvi_comparison['statistics'] = {
                    'min': min(ndvi_values),
                    'max': max(ndvi_values),
                    'mean': sum(ndvi_values) / len(ndvi_values),
                    'range': max(ndvi_values) - min(ndvi_values)
                }

            comparison_results['ndvi_comparison'] = ndvi_comparison

        # Generate comparison recommendations
        comparison_results['recommendations'] = _generate_comparison_recommendations(comparison_results, soil_data)

        logger.info(f"✅ Soil comparison complete for {len(soil_data)} locations")
        return jsonify(comparison_results)

    except Exception as e:
        logger.error(f"Soil comparison error: {e}")
        return jsonify({'error': f'Comparison failed: {str(e)}'}), 500

@app.route('/api/soil/recommendations/<float:lat>/<float:lng>', methods=['GET'])
def get_soil_recommendations(lat, lng):
    """Get detailed soil management recommendations for specific coordinates"""

    try:
        logger.info(f"🌾 Getting comprehensive soil recommendations for {lat}, {lng}")

        # Get soil data with NDVI integration
        soil_result = soil_collector.get_soil_data(lat, lng, include_ndvi=True)

        if not soil_result:
            return jsonify({'error': 'Unable to get soil data'}), 500

        # Generate detailed recommendations
        recommendations = {
            'coordinates': {'latitude': lat, 'longitude': lng},
            'analysis_date': datetime.now().isoformat(),
            'soil_health_score': _calculate_soil_health_score(soil_result),
            'immediate_actions': [],
            'seasonal_recommendations': {},
            'long_term_improvements': [],
            'fertilizer_recommendations': {},
            'irrigation_advice': {},
            'ndvi_soil_insights': {}
        }

        # Add specific recommendations based on soil properties
        if 'soil_properties' in soil_result:
            props = soil_result['soil_properties']

            # pH recommendations
            if 'ph' in props:
                ph_value = props['ph']['value']
                if ph_value < 6.0:
                    recommendations['immediate_actions'].append({
                        'action': 'Lime Application',
                        'reason': f'Soil pH is acidic ({ph_value})',
                        'recommendation': f'Apply agricultural lime at 2-4 tons/hectare',
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

                    if 'Low' in n_class or 'Very Low' in n_class:
                        if nutrient == 'nitrogen':
                            recommendations['fertilizer_recommendations'][nutrient] = {
                                'status': 'Deficient',
                                'current_level': f"{n_value} ppm",
                                'recommended_application': '120-150 kg N/hectare',
                                'sources': ['Urea', 'Ammonium Sulfate', 'Organic Compost'],
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
                                'sources': ['MOP', 'SOP', 'Potassium Schoenite'],
                                'timing': '50% at sowing, 50% at active growth stage'
                            }

        # NDVI-based recommendations
        if soil_result.get('ndvi_correlation'):
            ndvi_data = soil_result['ndvi_correlation']
            correlation_analysis = ndvi_data.get('soil_ndvi_correlation', {})

            recommendations['ndvi_soil_insights'] = {
                'ndvi_value': ndvi_data.get('ndvi_value'),
                'vegetation_health': ndvi_data.get('health_analysis', {}).get('category', 'Unknown'),
                'soil_vegetation_match': correlation_analysis.get('vegetation_soil_match', 'Unknown'),
                'limiting_factors': correlation_analysis.get('limiting_factors', []),
                'ndvi_recommendations': correlation_analysis.get('recommendations', [])
            }

            # Add NDVI-specific actions
            if ndvi_data.get('ndvi_value', 0) < 0.4:
                recommendations['immediate_actions'].append({
                    'action': 'Vegetation Health Assessment',
                    'reason': f'Low NDVI value ({ndvi_data.get("ndvi_value", 0):.3f}) indicates poor vegetation',
                    'recommendation': 'Investigate pest/disease issues and nutrient deficiencies',
                    'timing': 'Immediately',
                    'priority': 'High'
                })

        return jsonify(recommendations)

    except Exception as e:
        logger.error(f"Soil recommendations error: {e}")
        return jsonify({'error': f'Recommendations failed: {str(e)}'}), 500

@app.route('/api/soil/known-locations', methods=['GET'])
def get_known_locations():
    """Get list of known agricultural locations with sample data"""

    try:
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
                },
                'matches_ndvi_module': True  # These coordinates match your NDVI module
            })

        return jsonify({
            'known_locations': locations,
            'total_locations': len(locations),
            'message': 'These locations have verified soil survey data and match NDVI module coordinates',
            'integration_note': 'Coordinates are synchronized with existing NDVI module'
        })

    except Exception as e:
        logger.error(f"Known locations error: {e}")
        return jsonify({'error': f'Failed to get known locations: {str(e)}'}), 500

@app.route('/api/soil/integration-status', methods=['GET'])
def get_integration_status():
    """Get detailed integration status with NDVI module"""

    try:
        ndvi_status = ndvi_integration.get_status()

        integration_info = {
            'timestamp': datetime.now().isoformat(),
            'soil_module_status': 'active',
            'ndvi_integration': {
                'available': ndvi_status['module_available'],
                'calculator_initialized': ndvi_status['calculator_initialized'],
                'downloader_initialized': ndvi_status['downloader_initialized'],
                'known_locations': ndvi_status['known_locations'],
                'import_path': '../NDVI directory'
            },
            'credentials': {
                'copernicus_available': env_creds.has_copernicus_credentials(),
                'soilgrids_key_available': bool(env_creds.SOILGRIDS_API_KEY),
                'env_file_location': 'root backend directory'
            },
            'data_sources': {
                'known_agricultural_locations': len(soil_collector.known_agricultural_locations),
                'soilgrids_api': 'available',
                'regional_modeling': 'available',
                'fallback_generation': 'available'
            },
            'coordinate_handling': {
                'gps_coordinates': 'supported',
                'manual_coordinates': 'supported',
                'coordinate_validation': 'active'
            }
        }

        return jsonify(integration_info)

    except Exception as e:
        logger.error(f"Integration status error: {e}")
        return jsonify({'error': f'Status check failed: {str(e)}'}), 500

@app.route('/api/soil/debug', methods=['GET'])
def debug_info():
    """Debug endpoint for troubleshooting"""

    debug_data = {
        'system_info': {
            'working_directory': os.getcwd(),
            'python_path': sys.path[:3],  # First 3 paths
            'environment_variables': {
                'COPERNICUS_USERNAME': bool(os.getenv('COPERNICUS_USERNAME')),
                'COPERNICUS_PASSWORD': bool(os.getenv('COPERNICUS_PASSWORD')),
                'SOILGRIDS_API_KEY': bool(os.getenv('SOILGRIDS_API_KEY'))
            }
        },
        'modules_available': {},
        'known_soil_locations': list(soil_collector.known_agricultural_locations.keys()),
        'ndvi_integration': ndvi_integration.get_status(),
        'test_coordinates': [
            {'name': 'Punjab Wheat', 'lat': 30.3398, 'lng': 76.3869, 'expected': 'Alluvial Soil, pH 7.2'},
            {'name': 'Maharashtra Sugarcane', 'lat': 18.15, 'lng': 74.5777, 'expected': 'Black Cotton Soil, pH 8.1'},
            {'name': 'California Central Valley', 'lat': 36.7783, 'lng': -119.4179, 'expected': 'Aridisol, pH 7.8'},
            {'name': 'Iowa Corn Farm', 'lat': 41.5868, 'lng': -93.6250, 'expected': 'Prairie Soil, pH 6.3'},
            {'name': 'Karnataka Coffee', 'lat': 13.3409, 'lng': 75.7131, 'expected': 'Red Lateritic, pH 5.8'}
        ]
    }

    # Test module availability
    modules_to_test = ['requests', 'numpy', 'flask', 'rasterio']
    for module in modules_to_test:
        try:
            __import__(module)
            debug_data['modules_available'][module] = True
        except ImportError:
            debug_data['modules_available'][module] = False

    return jsonify(debug_data)

# Helper functions for recommendations
def _generate_management_recommendations(soil_result):
    """Generate soil management recommendations"""
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
        if 'Low' in oc_class or 'Very Low' in oc_class:
            recommendations['long_term'].append("Increase organic matter through composting, cover crops, or organic amendments")

    return recommendations

def _assess_crop_suitability(soil_result):
    """Assess crop suitability based on soil properties"""
    suitability = {
        'highly_suitable': [],
        'moderately_suitable': [],
        'not_suitable': [],
        'recommendations_by_crop': {}
    }

    if not soil_result.get('soil_properties'):
        return suitability

    props = soil_result['soil_properties']

    # Simple crop suitability logic based on pH and texture
    ph_val = props.get('ph', {}).get('value', 7.0)
    texture = props.get('texture', {}).get('value', 'Loam')

    # Rice suitability
    if 5.5 <= ph_val <= 7.0 and texture in ['Clay', 'Silty Clay']:
        suitability['highly_suitable'].append('Rice')

    # Wheat suitability
    if 6.0 <= ph_val <= 7.5 and texture in ['Loam', 'Clay Loam', 'Sandy Loam']:
        suitability['highly_suitable'].append('Wheat')

    # Corn suitability
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
            recommendations.append(f"High variation in {prop} across locations - consider site-specific management")

    # NDVI-based comparison recommendations
    if comparison_results.get('ndvi_comparison'):
        ndvi_stats = comparison_results['ndvi_comparison'].get('statistics', {})
        if ndvi_stats.get('range', 0) > 0.3:
            recommendations.append("Significant NDVI variation detected - investigate vegetation health differences")

    return recommendations

def _calculate_soil_health_score(soil_result):
    """Calculate overall soil health score (0-100)"""
    if not soil_result.get('soil_properties'):
        return 50  # Default neutral score

    score = 0
    factors = 0

    props = soil_result['soil_properties']

    # pH score (optimal range 6.0-7.5)
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
            if 'High' in classification or 'Very High' in classification:
                score += 15
            elif 'Medium' in classification:
                score += 12
            elif 'Low' in classification:
                score += 8
            else:
                score += 4
            factors += 1

    return min(100, score) if factors > 0 else 50

if __name__ == '__main__':
    print("🌱 Starting Soil Analysis Backend with NDVI Integration...")
    print("=" * 70)
    print("📍 API Endpoints:")
    print("  POST /api/soil/analyze - Comprehensive soil analysis with NDVI")
    print("  POST /api/soil/compare - Compare multiple locations") 
    print("  GET /api/soil/recommendations/<lat>/<lng> - Detailed recommendations")
    print("  GET /api/soil/known-locations - Known agricultural sites")
    print("  GET /api/soil/integration-status - NDVI integration status")
    print("  GET /api/health - Health check")
    print("  GET /api/soil/debug - Debug information")
    print("🔧 Key Features:")
    print("  ✅ Integrates with your existing NDVI module")
    print("  ✅ Uses root backend .env credentials")
    print("  ✅ Real agricultural survey data for known locations")
    print("  ✅ SoilGrids API integration for global coverage")
    print("  ✅ NDVI-Soil correlation analysis")
    print("  ✅ Supports both GPS and manual coordinates")
    print("  ✅ Comprehensive management recommendations")
    print("=" * 70)

    host = os.environ.get('SOIL_HOST', '127.0.0.1')
    port = int(os.environ.get('SOIL_PORT', '5002'))

    print(f"🚀 Server starting on http://{host}:{port}")
    print("🔗 NDVI module path: ../NDVI directory")
    print("🔧 Credentials path: root backend .env file")
    app.run(host=host, port=port, debug=True)
