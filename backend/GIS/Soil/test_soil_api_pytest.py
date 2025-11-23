try:
    import pytest  # type: ignore
except Exception:
    # Provide minimal no-op replacements so the module can be imported even if pytest
    # is not available; these allow the decorators used below to be no-ops.
    import types
    def _fixture(func):
        return func
    def _parametrize(argnames, argvalues):
        def decorator(f):
            return f
        return decorator
    pytest = types.SimpleNamespace(fixture=_fixture, mark=types.SimpleNamespace(parametrize=_parametrize))

import requests

BASE_URL = "http://127.0.0.1:5002"

@pytest.fixture
def headers():
    return {"Content-Type": "application/json"}

def test_soil_analyze_happy_path(headers):
    url = f"{BASE_URL}/api/soil/analyze"
    payload = {
        "latitude": 30.3398,
        "longitude": 76.3869,
        "depth": 30
    }
    resp = requests.post(url, json=payload, headers=headers, timeout=10)
    assert resp.status_code == 200
    data = resp.json()
    assert "soil_quality" in data

@pytest.mark.parametrize("payload", [
    {},
    {"latitude": "invalid", "longitude": "invalid", "depth": "deep"},
    {"latitude": None, "longitude": None},
    {"latitude": 1000, "longitude": 1000, "depth": 1000}
])
def test_soil_analyze_invalid_inputs(payload, headers):
    url = f"{BASE_URL}/api/soil/analyze"
    resp = requests.post(url, json=payload, headers=headers, timeout=10)
    assert resp.status_code in [400, 422]
