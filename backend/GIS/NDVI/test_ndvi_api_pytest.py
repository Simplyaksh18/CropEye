import pytest  # type: ignore
import requests

BASE_URL = "http://127.0.0.1:5001"

@pytest.fixture
def headers():
    return {"Content-Type": "application/json"}

def test_ndvi_analyze_happy_path(headers):
    url = f"{BASE_URL}/api/ndvi/analyze"
    payload = {
        "latitude": 30.3398,
        "longitude": 76.3869,
        "date": "2024-05-20"
    }
    resp = requests.post(url, json=payload, headers=headers, timeout=10)
    assert resp.status_code == 200
    data = resp.json()
    assert "ndvi_index" in data

@pytest.mark.parametrize("payload", [
    {},  # empty
    {"latitude": "invalid", "longitude": "invalid", "date": "not-a-date"},
    {"latitude": None, "longitude": None},
    {"latitude": 1000, "longitude": 1000, "date": "2024-05-20"}
])
def test_ndvi_analyze_invalid_inputs(payload, headers):
    url = f"{BASE_URL}/api/ndvi/analyze"
    resp = requests.post(url, json=payload, headers=headers, timeout=10)
    assert resp.status_code in [400, 422]

def test_ndvi_timeseries_happy_path(headers):
    url = f"{BASE_URL}/api/ndvi/timeseries"
    payload = {
        "latitude": 30.3398,
        "longitude": 76.3869,
        "start_date": "2024-05-01",
        "end_date": "2024-05-31"
    }
    resp = requests.post(url, json=payload, headers=headers, timeout=10)
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data.get("timeseries"), list)

@pytest.mark.parametrize("payload", [
    {},  # empty
    {"latitude": "x", "longitude": "y", "start_date": "a", "end_date": "b"},
    {"latitude": None, "longitude": None},
    {"latitude": 90, "longitude": 200, "start_date": "2024-05-01", "end_date": "2024-05-31"}
])
def test_ndvi_timeseries_invalid_inputs(payload, headers):
    url = f"{BASE_URL}/api/ndvi/timeseries"
    resp = requests.post(url, json=payload, headers=headers, timeout=10)
    assert resp.status_code in [400, 422]
