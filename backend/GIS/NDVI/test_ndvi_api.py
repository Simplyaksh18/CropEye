import requests
import json

BASE_URL = "http://127.0.0.1:5001"

def test_ndvi_analyze():
    url = f"{BASE_URL}/api/ndvi/analyze"
    payload = {
        "latitude": 30.3398,
        "longitude": 76.3869,
        "date": "2024-05-20"
    }
    response = requests.post(url, json=payload)
    print("Status Code:", response.status_code)
    print("Response JSON:", json.dumps(response.json(), indent=2))

def test_ndvi_timeseries():
    url = f"{BASE_URL}/api/ndvi/timeseries"
    payload = {
        "latitude": 30.3398,
        "longitude": 76.3869,
        "start_date": "2024-05-01",
        "end_date": "2024-05-31"
    }
    response = requests.post(url, json=payload)
    print("Status Code:", response.status_code)
    print("Response JSON:", json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    print("Testing /api/ndvi/analyze endpoint")
    test_ndvi_analyze()
    print("\nTesting /api/ndvi/timeseries endpoint")
    test_ndvi_timeseries()
