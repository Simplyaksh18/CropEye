import os
import importlib.util


# Load the Flask app module by path to avoid PYTHONPATH issues when running pytest
SOIL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
import sys
if SOIL_DIR not in sys.path:
    sys.path.insert(0, SOIL_DIR)

MODULE_PATH = os.path.abspath(os.path.join(SOIL_DIR, 'soil_flask_backend.py'))
spec = importlib.util.spec_from_file_location('soil_flask_backend', MODULE_PATH)
assert spec is not None, f"Cannot create module spec for {MODULE_PATH}"
assert spec.loader is not None, f"No loader available for module spec from {MODULE_PATH}"
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
flask_app = getattr(mod, 'app')


def test_ndvi_debug_endpoint_running():
    """Sanity test: NDVI debug endpoint responds with expected structure for a known coordinate.
    Uses Flask test client so no external server is required.
    """
    payload = {"latitude": 28.6139, "longitude": 77.209}

    client = flask_app.test_client()
    resp = client.post('/api/soil/ndvi/debug', json=payload)
    # Accept 200 (success) or service-unavailable responses; ensure structure is consistent
    assert resp.status_code in (200, 503, 500), f"Unexpected status: {resp.status_code} - {resp.data}"

    data = resp.get_json() or {}

    if resp.status_code == 200:
        assert 'download_result' in data
        assert 'processing_details' in data
        proc = data['processing_details']
        if proc:
            assert isinstance(proc, dict)
            assert any(k in proc for k in ('red_band_path', 'nir_band_path', 'red_band_file_type', 'nir_band_file_type'))
    else:
        assert 'error' in data
