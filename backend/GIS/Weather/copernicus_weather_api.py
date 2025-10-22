#!/usr/bin/env python3
"""
Copernicus ERA5 Weather API Handler
CropEye1 Weather Module - Historical & Reanalysis Weather Data

Location: D:\\CropEye1\\backend\\GIS\\Weather\\copernicus_weather_api.py

Features:
- ERA5 hourly reanalysis data (1950-present)
- Soil moisture data
- Solar radiation
- Evapotranspiration
- High-resolution historical weather

Uses Copernicus Climate Data Store (CDS) API
API Docs: https://cds.climate.copernicus.eu/api-how-to

Author: CropEye1 System
Date: October 18, 2025 - FIXED VERSION
"""

import os
import logging
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import tempfile
from pathlib import Path

# Configure logging once
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Optional dependencies with proper error handling
try:
    import cdsapi
except ImportError:
    cdsapi = None
    logger.warning('cdsapi package not found; Copernicus CDS features will be unavailable')

try:
    import netCDF4 as nc
except ImportError:
    nc = None
    logger.warning('netCDF4 package not found; NetCDF processing will be disabled')


class CopernicusWeatherAPI:
    """Copernicus ERA5 Climate Data Store API client"""
    
    def __init__(self):
        """Initialize Copernicus CDS API client"""
        
        # Check for CDS API credentials
        cds_url = os.getenv('COPERNICUS_CDS_URL', 'https://cds.climate.copernicus.eu/api/v2')
        cds_key = os.getenv('COPERNICUS_CDS_KEY')
        
        self.available: bool = False
        self.client: Optional[Any] = None
        
        # Try to initialize CDS API if available
        # Attempt robust initialization of the CDS client. The CDS API and the cdsapi
        # client have evolved: older .cdsapirc files used an URL ending in /api/v2 and
        # a key prefixed with '<UID>:', while newer clients expect the URL
        # 'https://cds.climate.copernicus.eu/api' and the API key without the prefix.
        if cdsapi is None:
            logger.warning("cdsapi package not found; Copernicus CDS features will be unavailable.")
        else:
            # Helper to try to create a client with given params
            def try_client(url_try: str, key_try: Optional[str]) -> Optional[Any]:
                # If cdsapi failed to import, avoid calling its Client attribute.
                if cdsapi is None:
                    return None
                try:
                    if key_try:
                        return cdsapi.Client(url=url_try, key=key_try, verify=True)
                    else:
                        # Let cdsapi read the user's ~/.cdsapirc if no key provided
                        return cdsapi.Client()
                except Exception:
                    return None

            # First-pass: try the env-provided url/key (if any)
            tried = []
            client = None
            if cds_key:
                client = try_client(cds_url, cds_key)
                tried.append((cds_url, cds_key, client is not None))

            # If first attempt failed (or no env key), try letting cdsapi read .cdsapirc
            if client is None:
                client = try_client(cds_url, None)
                tried.append((cds_url, None, client is not None))

            # If still failed, try common fallback URL without /v2
            if client is None:
                alt_url = cds_url.rstrip('/')
                if alt_url.endswith('/v2'):
                    alt_url = alt_url[: -3]  # remove '/v2'
                else:
                    alt_url = 'https://cds.climate.copernicus.eu/api'

                # If cds_key was provided with a UID prefix like '12345:abcd', try stripping the prefix
                stripped_key = None
                if cds_key and ':' in cds_key:
                    stripped_key = cds_key.split(':', 1)[1]

                client = try_client(alt_url, cds_key)
                tried.append((alt_url, cds_key, client is not None))

                if client is None and stripped_key:
                    client = try_client(alt_url, stripped_key)
                    tried.append((alt_url, stripped_key, client is not None))

            if client is not None:
                self.client = client
                self.available = True
                logger.info("✅ Copernicus CDS API initialized")
                # If we attempted any fallbacks, log them at debug level to help the user
                for url_try, key_try, ok in tried:
                    logger.debug(f"cdsapi try: url={url_try!r} key_present={bool(key_try)} success={ok}")
                # If the key looks like it contains a deprecated UID prefix, inform the user
                if cds_key and cds_key.count(':') == 1:
                    uid_prefix = cds_key.split(':', 1)[0]
                    if uid_prefix.isdigit() or len(uid_prefix) > 4:
                        logger.info("Notice: your COPERNICUS_CDS_KEY appears to include a UID prefix."
                                    " The CDS API now expects the key without the '<UID>:' prefix."
                                    " Consider updating your ~/.cdsapirc accordingly.")
            else:
                logger.warning("⚠️ Copernicus CDS API not available after trying common fallbacks.")
                logger.warning("   Ensure cdsapi is up-to-date and that ~/.cdsapirc or COPERNICUS_CDS_KEY is valid.")
        
        # Temp directory for downloaded files
        temp_dir_env = os.getenv('COPERNICUS_TEMP_DIR')
        if temp_dir_env:
            self.temp_dir = Path(temp_dir_env)
        else:
            self.temp_dir = Path(tempfile.gettempdir()) / "cropeye_weather"
        
        try:
            self.temp_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logger.warning(f"Could not create temp dir {self.temp_dir}: {e}")
    
    def is_available(self) -> bool:
        """Check if Copernicus API is available"""
        return self.available
    
    def get_era5_hourly_data(
        self,
        latitude: float,
        longitude: float,
        start_date: str,
        end_date: str,
        variables: Optional[List[str]] = None
    ) -> Dict:
        """
        Get ERA5 hourly reanalysis data
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            variables: List of variables to retrieve
            
        Returns:
            Dict containing hourly weather data
        """
        if not self.available or nc is None:
            logger.warning("Copernicus API or netCDF4 not available, using fallback")
            return self._get_fallback_era5_data(latitude, longitude, start_date, end_date)
        
        try:
            # Default variables
            if variables is None:
                variables = [
                    '2m_temperature',
                    'total_precipitation',
                    '10m_u_component_of_wind',
                    '10m_v_component_of_wind',
                    'surface_pressure',
                    'total_cloud_cover',
                    '2m_dewpoint_temperature'
                ]
            
            # Parse dates
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
            end_dt = datetime.strptime(end_date, '%Y-%m-%d')
            
            # Create bounding box
            bbox = self._create_bbox(latitude, longitude, buffer=0.1)
            
            # Prepare request
            request_params = {
                'product_type': 'reanalysis',
                'format': 'netcdf',
                'variable': variables,
                'year': [str(year) for year in range(start_dt.year, end_dt.year + 1)],
                'month': [f'{month:02d}' for month in range(1, 13)],
                'day': [f'{day:02d}' for day in range(1, 32)],
                'time': [f'{hour:02d}:00' for hour in range(24)],
                'area': [bbox['north'], bbox['west'], bbox['south'], bbox['east']],
            }
            
            # Download data
            output_file = self.temp_dir / f"era5_{latitude}_{longitude}_{start_date}_{end_date}.nc"
            
            logger.info(f"📥 Requesting ERA5 data from Copernicus CDS...")
            logger.info(f"   Period: {start_date} to {end_date}")
            logger.info(f"   Variables: {len(variables)}")
            # Log the request params (safe-printed) for diagnostics (no secrets)
            try:
                import json as _json
                logger.debug("CDS retrieve request params: %s", _json.dumps({k: str(v) for k, v in request_params.items()}))
            except Exception:
                logger.debug("CDS retrieve request params (could not JSONize)")
            
            # Ensure the CDS client is initialized before calling retrieve
            if self.client is None:
                logger.warning("Copernicus CDS client is not initialized; falling back to generated data")
                return self._get_fallback_era5_data(latitude, longitude, start_date, end_date)
            
            try:
                self.client.retrieve(
                    'reanalysis-era5-single-levels',
                    request_params,
                    str(output_file)
                )
            except Exception as e_retr:
                msg = str(e_retr)
                logger.error(f"❌ Failed to retrieve ERA5 data from Copernicus CDS: {msg}")
                # Attempt to extract HTTP response details if available on the exception
                http_status = None
                http_text = None
                try:
                    resp = getattr(e_retr, 'response', None)
                    if resp is not None:
                        http_status = getattr(resp, 'status_code', None)
                        http_text = getattr(resp, 'text', None)
                except Exception:
                    http_status = None
                    http_text = None
                # Retry once if this looks like an endpoint / api path mismatch
                if 'endpoint not found' in msg.lower() or 'api endpoint not found' in msg.lower() or 'not found' in msg.lower():
                    logger.info('Attempting a one-time retry using the CDS client (lenient)')
                    try:
                        self.client.retrieve('reanalysis-era5-single-levels', request_params, str(output_file))
                    except Exception as e2:
                        logger.error(f"Retry failed: {e2}")
                        logger.warning("   Falling back to local ERA5 data generator")
                        # Attach diagnostics to fallback
                        fb = self._get_fallback_era5_data(latitude, longitude, start_date, end_date)
                        fb['cds_error'] = msg
                        fb['cds_http_status'] = http_status
                        fb['cds_http_text'] = http_text
                        try:
                            fb['cds_request'] = {k: str(v) for k, v in request_params.items()}
                        except Exception:
                            fb['cds_request'] = 'unserializable'
                        return fb
                else:
                    logger.warning("   Falling back to local ERA5 data generator")
                    fb = self._get_fallback_era5_data(latitude, longitude, start_date, end_date)
                    fb['cds_error'] = msg
                    fb['cds_http_status'] = http_status
                    fb['cds_http_text'] = http_text
                    try:
                        fb['cds_request'] = {k: str(v) for k, v in request_params.items()}
                    except Exception:
                        fb['cds_request'] = 'unserializable'
                    return fb

            logger.info("✅ ERA5 data downloaded, processing...")

            # Discover actual output file: the cdsapi client may write to a
            # different temporary file name than the one we passed. Try the
            # expected path first, otherwise search the temp dir for the
            # most-recent .nc file.
            actual_output = output_file
            if not output_file.exists():
                try:
                    tmpdir = Path(self.temp_dir)
                    if not tmpdir.exists():
                        tmpdir = Path(tempfile.gettempdir()) / 'cropeye_weather'
                    nc_files = list(tmpdir.glob('*.nc'))
                    if nc_files:
                        actual_output = max(nc_files, key=lambda p: p.stat().st_mtime)
                except Exception:
                    actual_output = output_file

            # Try to preserve a copy of the actual output into project outputs
            saved_path = None
            try:
                if actual_output.exists():
                    outputs_dir = Path(__file__).resolve().parents[2] / 'GIS' / 'Weather' / 'outputs'
                    outputs_dir.mkdir(parents=True, exist_ok=True)
                    dest = outputs_dir / actual_output.name
                    counter = 0
                    while dest.exists():
                        counter += 1
                        dest = outputs_dir / f"{actual_output.stem}.{counter}{actual_output.suffix}"
                    try:
                        import shutil
                        shutil.copy2(str(actual_output), str(dest))
                        saved_path = str(dest)
                    except Exception:
                        try:
                            actual_output.replace(dest)
                            saved_path = str(dest)
                        except Exception:
                            saved_path = None
            except Exception:
                saved_path = None

            # Process NetCDF file using the discovered actual output path
            weather_data = self._process_era5_netcdf(actual_output, latitude, longitude)

            # Attach metadata about the downloaded file
            try:
                weather_data['file_path'] = saved_path
                weather_data['original_file_path'] = str(actual_output) if actual_output.exists() else None
            except Exception:
                pass

            return weather_data
        except Exception as e:
            logger.error(f"❌ Error retrieving ERA5 hourly data: {e}")
            return self._get_fallback_era5_data(latitude, longitude, start_date, end_date)

    def get_era5_soil_moisture(
        self,
        latitude: float,
        longitude: float,
        start_date: str,
        end_date: str
    ) -> Dict:
        """
        Get ERA5 soil moisture data
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            
        Returns:
            Dict containing soil moisture data
        """
        if not self.available:
            return self._get_fallback_soil_moisture(latitude, longitude, start_date, end_date)
        
        try:
            variables = [
                'volumetric_soil_water_layer_1',
                'volumetric_soil_water_layer_2',
                'volumetric_soil_water_layer_3',
                'volumetric_soil_water_layer_4',
                'soil_temperature_level_1'
            ]
            
            data = self.get_era5_hourly_data(
                latitude, longitude, start_date, end_date, variables
            )
            
            return data
            
        except Exception as e:
            logger.error(f"❌ Error retrieving soil moisture: {e}")
            return self._get_fallback_soil_moisture(latitude, longitude, start_date, end_date)
    
    def get_era5_solar_radiation(
        self,
        latitude: float,
        longitude: float,
        start_date: str,
        end_date: str
    ) -> Dict:
        """
        Get ERA5 solar radiation data
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            
        Returns:
            Dict containing solar radiation data
        """
        if not self.available:
            return self._get_fallback_solar_radiation(latitude, longitude, start_date, end_date)
        
        try:
            variables = [
                'surface_solar_radiation_downwards',
                'surface_net_solar_radiation',
                'total_sky_direct_solar_radiation_at_surface'
            ]
            
            data = self.get_era5_hourly_data(
                latitude, longitude, start_date, end_date, variables
            )
            
            return data
            
        except Exception as e:
            logger.error(f"❌ Error retrieving solar radiation: {e}")
            return self._get_fallback_solar_radiation(latitude, longitude, start_date, end_date)
    
    def _create_bbox(self, latitude: float, longitude: float, buffer: float = 0.1) -> Dict:
        """Create bounding box around point"""
        return {
            'north': latitude + buffer,
            'south': latitude - buffer,
            'east': longitude + buffer,
            'west': longitude - buffer
        }
    
    def _process_era5_netcdf(self, file_path: Path, latitude: float, longitude: float) -> Dict:
        """
        Process ERA5 NetCDF file and extract data for location
        
        Args:
            file_path: Path to NetCDF file
            latitude: Target latitude
            longitude: Target longitude
            
        Returns:
            Dict containing processed weather data
        """
        try:
            # Ensure netCDF4 is available
            if nc is None:
                try:
                    import netCDF4 as nc_module
                except ImportError:
                    raise RuntimeError("netCDF4 is required to process NetCDF files")
            else:
                nc_module = nc
            
            # Open NetCDF file
            with nc_module.Dataset(str(file_path), 'r') as dataset:
                # Find nearest grid point
                # Robust lookup for latitude/longitude variables (try common names and fallbacks)
                def _find_var_by_names(ds, names):
                    for n in names:
                        if n in ds.variables:
                            return ds.variables[n][:]
                    return None

                lats = _find_var_by_names(dataset, ['latitude', 'lat', 'latitudes', 'nav_lat'])
                lons = _find_var_by_names(dataset, ['longitude', 'lon', 'longitudes', 'nav_lon'])

                # If not found, try to heuristically find 1D or 2D latitude/longitude arrays
                if lats is None or lons is None:
                    for vname, vobj in dataset.variables.items():
                        try:
                            if getattr(vobj, 'standard_name', '').lower() in ('latitude',) and lats is None:
                                lats = vobj[:]
                            if getattr(vobj, 'standard_name', '').lower() in ('longitude',) and lons is None:
                                lons = vobj[:]
                        except Exception:
                            continue

                if lats is None or lons is None:
                    # As a last resort, try any 1D numeric variable that looks like lat/lon (range checks)
                    for vname, vobj in dataset.variables.items():
                        try:
                            arr = np.array(vobj[:])
                            if arr.ndim == 1 and lats is None and arr.min() >= -90 and arr.max() <= 90:
                                lats = arr
                            if arr.ndim == 1 and lons is None and arr.min() >= -180 and arr.max() <= 180:
                                lons = arr
                        except Exception:
                            continue

                if lats is None or lons is None:
                    raise KeyError('latitude/longitude')
                
                # Handle 1D or 2D lat/lon arrays
                if lats.ndim == 1 and lons.ndim == 1:
                    lat_idx = np.abs(lats - latitude).argmin()
                    lon_idx = np.abs(lons - longitude).argmin()
                    actual_lat = float(lats[lat_idx])
                    actual_lon = float(lons[lon_idx])
                else:
                    # 2D arrays - find nearest by distance
                    lats_arr = np.array(lats)
                    lons_arr = np.array(lons)
                    dist = (lats_arr - latitude)**2 + (lons_arr - longitude)**2
                    flat_idx = np.argmin(dist)
                    lat_idx, lon_idx = np.unravel_index(flat_idx, lats_arr.shape)
                    actual_lat = float(lats_arr[lat_idx, lon_idx])
                    actual_lon = float(lons_arr[lat_idx, lon_idx])
                
                # Extract time
                # Extract time variable robustly (try common names and heuristics)
                time_var = None
                for cand in ('time', 'times', 'date', 'time_counter'):
                    if cand in dataset.variables:
                        time_var = dataset.variables[cand]
                        break

                if time_var is None:
                    # look for variable with 'units' attribute containing 'since'
                    for vname, vobj in dataset.variables.items():
                        try:
                            units_attr = getattr(vobj, 'units', '')
                            if isinstance(units_attr, str) and 'since' in units_attr:
                                time_var = vobj
                                break
                        except Exception:
                            continue

                if time_var is None:
                    # look for a dimension named like time and try to find a variable for it
                    for dim_name in dataset.dimensions.keys():
                        if 'time' in dim_name.lower():
                            if dim_name in dataset.variables:
                                time_var = dataset.variables[dim_name]
                                break

                if time_var is None:
                    raise KeyError('time')

                times = time_var[:]
                time_units = getattr(time_var, 'units', None)
                time_calendar = getattr(time_var, 'calendar', 'standard')
                
                # Ensure time_units is a str for netCDF4.num2date and provide a safe fallback
                if time_units is None:
                    # Fall back to a reasonable epoch-based units if missing; many datasets use hours since 1970-01-01
                    time_units = 'hours since 1970-01-01 00:00:00'
                
                # Convert time to datetime objects and ensure iterable list
                dates = nc_module.num2date(times, time_units, time_calendar)
                
                # Normalize to a Python list of datetime objects (handles scalars and arrays)
                try:
                    # num2date may return a single datetime or an array-like of datetimes.
                    # Convert without using numpy.atleast_1d to avoid typing errors for datetime objects.
                    if isinstance(dates, (list, tuple)):
                        dates = list(dates)
                    elif isinstance(dates, np.ndarray):
                        # Convert numpy array (including numpy datetime types) to list
                        dates = dates.tolist()
                    else:
                        # Single datetime object or scalar - wrap in list
                        dates = [dates]
                except Exception:
                    # Fallback: wrap single datetime in list or convert iterable to list
                    if not hasattr(dates, '__iter__') or isinstance(dates, (str, bytes, datetime)):
                        dates = [dates]
                    else:
                        dates = list(dates)
                
                # Extract data for each variable
                hourly_data = []
                
                for i, date in enumerate(dates):
                    # Convert timestamp
                    try:
                        if isinstance(date, datetime):
                            timestamp = date.isoformat()
                        else:
                            timestamp = str(date)
                    except:
                        timestamp = str(date)
                    
                    data_point = {
                        'timestamp': timestamp,
                        'latitude': actual_lat,
                        'longitude': actual_lon
                    }
                    
                    # Extract all available variables
                    for var_name in dataset.variables:
                        if var_name in ['latitude', 'longitude', 'time']:
                            continue
                        
                        try:
                            var_data = dataset.variables[var_name]
                            
                            # Handle different shapes
                            if var_data.ndim == 3:  # (time, lat, lon)
                                raw_value = var_data[i, lat_idx, lon_idx]
                            elif var_data.ndim == 4:  # (time, level, lat, lon)
                                raw_value = var_data[i, 0, lat_idx, lon_idx]
                            else:
                                continue
                            
                            # Check for masked values
                            if np.ma.is_masked(raw_value):
                                continue
                            
                            # Convert to Python float
                            if hasattr(raw_value, 'item'):
                                value = float(raw_value.item())
                            else:
                                value = float(raw_value)
                            
                            data_point[var_name] = value
                            
                        except Exception as var_ex:
                            logger.debug(f"Could not extract variable '{var_name}': {var_ex}")
                            continue
                    
                    hourly_data.append(data_point)
                
                result = {
                    'location': {
                        'latitude': latitude,
                        'longitude': longitude,
                        'actual_lat': actual_lat,
                        'actual_lon': actual_lon
                    },
                    'data_source': 'copernicus_era5',
                    'resolution': '11km',
                    'data_type': 'reanalysis',
                    'retrieved_at': datetime.now().isoformat(),
                    'hourly_data': hourly_data,
                    'data_points': len(hourly_data)
                }
                
                return result
                
        except Exception as e:
            logger.error(f"❌ Error processing NetCDF file: {e}")
            raise
    
    # Fallback methods
    
    def _get_fallback_era5_data(self, latitude: float, longitude: float, 
                                 start_date: str, end_date: str) -> Dict:
        """Generate fallback ERA5 data when API unavailable"""
        
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')
        
        hours = int((end_dt - start_dt).total_seconds() / 3600) + 24
        
        hourly_data = []
        for i in range(hours):
            dt = start_dt + timedelta(hours=i)
            
            # Generate seasonal patterns
            day_of_year = dt.timetuple().tm_yday
            hour_of_day = dt.hour
            
            # Temperature with daily and seasonal cycles
            base_temp = 20 + 10 * np.sin(2 * np.pi * day_of_year / 365)
            daily_variation = 8 * np.sin(2 * np.pi * (hour_of_day - 6) / 24)
            temperature = base_temp + daily_variation
            
            data_point = {
                'timestamp': dt.isoformat(),
                'latitude': latitude,
                'longitude': longitude,
                '2m_temperature': temperature + 273.15,  # Kelvin
                'total_precipitation': 0.001 if np.random.random() > 0.9 else 0,
                'surface_pressure': 101325,
                'total_cloud_cover': 0.3,
                '2m_dewpoint_temperature': temperature - 5 + 273.15
            }
            
            hourly_data.append(data_point)
        
        return {
            'location': {'latitude': latitude, 'longitude': longitude},
            'data_source': 'fallback',
            'note': 'Copernicus API unavailable - using modeled data',
            'hourly_data': hourly_data,
            'data_points': len(hourly_data)
        }
    
    def _get_fallback_soil_moisture(self, latitude: float, longitude: float,
                                    start_date: str, end_date: str) -> Dict:
        """Generate fallback soil moisture data"""
        base_data = self._get_fallback_era5_data(latitude, longitude, start_date, end_date)
        
        # Add soil moisture estimates
        for point in base_data['hourly_data']:
            point['volumetric_soil_water_layer_1'] = 0.25
            point['volumetric_soil_water_layer_2'] = 0.28
            point['soil_temperature_level_1'] = point['2m_temperature'] - 2
        
        return base_data
    
    def _get_fallback_solar_radiation(self, latitude: float, longitude: float,
                                      start_date: str, end_date: str) -> Dict:
        """Generate fallback solar radiation data"""
        base_data = self._get_fallback_era5_data(latitude, longitude, start_date, end_date)
        
        # Add solar radiation estimates
        for point in base_data['hourly_data']:
            dt = datetime.fromisoformat(point['timestamp'])
            hour = dt.hour
            
            # Simple solar radiation model
            if 6 <= hour <= 18:
                solar_angle = np.sin(np.pi * (hour - 6) / 12)
                point['surface_solar_radiation_downwards'] = 800 * solar_angle
            else:
                point['surface_solar_radiation_downwards'] = 0
        
        return base_data


# Module-level functions

_api_instance = None

def get_api_instance() -> CopernicusWeatherAPI:
    """Get singleton API instance"""
    global _api_instance
    if _api_instance is None:
        _api_instance = CopernicusWeatherAPI()
    return _api_instance


def get_era5_hourly_data(latitude: float, longitude: float,
                         start_date: str, end_date: str) -> Dict:
    """Convenience function to get ERA5 hourly data"""
    return get_api_instance().get_era5_hourly_data(latitude, longitude, start_date, end_date)


def get_era5_soil_moisture(latitude: float, longitude: float,
                          start_date: str, end_date: str) -> Dict:
    """Convenience function to get ERA5 soil moisture"""
    return get_api_instance().get_era5_soil_moisture(latitude, longitude, start_date, end_date)


# Test the module
if __name__ == "__main__":
    print("🛰️ Testing Copernicus ERA5 Weather API Handler")
    print("=" * 80)
    
    # Test coordinates (Punjab, India)
    lat, lng = 30.3398, 76.3869
    start = "2025-10-01"
    end = "2025-10-03"
    
    try:
        api = CopernicusWeatherAPI()
        
        print(f"\n📍 API Status: {'✅ Available' if api.is_available() else '⚠️ Fallback Mode'}")
        
        print(f"\n📍 Test 1: ERA5 Hourly Data")
        print(f"   Period: {start} to {end}")
        data = api.get_era5_hourly_data(lat, lng, start, end)
        print(f"   Data points: {data.get('data_points', 0)}")
        print(f"   Source: {data.get('data_source', 'unknown')}")
        
        print("\n✅ Tests complete!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
