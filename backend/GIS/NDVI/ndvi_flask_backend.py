#!/usr/bin/env python3
"""
CORRECTED Flask Backend for NDVI Analysis
Prioritizes REAL Copernicus data, falls back to synthetic only when necessary
"""
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import logging
from datetime import datetime, timedelta
import numpy as np
from dotenv import load_dotenv

# Import modules
from sentinel_downloader import CopernicusDataDownloader
from ndvi_calculator import NDVICalculator

# Load environment variables: prefer backend/.env, fall back to backend/file.env
dotenv_candidates = [
    os.path.join(os.path.dirname(__file__), '..', '..', '.env'),
    os.path.join(os.path.dirname(__file__), '..', '..', 'file.env'),
    os.path.join(os.path.dirname(__file__), '..', 'file.env')
]
loaded_dotenv = None
for p in dotenv_candidates:
    if os.path.exists(p):
        load_dotenv(dotenv_path=p)
        loaded_dotenv = p
        break

# Record which dotenv was loaded for debugging
if loaded_dotenv:
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.info(f"✅ Loaded environment variables from: {loaded_dotenv}")
else:
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.warning("⚠️  No dotenv file found in expected locations; relying on process environment")

app = Flask(__name__)
CORS(app)

# Configure logging (DEBUG to capture downloader internals)
# Note: set to DEBUG temporarily to help diagnose Copernicus queries
logger = logging.getLogger(__name__)

# Log presence of key environment variables for debugging
def log_env_vars():
    keys = ['COPERNICUS_USERNAME', 'COPERNICUS_PASSWORD', 'COPERNICUS_CLIENT_ID', 'COPERNICUS_CLIENT_SECRET', 'NDVI_FORCE_SIMULATED', 'NDVI_PORT']
    for key in keys:
        val = os.getenv(key)
        if val is None:
            logger.warning(f"⚠️  Environment variable {key} is NOT set")
        else:
            logger.info(f"✅ Environment variable {key} is set")

log_env_vars()

# Initialize components
downloader = CopernicusDataDownloader()
calculator = NDVICalculator()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'NDVI Analysis API',
        'timestamp': datetime.now().isoformat(),
        'copernicus_configured': downloader.username is not None,
        'force_simulated': downloader.force_simulated
    })

@app.route('/api/ndvi/analyze', methods=['POST'])
def analyze_ndvi():
    """
    Analyze NDVI for given coordinates
    PRIORITY: Try Copernicus first, fallback to synthetic only if fails
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        latitude = data.get('latitude')
        longitude = data.get('longitude')
        date_str = data.get('date')

        if latitude is None or longitude is None:
            return jsonify({'error': 'Latitude and longitude are required'}), 400

        # Parse date
        if date_str:
            try:
                target_date = datetime.strptime(date_str, '%Y-%m-%d')
            except ValueError:
                return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        else:
            target_date = datetime.now() - timedelta(days=7)

        logger.info(f"📍 NDVI Analysis Request: lat={latitude}, lon={longitude}, date={target_date.date()}")

        # STEP 1: Try REAL Copernicus data first
        real_data_success = False
        ndvi_data = None
        data_source = "unknown"

        if not downloader.force_simulated and downloader.username:
            logger.info("🛰️  Attempting to fetch REAL Copernicus Sentinel-2 data...")
            try:
                sentinel_data = downloader.download_sentinel_data(
                    latitude=latitude,
                    longitude=longitude,
                    start_date=target_date - timedelta(days=15),
                    end_date=target_date,
                    bands=['B04', 'B08']  # Red and NIR bands
                )

                if sentinel_data and 'status' in sentinel_data and sentinel_data['status'] == 'success':
                    logger.info("✅ Successfully downloaded REAL Copernicus data!")

                    # Calculate NDVI from real bands
                    red_band = sentinel_data.get('red_band')
                    nir_band = sentinel_data.get('nir_band')

                    if red_band is not None and nir_band is not None:
                        # Calculate NDVI
                        ndvi_value = calculator.calculate_ndvi_from_bands(red_band, nir_band)

                        # Safely convert to float only if values are not None
                        ndvi_float = None
                        try:
                            if ndvi_value is not None:
                                ndvi_float = float(ndvi_value)
                        except (TypeError, ValueError):
                            ndvi_float = None

                        red_float = None
                        try:
                            if red_band is not None:
                                red_float = float(red_band)
                        except (TypeError, ValueError):
                            red_float = None

                        nir_float = None
                        try:
                            if nir_band is not None:
                                nir_float = float(nir_band)
                        except (TypeError, ValueError):
                            nir_float = None

                        ndvi_data = {
                            'ndvi': ndvi_float,
                            'red_band': red_float,
                            'nir_band': nir_float,
                            'health_category': calculator.get_health_category(ndvi_value) if ndvi_value is not None else None,
                            'health_score': calculator.get_health_score(ndvi_value) if ndvi_value is not None else None,
                            'description': f'Real satellite data from Copernicus Sentinel-2',
                            'acquisition_date': sentinel_data.get('acquisition_date', target_date.isoformat()),
                            'cloud_coverage': sentinel_data.get('cloud_coverage', 0)
                        }

                        real_data_success = True
                        data_source = "copernicus_real"
                        logger.info(f"🎯 Real NDVI calculated: {ndvi_value:.3f}")
                    else:
                        logger.warning("⚠️  Copernicus returned success but bands are missing")
                else:
                    logger.warning("⚠️  Copernicus data download failed or returned no data")

            except Exception as e:
                logger.error(f"❌ Error fetching Copernicus data: {e}")
                real_data_success = False
        else:
            if downloader.force_simulated:
                logger.info("⚙️  NDVI_FORCE_SIMULATED is enabled - skipping real data")
            else:
                logger.warning("⚠️  No Copernicus credentials configured - cannot fetch real data")

        # STEP 2: Fallback to synthetic/modeled data if real data failed
        if not real_data_success:
            logger.info("📊 Falling back to synthetic/modeled NDVI data...")

            ndvi_data = calculator.calculate_ndvi(
                latitude=latitude,
                longitude=longitude,
                acquisition_date=target_date
            )

            data_source = "synthetic_modeled"
            logger.warning("⚠️  Using SYNTHETIC data - not real satellite imagery!")

            # Convert any numpy ndarrays to lists for JSON serialization
            if isinstance(ndvi_data, dict) and ndvi_data.get('ndvi_array') is not None:
                try:
                    ndvi_data['ndvi_array'] = ndvi_data['ndvi_array'].tolist()
                except AttributeError:
                    # ndvi_array is not a numpy array (already serializable) — leave as is
                    pass

        # Build response
        response = {
            'status': 'success',
            'data': ndvi_data,
            'metadata': {
                'latitude': latitude,
                'longitude': longitude,
                'date': target_date.isoformat(),
                'data_source': data_source,
                'is_real_data': real_data_success,
                'timestamp': datetime.now().isoformat()
            }
        }

        return jsonify(response), 200

    except Exception as e:
        logger.error(f"Error in NDVI analysis: {e}")
        return jsonify({
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/ndvi/timeseries', methods=['POST'])
def get_ndvi_timeseries():
    """Get NDVI time series data"""
    try:
        data = request.get_json()

        latitude = data.get('latitude')
        longitude = data.get('longitude')
        start_date_str = data.get('start_date')
        end_date_str = data.get('end_date')

        if not all([latitude, longitude, start_date_str, end_date_str]):
            return jsonify({'error': 'Missing required parameters'}), 400

        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

        logger.info(f"📈 Time series request: {start_date.date()} to {end_date.date()}")

        # Generate time series (attempt real data for each point)
        timeseries = []
        current_date = start_date

        while current_date <= end_date:
            # Try real data first
            point_data = {
                'date': current_date.isoformat(),
                'ndvi': None,
                'source': 'none'
            }

            if not downloader.force_simulated and downloader.username:
                try:
                    sentinel_data = downloader.download_sentinel_data(
                        latitude=latitude,
                        longitude=longitude,
                        start_date=current_date - timedelta(days=3),
                        end_date=current_date + timedelta(days=3),
                        bands=['B04', 'B08']
                    )

                    if sentinel_data and sentinel_data.get('status') == 'success':
                        red = sentinel_data.get('red_band')
                        nir = sentinel_data.get('nir_band')
                        if red is not None and nir is not None:
                            ndvi_val = calculator.calculate_ndvi_from_bands(red, nir)
                            # Safely convert only when a numeric value is returned
                            if ndvi_val is not None:
                                try:
                                    point_data['ndvi'] = float(ndvi_val)
                                    point_data['source'] = 'copernicus_real'
                                except (TypeError, ValueError):
                                    logger.warning("Invalid NDVI value from bands; falling back to synthetic")
                                    point_data['ndvi'] = None
                                    point_data['source'] = 'none'
                except Exception as e:
                    logger.error(f"Error fetching Sentinel data in time series: {e}")

            # Fallback to synthetic
            if point_data['ndvi'] is None:
                synthetic = calculator.calculate_ndvi(latitude, longitude, current_date)
                # synthetic may be None or not a dict; handle robustly
                if isinstance(synthetic, dict):
                    point_data['ndvi'] = synthetic.get('ndvi', 0.5)
                else:
                    # Explicitly handle None before converting to float to satisfy type checkers
                    if synthetic is None:
                        point_data['ndvi'] = 0.5
                    else:
                        try:
                            # if synthetic is a numeric value
                            point_data['ndvi'] = float(synthetic)
                        except (TypeError, ValueError):
                            point_data['ndvi'] = 0.5
                point_data['source'] = 'synthetic'

            timeseries.append(point_data)
            current_date += timedelta(days=7)  # Weekly intervals

        return jsonify({
            'status': 'success',
            'data': timeseries,
            'metadata': {
                'latitude': latitude,
                'longitude': longitude,
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat()
            }
        }), 200

    except Exception as e:
        logger.error(f"Error in time series: {e}")
        return jsonify({'status': 'error', 'error': str(e)}), 500

# Optional endpoint for environment credential check (for debugging)
@app.route('/api/env_check', methods=['GET'])
def env_check():
    creds = {
        'COPERNICUS_USERNAME': bool(os.getenv('COPERNICUS_USERNAME')),
        'COPERNICUS_PASSWORD': bool(os.getenv('COPERNICUS_PASSWORD')),
        'COPERNICUS_CLIENT_ID': bool(os.getenv('COPERNICUS_CLIENT_ID')),
        'COPERNICUS_CLIENT_SECRET': bool(os.getenv('COPERNICUS_CLIENT_SECRET')),
        'NDVI_FORCE_SIMULATED': bool(os.getenv('NDVI_FORCE_SIMULATED')),
        'NDVI_PORT': os.getenv('NDVI_PORT', 'Not Set')
    }
    return jsonify({'environment_variables': creds}), 200

if __name__ == '__main__':
    port = int(os.getenv('NDVI_PORT', 5001))
    logger.info(f"🚀 Starting NDVI Analysis API on port {port}")
    logger.info(f"📡 Copernicus configured: {downloader.username is not None}")
    logger.info(f"⚙️  Force simulated: {downloader.force_simulated}")
    app.run(host='0.0.0.0', port=port, debug=True)
