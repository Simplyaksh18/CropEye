import requests
import json

BASE_URL = "http://localhost:5001/api"

def test_health():
    url = f"{BASE_URL}/health"
    r = requests.get(url)
    print("Health endpoint status:", r.status_code)
    print("Response:", r.json())

def test_ndvi_analyze():
    url = f"{BASE_URL}/ndvi/analyze"
    test_cases = [
        {"latitude": 40.7128, "longitude": -74.0060, "date": "2023-01-01"},
        {"latitude": 40.7128, "longitude": -74.0060},  # no date, fallback to 7 days ago
        {},  # no data, expect error
        {"latitude": None, "longitude": -74.0060},  # missing lat, error
        {"latitude": 40.7128, "longitude": None}   # missing lon, error
    ]
    for i, data in enumerate(test_cases):
        r = requests.post(url, json=data)
        print(f"NDVI Analyze Test case {i+1}: status={r.status_code}")
        try:
            print("Response:", r.json())
        except json.JSONDecodeError:
            print("Response content could not be decoded as JSON")

def test_ndvi_timeseries():
    url = f"{BASE_URL}/ndvi/timeseries"
    test_cases = [
        {
            "latitude": 40.7128,
            "longitude": -74.0060,
            "start_date": "2023-01-01",
            "end_date": "2023-01-31"
        },
        {
            "latitude": None,
            "longitude": -74.0060,
            "start_date": "2023-01-01",
            "end_date": "2023-01-31"
        }  # missing latitude, expecting error
    ]

    for i, data in enumerate(test_cases):
        r = requests.post(url, json=data)
        print(f"NDVI Timeseries Test case {i+1}: status={r.status_code}")
        try:
            print("Response:", r.json())
        except json.JSONDecodeError:
            print("Response content could not be decoded as JSON")

def test_env_check():
    url = f"{BASE_URL}/env_check"
    r = requests.get(url)
    print("Env check endpoint status:", r.status_code)
    print("Response:", r.json())

if __name__ == "__main__":
    print("Starting thorough tests on NDVI Flask backend...\n")

    print("Testing /api/health")
    test_health()

    print("\nTesting /api/ndvi/analyze")
    test_ndvi_analyze()

    print("\nTesting /api/ndvi/timeseries")
    test_ndvi_timeseries()

    print("\nTesting /api/env_check")
    test_env_check()

    print("\nAll tests completed.")
