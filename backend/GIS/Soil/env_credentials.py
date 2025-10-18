"""Environment Credentials Helper - Updated for Windows Paths
Loads credentials from root backend .env file

This module locates the root `backend/.env` file (from the Soil Analysis
subdirectory) and loads it into the environment. It also provides a small
helper to expose credential availability without printing secrets.
"""

import os
from dotenv import load_dotenv
import sys
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class EnvironmentCredentials:
    def __init__(self):
        """
        Initialize credentials from root backend .env file
        Handles Windows paths properly
        """
        # Current structure: D:\CropEye1\backend\GIS\Soil Analysis\env_credentials.py
        # Target .env file: D:\CropEye1\backend\.env

        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Go up from "Soil Analysis" -> "GIS" -> "backend"
        backend_dir = os.path.dirname(os.path.dirname(current_dir))
        env_path = os.path.join(backend_dir, '.env')

        logger.info(f"Looking for .env file at: {env_path}")

        if os.path.exists(env_path):
            load_dotenv(env_path)
            logger.info("✅ Environment variables loaded from root backend .env")
        else:
            logger.warning(f"⚠️ .env file not found at {env_path}")
            logger.info("Trying alternative paths...")

            # Try other possible locations
            alternative_paths = [
                os.path.join(current_dir, '..', '..', '.env'),  # Relative path
                os.path.join(os.getcwd(), '.env'),              # Current working directory
                os.path.join('D:', 'CropEye1', 'backend', '.env') # Absolute Windows path
            ]

            for alt_path in alternative_paths:
                abs_alt_path = os.path.abspath(alt_path)
                if os.path.exists(abs_alt_path):
                    load_dotenv(abs_alt_path)
                    logger.info(f"✅ Environment variables loaded from: {abs_alt_path}")
                    break
            else:
                logger.warning("❌ Could not find .env file in any expected location")

        # Load Copernicus credentials
        self.COPERNICUS_USERNAME = os.getenv('COPERNICUS_USERNAME')
        self.COPERNICUS_PASSWORD = os.getenv('COPERNICUS_PASSWORD') 
        self.COPERNICUS_CLIENT_ID = os.getenv('COPERNICUS_CLIENT_ID')
        self.COPERNICUS_CLIENT_SECRET = os.getenv('COPERNICUS_CLIENT_SECRET')

        # Soil data API credentials (if available)
        self.SOILGRIDS_API_KEY = os.getenv('SOILGRIDS_API_KEY', '')
        self.ISRIC_API_KEY = os.getenv('ISRIC_API_KEY', '')

        # Weather API credentials
        self.OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY', '')

        # Database credentials
        self.DATABASE_URL = os.getenv('DATABASE_URL', '')

        logger.info("📋 Credentials loaded from root backend .env file")
        self._log_credential_status()

    def _log_credential_status(self):
        """Log which credentials are available (without showing actual values)"""
        credentials_status = {
            'COPERNICUS_USERNAME': bool(self.COPERNICUS_USERNAME),
            'COPERNICUS_PASSWORD': bool(self.COPERNICUS_PASSWORD),
            'COPERNICUS_CLIENT_ID': bool(self.COPERNICUS_CLIENT_ID),
            'COPERNICUS_CLIENT_SECRET': bool(self.COPERNICUS_CLIENT_SECRET),
            'SOILGRIDS_API_KEY': bool(self.SOILGRIDS_API_KEY),
        }

        logger.info("📋 Credential availability:")
        for cred, available in credentials_status.items():
            status = "✅ Available" if available else "❌ Missing"
            logger.info(f"   {cred}: {status}")

    def set_environment_variables(self):
        """Set environment variables for the current session.

        Also attempt to set a sane PROJ_LIB on Windows so rasterio/GDAL will
        use a compatible proj.db (avoiding system PostGIS proj.db conflicts).
        """
        env_vars = {
            'COPERNICUS_USERNAME': self.COPERNICUS_USERNAME,
            'COPERNICUS_PASSWORD': self.COPERNICUS_PASSWORD,
            'COPERNICUS_CLIENT_ID': self.COPERNICUS_CLIENT_ID,
            'COPERNICUS_CLIENT_SECRET': self.COPERNICUS_CLIENT_SECRET,
            'SOILGRIDS_API_KEY': self.SOILGRIDS_API_KEY,
            'ISRIC_API_KEY': self.ISRIC_API_KEY,
        }

        for key, value in env_vars.items():
            if value:
                os.environ[key] = value

        # PROJ_LIB shim: only set if not already set in the environment
        if not os.environ.get('PROJ_LIB'):
            candidates = []
            conda_prefix = os.environ.get('CONDA_PREFIX')
            if conda_prefix:
                candidates.append(Path(conda_prefix) / 'Library' / 'share' / 'proj')
                candidates.append(Path(conda_prefix) / 'share' / 'proj')

            # sys.prefix can be a virtualenv or interpreter install
            if sys.prefix:
                candidates.append(Path(sys.prefix) / 'Library' / 'share' / 'proj')
                candidates.append(Path(sys.prefix) / 'share' / 'proj')

            # Common OSGeo4W install path on Windows
            candidates.append(Path(r"C:\OSGeo4W64\share\proj"))

            # Program Files variants (ArcGIS or other installers)
            program_files = os.environ.get('PROGRAMFILES', r"C:\Program Files")
            candidates.append(Path(program_files) / 'ArcGIS' / 'PROJ' / 'share' / 'proj')

            chosen = None
            for p in candidates:
                try:
                    if p.exists() and any(p.iterdir()):
                        chosen = p
                        break
                except Exception:
                    continue

            if chosen:
                os.environ['PROJ_LIB'] = str(chosen)
                logger.info(f"PROJ_LIB set to: {chosen}")
            else:
                logger.info("No PROJ_LIB candidate found; leaving PROJ_LIB unset if not present")

        logger.info("🔧 Environment variables set for current session")
        return True

    def has_copernicus_credentials(self):
        """Check if Copernicus credentials are available"""
        return bool(self.COPERNICUS_USERNAME and self.COPERNICUS_PASSWORD)

# Global instance
env_creds = EnvironmentCredentials()
