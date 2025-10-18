import pytest
import requests
import os
import importlib.util
import sys


# Use an environment variable for the API base, with a sensible default.
API_BASE = os.environ.get("TEST_API_BASE", "http://127.0.0.1:5002/api")


def _load_local_flask_app():
    """Attempt to load the local Flask app (soil_flask_backend.py) and return app if available."""
    try:
        SOIL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        MODULE_PATH = os.path.join(SOIL_DIR, 'soil_flask_backend.py')
        if not os.path.exists(MODULE_PATH):
            return None
        spec = importlib.util.spec_from_file_location('soil_flask_backend', MODULE_PATH)
        if not spec or not spec.loader:
            return None
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return getattr(mod, 'app', None)
    except Exception:
        return None


FLASK_APP = _load_local_flask_app()


def _server_available():
    try:
        r = requests.get(f"{API_BASE}/health", timeout=3)
        return r.status_code == 200
    except Exception:
        return False


# Skip module when neither server nor local app are available
skip_reason = "Neither running Soil API nor local Flask app available"
pytestmark = pytest.mark.skipif((FLASK_APP is None) and (not _server_available()), reason=skip_reason)


def _get(path, client=None, timeout=10):
    if client:
        resp = client.get(path)
        return resp.status_code, resp.get_json()
    else:
        r = requests.get(f"{API_BASE}{path}", timeout=timeout)
        return r.status_code, r.json()


def _post(path, payload, client=None, timeout=60):
    if client:
        resp = client.post(path, json=payload)
        return resp.status_code, resp.get_json()
    else:
        r = requests.post(f"{API_BASE}{path}", json=payload, timeout=timeout)
        return r.status_code, r.json()


def test_api_health():
    """Test the /health endpoint using local test client or HTTP fallback."""
    client = FLASK_APP.test_client() if FLASK_APP else None
    status, body = _get('/health', client=client)
    assert status == 200
    assert isinstance(body, dict)
    assert 'status' in body


def test_integration_status():
    client = FLASK_APP.test_client() if FLASK_APP else None
    status, body = _get('/soil/integration-status', client=client)
    assert status == 200
    assert 'ndvi_integration' in body


def test_sample_analysis_with_ndvi():
    payload = {"latitude": 30.3398, "longitude": 76.3869, "include_ndvi": True, "analysis_depth": "comprehensive"}
    client = FLASK_APP.test_client() if FLASK_APP else None
    status, body = _post('/soil/analyze', payload, client=client)
    assert status == 200
    assert 'soil_properties' in body
    assert 'ndvi_provenance' in body
