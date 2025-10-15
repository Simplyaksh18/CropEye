"""NDVI package for backend - re-exports useful modules.

This file attempts a normal relative import first. If the repository layout places
the NDVI modules under `backend/GIS/NDVI/` (as in this project), fall back to
loading the module files directly using importlib so `from backend.ndvi import ...`
works for consumers.
"""
import os
import importlib.util
import logging

logger = logging.getLogger(__name__)

def _load_from_path(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    return None

# Try to import NDVI modules in a robust, dynamic way to avoid static unresolved import warnings
try:
    import importlib

    pkg_dir = os.path.dirname(__file__)

    sentinel_pkg = None
    calculator_pkg = None

    # 1) Try absolute package import (works when project root is on sys.path)
    try:
        sentinel_pkg = importlib.import_module('backend.ndvi.sentinel_downloader')
        calculator_pkg = importlib.import_module('backend.ndvi.ndvi_calculator')
    except Exception:
        # 2) Try package-relative import (if the package contains the modules)
        try:
            sentinel_pkg = importlib.import_module(f'{__package__}.sentinel_downloader')
            calculator_pkg = importlib.import_module(f'{__package__}.ndvi_calculator')
        except Exception:
            sentinel_pkg = None
            calculator_pkg = None

    # 3) Fallback: load files from backend/GIS/NDVI if present
    if not (sentinel_pkg and calculator_pkg):
        candidate_dir = os.path.abspath(os.path.join(pkg_dir, '..', 'GIS', 'NDVI'))

        sentinel_path = os.path.join(candidate_dir, 'sentinel_downloader.py')
        calculator_path = os.path.join(candidate_dir, 'ndvi_calculator.py')

        sentinel_mod = None
        calculator_mod = None

        try:
            if os.path.exists(sentinel_path):
                sentinel_mod = _load_from_path('backend.ndvi.sentinel_downloader', sentinel_path)
            if os.path.exists(calculator_path):
                calculator_mod = _load_from_path('backend.ndvi.ndvi_calculator', calculator_path)

            if sentinel_mod:
                sentinel_pkg = sentinel_mod
            if calculator_mod:
                calculator_pkg = calculator_mod

        except Exception as e:
            logger.warning(f"Failed to load NDVI modules from GIS/NDVI: {e}")

    # Expose symbols if we found them, otherwise None
    if sentinel_pkg and hasattr(sentinel_pkg, 'CopernicusDataDownloader'):
        CopernicusDataDownloader = getattr(sentinel_pkg, 'CopernicusDataDownloader')
    else:
        CopernicusDataDownloader = None

    if calculator_pkg and hasattr(calculator_pkg, 'NDVICalculator'):
        NDVICalculator = getattr(calculator_pkg, 'NDVICalculator')
        create_sample_ndvi_data = getattr(calculator_pkg, 'create_sample_ndvi_data', None)
    else:
        NDVICalculator = None
        create_sample_ndvi_data = None

except Exception as e:
    logger.warning(f"Failed to dynamically load NDVI modules: {e}")
    CopernicusDataDownloader = None
    NDVICalculator = None
    create_sample_ndvi_data = None

__all__ = [
    "CopernicusDataDownloader",
    "NDVICalculator",
    "create_sample_ndvi_data",
]
