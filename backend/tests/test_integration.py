import os
import requests
import pytest

BASE = os.getenv('MAIN_API_URL', 'http://127.0.0.1:5000')

@pytest.mark.parametrize('path,method', [
    ('/api/health', 'get'),
    ('/api/health/aggregate', 'get'),
    ('/api/crop/list', 'get'),
])
def test_endpoint_up(path, method):
    url = BASE + path
    try:
        resp = getattr(requests, method)(url, timeout=5)
    except requests.RequestException:
        pytest.skip(f"Unable to reach {url}")
    assert resp.status_code in (200, 503)


def test_recommend_sample():
    url = BASE + '/api/crop/recommend'
    payload = {
        'latitude': 30.8,
        'longitude': 75.8,
        'ph': 7.1,
        'rainfall': 900,
        'temp_mean': 30,
        'ndvi': 0.62
    }
    try:
        resp = requests.post(url, json=payload, timeout=8)
    except requests.RequestException:
        pytest.skip('Recommend endpoint not reachable')
    assert resp.status_code in (200, 503)
    # If service is available, assert shape
    if resp.status_code == 200:
        j = resp.json()
        assert 'recommendations' in j or 'success' in j
