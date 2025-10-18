import os
import sys
import math
# Import pytest if available; use a simple guarded import and silence linters with a type ignore.
# If your editor still shows "could not be resolved", ensure the editor is using the same Python
# interpreter/environment where pytest is installed.
try:
    import pytest  # type: ignore
except Exception:  # pytest may not be available in all environments
    pytest = None

# Ensure local Soil package modules can be imported
SOIL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if SOIL_DIR not in sys.path:
    sys.path.insert(0, SOIL_DIR)

from ndvi_integration import ndvi_integration
from soil_data_collector import SoilDataCollector


def test_ndvi_integration_unknown_location():
    """NDVI integration should return a numeric ndvi_value for unknown coordinates."""
    lat, lng = 12.9716, 77.5946  # Bangalore (not listed in known locations)

    ndvi = ndvi_integration.get_ndvi_for_location(lat, lng)
    assert isinstance(ndvi, dict), f"Expected dict from NDVI integration, got {type(ndvi)}"

    ndvi_value = ndvi.get('ndvi_value')
    assert ndvi_value is not None, "NDVI value should not be None for unknown location"
    assert isinstance(ndvi_value, (int, float)), f"NDVI value must be numeric, got {type(ndvi_value)}"
    assert -1.0 <= float(ndvi_value) <= 1.0, f"NDVI value {ndvi_value} out of valid range"


def test_soil_data_collector_unknown_location():
    """SoilDataCollector should produce ndvi_correlation for unknown coordinates when include_ndvi=True."""
    lat, lng = 12.9716, 77.5946
    collector = SoilDataCollector()

    result = collector.get_soil_data(lat, lng, include_ndvi=True)
    assert isinstance(result, dict), "SoilDataCollector should return a dict"

    ndvi_corr = result.get('ndvi_correlation')
    assert ndvi_corr is not None, "ndvi_correlation should be present in soil result for include_ndvi=True"

    ndvi_value = ndvi_corr.get('ndvi_value')
    assert ndvi_value is not None, "ndvi_value should be present in ndvi_correlation"
    assert isinstance(ndvi_value, (int, float)), "ndvi_value should be numeric"
    assert -1.0 <= float(ndvi_value) <= 1.0

    # Also ensure provenance fields exist (may be None depending on downloader)
    assert 'processing_details' in ndvi_corr
