import os
import sys
import json
import pytest

# Ensure local modules load
SOIL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if SOIL_DIR not in sys.path:
    sys.path.insert(0, SOIL_DIR)

try:
    from ndvi_integration import ndvi_integration
    from soil_data_collector import SoilDataCollector
except Exception:
    ndvi_integration = None
    SoilDataCollector = None


@pytest.mark.skipif(ndvi_integration is None or SoilDataCollector is None, reason="NDVI modules not importable")
def test_ndvi_and_soil_integration_direct():
    lat, lng = 12.9716, 77.5946

    # Ensure static analyzers and runtime see these are present
    assert ndvi_integration is not None
    nd = ndvi_integration.get_ndvi_for_location(lat, lng)
    assert isinstance(nd, dict)
    assert 'ndvi_value' in nd

    assert SoilDataCollector is not None
    collector = SoilDataCollector()
    res = collector.get_soil_data(lat, lng, include_ndvi=True)
    assert isinstance(res, dict)
    # ndvi_correlation may be present
    assert 'ndvi_correlation' in res

