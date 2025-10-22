"""
Check Weather Flask endpoints using the Flask test client.
This script imports the weather Flask backend, creates an app test client and calls
several endpoints (health, debug, integrated) to print JSON outputs for inspection.

Run from project root with the cropeye python interpreter:
& "C:\\Users\\akshi\\anaconda3\\envs\\cropeye\\python.exe" "D:\\CropEye1\\backend\\scripts\\check_weather_endpoints.py"
"""

import json
import os
import sys
import pathlib
import importlib.util

# Ensure project root is on sys.path so imports work when running the script
REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# Try normal import first, fall back to loading by file path
try:
    from backend.GIS.Weather import weather_flask_backend as wb
except Exception:
    module_path = REPO_ROOT.joinpath('backend', 'GIS', 'Weather', 'weather_flask_backend.py')
    spec = importlib.util.spec_from_file_location('weather_flask_backend', str(module_path))
    if spec is None or spec.loader is None:
        raise ImportError(f'Could not create module spec for {module_path}')
    wb = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(wb)

app = wb.app

with app.app_context():
    # Ensure the weather_collector is initialized for the test client.
    # If the backend module didn't initialize it earlier, create a simplified collector here.
    try:
        from backend.GIS.Weather.weather_data_collector import WeatherDataCollector
        # instantiate and attach to the backend module so endpoints use it
        from typing import cast, Any
        cast(Any, wb).weather_collector = WeatherDataCollector()
    except Exception as e:
        print('Could not instantiate WeatherDataCollector:', e)

    client = app.test_client()

    endpoints = [
        ('GET', '/api/weather/health'),
        ('GET', '/api/weather/debug'),
        # integrated requires lat/lng; use a safe sample
        ('GET', '/api/weather/integrated?lat=30.3398&lng=76.3869&include_soil=false&include_ndvi=true')
    ]

    for method, path in endpoints:
        try:
            print(f'\n--- Calling {method} {path} ---')
            if method == 'GET':
                r = client.get(path)
            else:
                r = client.open(path, method=method)

            print('Status code:', r.status_code)
            try:
                print(json.dumps(r.get_json(), indent=2))
            except Exception as e:
                print('Could not decode JSON response:', e)
        except Exception as e:
            print('Request failed:', e)
