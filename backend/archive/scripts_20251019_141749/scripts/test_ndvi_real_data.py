#!/usr/bin/env python3
"""
Test Script for Real NDVI Data Analysis

This script calls the running `ndvi_flask_backend.py` service and explicitly
requests an analysis using real Copernicus satellite data.

Instructions:
1. Run all backend services using `python scripts/run_all_servers.py`.
2. In a separate terminal, run this script: `python GIS/NDVI/tests/test_ndvi_real_data.py`

Look for `"data_source": "copernicus_real"` in the output to confirm success.
"""

import requests
import json
import time

NDVI_API_URL = "http://localhost:5001/api/ndvi/analyze"

TEST_LOCATION = {
    "latitude": 30.3398,  # Punjab, India
    "longitude": 76.3869,
    "use_real_data": True,
    "days_back": 60  # Look back 60 days to increase chances of finding a cloud-free image
}

def main():
    """Runs the real data NDVI test."""
    print("=" * 80)
    print("🛰️  Testing Real NDVI Data Analysis from Copernicus")
    print("=" * 80)
    print(f"   Calling endpoint: {NDVI_API_URL}")
    print(f"   Requesting data for: ({TEST_LOCATION['latitude']}, {TEST_LOCATION['longitude']})")
    print("   This may take a minute as it involves a live satellite data search...")

    try:
        start_time = time.time()
        response = requests.post(NDVI_API_URL, json=TEST_LOCATION, timeout=180)
        end_time = time.time()

        print(f"\n   -> HTTP Status Code: {response.status_code}")
        print(f"   -> Request completed in {end_time - start_time:.2f} seconds.")

        response.raise_for_status()
        data = response.json()

        print("\n--- Full Analysis Response ---")
        print(json.dumps(data, indent=2))

        print("\n--- Verification ---")
        if data.get('data_source') == 'copernicus_real' or data.get('verification', {}).get('data_quality') == 'satellite_derived':
            print("\n✅ SUCCESS: The service successfully used REAL satellite data!")
        else:
            print("\n⚠️  WARNING: The service fell back to simulated data. Check the NDVI service logs for errors (e.g., cloud cover, API issues).")

    except requests.exceptions.RequestException as e:
        print(f"\n❌ FAILED: Could not connect to the NDVI service. Is it running?")
        print(f"   Error: {e}")

if __name__ == "__main__":
    main()