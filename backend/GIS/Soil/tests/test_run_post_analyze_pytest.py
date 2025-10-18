import pytest
import requests
import os

API_BASE = os.environ.get('TEST_API_BASE', 'http://127.0.0.1:5002/api')


def _server_available():
    try:
        r = requests.get(f"{API_BASE}/health", timeout=3)
        return r.status_code == 200
    except Exception:
        return False


pytestmark = pytest.mark.skipif(not _server_available(), reason="Soil API not running")


def test_post_analyze_endpoint():
    url = f"{API_BASE}/soil/analyze"
    payload = {
        'latitude': 28.6139,
        'longitude': 77.2090,
        'include_ndvi': True,
        'analysis_depth': 'comprehensive'
    }

    resp = requests.post(url, json=payload, timeout=120)
    assert resp.status_code == 200
    data = resp.json()
    assert 'soil_properties' in data
