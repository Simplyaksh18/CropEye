
"""
NDVI Integration Helper - Updated for Windows GIS Structure
Integrates with existing NDVI module in D:/CropEye1/backend/GIS/NDVI
"""

import os
import sys
import logging
import numpy as np

logger = logging.getLogger(__name__)

class NDVIIntegration:
    def __init__(self):
        """Initialize NDVI integration with existing module"""
        self.ndvi_module_available = False
        self.calculator = None
        self.downloader = None
        self.create_sample_ndvi_data = None

        # Prefer absolute package imports from backend.ndvi; fallback to loading files
        try:
            logger.info("🌿 Attempting to import NDVI modules via package 'backend.ndvi'")
            import importlib

            sentinel_pkg = importlib.import_module('backend.ndvi.sentinel_downloader')
            calculator_pkg = importlib.import_module('backend.ndvi.ndvi_calculator')

            CopernicusDataDownloader = getattr(sentinel_pkg, 'CopernicusDataDownloader', None)
            NDVICalculator = getattr(calculator_pkg, 'NDVICalculator', None)
            create_sample_ndvi_data_pkg = getattr(calculator_pkg, 'create_sample_ndvi_data', None)

            # Initialize components
            try:
                self.downloader = CopernicusDataDownloader() if CopernicusDataDownloader else None
            except Exception:
                self.downloader = None

            try:
                self.calculator = NDVICalculator() if NDVICalculator else None
            except Exception:
                self.calculator = None

            # attach helper if available
            self.create_sample_ndvi_data = create_sample_ndvi_data_pkg

            self.ndvi_module_available = bool(self.calculator or self.downloader)

            if self.ndvi_module_available:
                logger.info("✅ NDVI module integration successful via backend.ndvi")
                try:
                    known_count = len(self.calculator.known_locations) if self.calculator and hasattr(self.calculator, 'known_locations') else 0
                    logger.info(f"   Known NDVI locations: {known_count}")
                except Exception:
                    pass
            else:
                logger.warning("⚠️ backend.ndvi imported but components failed to initialize")

        except ImportError:
            # If package import fails (common when running the script directly), try loading from GIS/NDVI
            try:
                logger.info("🌿 backend.ndvi not importable; trying to load NDVI modules from backend/GIS/NDVI files")
                import importlib.util

                current_dir = os.path.dirname(os.path.abspath(__file__))
                candidate_dir = os.path.abspath(os.path.join(current_dir, '..', 'NDVI'))

                sentinel_path = os.path.join(candidate_dir, 'sentinel_downloader.py')
                calculator_path = os.path.join(candidate_dir, 'ndvi_calculator.py')

                sentinel_mod = None
                calculator_mod = None

                if os.path.exists(sentinel_path):
                    spec = importlib.util.spec_from_file_location('sentinel_downloader', sentinel_path)
                    if spec and spec.loader:
                        sentinel_mod = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(sentinel_mod)

                if os.path.exists(calculator_path):
                    spec2 = importlib.util.spec_from_file_location('ndvi_calculator', calculator_path)
                    if spec2 and spec2.loader:
                        calculator_mod = importlib.util.module_from_spec(spec2)
                        spec2.loader.exec_module(calculator_mod)

                if sentinel_mod and hasattr(sentinel_mod, 'CopernicusDataDownloader'):
                    try:
                        self.downloader = sentinel_mod.CopernicusDataDownloader()
                    except Exception:
                        self.downloader = None
                else:
                    self.downloader = None

                if calculator_mod and hasattr(calculator_mod, 'NDVICalculator'):
                    try:
                        self.calculator = calculator_mod.NDVICalculator()
                    except Exception:
                        self.calculator = None
                    self.create_sample_ndvi_data = getattr(calculator_mod, 'create_sample_ndvi_data', None)
                else:
                    self.calculator = None
                    self.create_sample_ndvi_data = None

                self.ndvi_module_available = bool(self.calculator or self.downloader)

                if self.ndvi_module_available:
                    logger.info("✅ NDVI module integration successful via GIS/NDVI files")
                else:
                    logger.warning("⚠️ NDVI files found but components failed to initialize")

            except Exception as ex:
                logger.warning(f"⚠️ Could not import NDVI modules from files: {ex}")
                logger.info("Will use fallback NDVI estimation methods")
                self.ndvi_module_available = False
                self.calculator = None
                self.downloader = None
                self.create_sample_ndvi_data = None
        except Exception as e:
            logger.error(f"❌ NDVI module integration failed with unexpected error: {e}")
            self.ndvi_module_available = False
            self.calculator = None
            self.downloader = None
            self.create_sample_ndvi_data = None

    def get_ndvi_for_location(self, latitude: float, longitude: float, days_back: int = 30):
        """Get NDVI data for a specific location using existing NDVI module"""
        if not self.ndvi_module_available:
            logger.warning("NDVI module not available, using fallback estimation")
            return self._fallback_ndvi_estimation(latitude, longitude)

        try:
            logger.info(f"🌿 Getting NDVI data for {latitude}, {longitude}")

            # First, check if we have known location data (matches NDVI module exactly)
            coord_key = f"{latitude},{longitude}"

            # Use local references and guard them to satisfy static checks
            calculator = self.calculator
            downloader = self.downloader

            # Check for exact matches in known locations
            if calculator and hasattr(calculator, 'known_locations') and coord_key in calculator.known_locations:
                known_data = calculator.known_locations[coord_key]
                logger.info(f"✅ Found exact match in NDVI module: {known_data['name']}")

                return {
                    'ndvi_value': known_data['ndvi'],
                    'ndvi_data_source': 'verified_ground_truth',
                    'data_quality': 'high',
                    'is_real_data': True,
                    'location_name': known_data['name'],
                    'health_analysis': {
                        'category': known_data['health_category'],
                        'health_score': known_data['health_score'],
                        'description': known_data['description'],
                        'crop_stage': known_data.get('crop_stage', 'Unknown')
                    },
                    'processing_details': {
                        'source': 'known_location_database',
                        'confidence': 0.95,
                        'red_band': known_data.get('red_band', 0),
                        'nir_band': known_data.get('nir_band', 0)
                    }
                }

            # Try to get real satellite data if no known location
            try:
                logger.info("📡 Attempting to get real satellite NDVI data...")
                download_result = None
                if downloader:
                    download_result = downloader.download_for_coordinates(latitude, longitude, days_back=days_back)

                    if download_result and download_result.get('red_band_path') and download_result.get('nir_band_path'):
                        # Calculate NDVI from downloaded bands (only if calculator present)
                        if calculator:
                            ndvi_result = calculator.calculate_ndvi_from_files(
                                download_result['red_band_path'],
                                download_result['nir_band_path']
                            )
                        else:
                            ndvi_result = None
                    else:
                        ndvi_result = None
                else:
                    ndvi_result = None

                    if ndvi_result and 'statistics' in ndvi_result:
                        # Safe extraction of processing details from download_result
                        dr = download_result if 'download_result' in locals() and download_result else {}

                        return {
                            'ndvi_value': ndvi_result['statistics']['mean'],
                            'ndvi_data_source': 'satellite_derived',
                            'data_quality': 'high',
                            'is_real_data': dr.get('is_real_data', True) if isinstance(dr, dict) else True,
                            'location_name': f"Satellite Location ({latitude:.4f}, {longitude:.4f})",
                            'health_analysis': self._analyze_ndvi_health(ndvi_result['statistics']['mean']),
                            'processing_details': {
                                'red_band_path': dr.get('red_band_path') if isinstance(dr, dict) else None,
                                'nir_band_path': dr.get('nir_band_path') if isinstance(dr, dict) else None,
                                'download_source': dr.get('data_source', 'copernicus') if isinstance(dr, dict) else 'copernicus',
                                'confidence': 0.90
                            }
                        }

            except Exception as e:
                logger.warning(f"Satellite NDVI retrieval failed: {e}")

            # Fallback to sample generation using NDVI module
            if self.create_sample_ndvi_data:
                logger.info("📊 Using NDVI sample data generation...")
                sample_ndvi = self.create_sample_ndvi_data(latitude, longitude)
                mean_ndvi = np.mean(sample_ndvi)

                return {
                    'ndvi_value': mean_ndvi,
                    'ndvi_data_source': 'geographic_simulation',
                    'data_quality': 'medium',
                    'is_real_data': False,
                    'location_name': f"Simulated Location ({latitude:.4f}, {longitude:.4f})",
                    'health_analysis': self._analyze_ndvi_health(mean_ndvi),
                    'processing_details': {
                        'source': 'sample_data_generation',
                        'confidence': 0.70
                    }
                }
            else:
                raise Exception("No sample data generation function available")

        except Exception as e:
            logger.error(f"❌ NDVI integration failed: {e}")
            return self._fallback_ndvi_estimation(latitude, longitude)

    def _analyze_ndvi_health(self, ndvi_value: float):
        """Analyze vegetation health from NDVI value"""
        if ndvi_value >= 0.6:
            return {
                'category': 'Excellent',
                'health_score': 95,
                'description': 'Very healthy, dense vegetation with optimal biomass',
                'recommendations': ['Continue current management practices', 'Monitor for optimal harvest timing']
            }
        elif ndvi_value >= 0.4:
            return {
                'category': 'Good',
                'health_score': 80,
                'description': 'Healthy vegetation with good coverage',
                'recommendations': ['Monitor water and nutrient levels', 'Regular field scouting recommended']
            }
        elif ndvi_value >= 0.2:
            return {
                'category': 'Moderate',
                'health_score': 60,
                'description': 'Moderate vegetation with some stress indicators',
                'recommendations': ['Check irrigation programs', 'Consider soil testing']
            }
        else:
            return {
                'category': 'Poor',
                'health_score': 30,
                'description': 'Poor vegetation health, immediate attention needed',
                'recommendations': ['Immediate intervention needed', 'Check for water/nutrient stress']
            }

    def _fallback_ndvi_estimation(self, latitude: float, longitude: float):
        """Fallback NDVI estimation when module is not available"""
        logger.info("🔄 Using fallback NDVI estimation")

        # Enhanced geographic-based NDVI estimation
        base_ndvi = 0.4  # Default

        # Regional adjustments
        if 20 <= latitude <= 40:  # Temperate agricultural regions
            if 70 <= longitude <= 85:  # India
                base_ndvi = np.random.uniform(0.45, 0.70)
            elif -100 <= longitude <= -60:  # North America  
                base_ndvi = np.random.uniform(0.50, 0.75)
            else:
                base_ndvi = np.random.uniform(0.35, 0.60)
        elif abs(latitude) < 20:  # Tropical
            base_ndvi = np.random.uniform(0.40, 0.65)
        else:  # Other regions
            base_ndvi = np.random.uniform(0.25, 0.50)

        return {
            'ndvi_value': round(base_ndvi, 4),
            'ndvi_data_source': 'fallback_estimation',
            'data_quality': 'low',
            'is_real_data': False,
            'location_name': f"Estimated Location ({latitude:.4f}, {longitude:.4f})",
            'health_analysis': self._analyze_ndvi_health(base_ndvi),
            'processing_details': {
                'source': 'geographic_fallback',
                'confidence': 0.40,
                'note': 'NDVI module not available - using geographic estimation'
            }
        }

    def get_ndvi_soil_correlation(self, ndvi_data: dict, soil_data: dict):
        """Analyze correlation between NDVI and soil properties"""
        if not ndvi_data or not soil_data:
            return {
                'correlation_available': False,
                'message': 'Insufficient data for correlation analysis'
            }

        ndvi_value = ndvi_data.get('ndvi_value', 0)
        soil_props = soil_data

        correlation_analysis = {
            'correlation_available': True,
            'ndvi_value': ndvi_value,
            'vegetation_soil_match': 'Unknown',
            'limiting_factors': [],
            'recommendations': [],
            'detailed_analysis': {}
        }

        # pH-NDVI correlation
        if 'ph' in soil_props:
            ph_value = soil_props['ph'].get('value', 7.0)
            if ndvi_value < 0.4 and (ph_value < 5.5 or ph_value > 8.5):
                correlation_analysis['limiting_factors'].append(
                    f"Soil pH ({ph_value}) outside optimal range may be limiting vegetation growth"
                )
                correlation_analysis['recommendations'].append(
                    "Consider soil pH amendment for better nutrient availability"
                )

            correlation_analysis['detailed_analysis']['ph_correlation'] = {
                'ph_value': ph_value,
                'ndvi_ph_relationship': 'Optimal' if 6.0 <= ph_value <= 7.5 else 'Suboptimal',
                'impact_on_vegetation': 'Minimal' if 6.0 <= ph_value <= 7.5 else 'Moderate to High'
            }

        # Nutrient-NDVI correlation
        for nutrient in ['nitrogen', 'phosphorus', 'potassium']:
            if nutrient in soil_props and ndvi_value < 0.5:
                nutrient_data = soil_props[nutrient]
                n_value = nutrient_data.get('value', 0)
                n_class = nutrient_data.get('classification', '')

                if 'Low' in n_class or 'Very Low' in n_class:
                    correlation_analysis['limiting_factors'].append(
                        f"Low {nutrient} levels ({n_value} ppm) may be limiting vegetation growth"
                    )
                    correlation_analysis['recommendations'].append(
                        f"Consider {nutrient} fertilization to improve plant vigor"
                    )

        # Organic matter-NDVI correlation
        if 'organic_carbon' in soil_props:
            oc_value = soil_props['organic_carbon'].get('value', 0)

            if ndvi_value > 0.6 and oc_value > 2.0:
                correlation_analysis['vegetation_soil_match'] = "Excellent - High organic matter supports healthy vegetation"
            elif ndvi_value < 0.4 and oc_value < 1.0:
                correlation_analysis['vegetation_soil_match'] = "Poor - Low organic matter limiting plant growth"
                correlation_analysis['recommendations'].append(
                    "Increase organic matter through composting or cover crops"
                )
            else:
                correlation_analysis['vegetation_soil_match'] = "Moderate - Some soil-plant growth correlation observed"

        return correlation_analysis

    def is_available(self):
        """Check if NDVI module integration is available"""
        return self.ndvi_module_available

    def get_status(self):
        """Get integration status information"""
        return {
            'module_available': self.ndvi_module_available,
            'calculator_initialized': self.calculator is not None,
            'downloader_initialized': self.downloader is not None,
            'known_locations': len(self.calculator.known_locations) if self.calculator and hasattr(self.calculator, 'known_locations') else 0,
            'import_path': 'D:/CropEye1/backend/GIS/NDVI'
        }

# Global instance
ndvi_integration = NDVIIntegration()
