"""
Quick test script to call the Flask integrated endpoint using the Flask test client.
This script imports the `app` object from `weather_flask_backend.py` and performs a GET
against /api/weather/integrated with coordinates that trigger the NDVI fallback.

Run from the `backend/GIS/Weather` directory with:

    python test_integrated_endpoint.py

"""
import json
import weather_flask_backend as wf
app = wf.app
weather_collector = getattr(wf, "weather_collector", None)

# Use Flask's test client to avoid starting the server
with app.test_client() as client:
    # Step 1: Get your location from your IP address
    print("🌍 Detecting your location via IP address...")
    if weather_collector is not None and hasattr(weather_collector, "get_location_from_ip"):
        location_data = weather_collector.get_location_from_ip()
    else:
        # Fallback to a module-level function if available
        get_loc = getattr(wf, "get_location_from_ip", None)
        if callable(get_loc):
            location_data = get_loc()
        else:
            print("⚠️ weather_collector.get_location_from_ip not available; cannot auto-detect location.")
            location_data = None

    if not location_data:
        print("❌ Could not determine your location. Please check your internet connection.")
    else:
        # location_data may be a dict or an object with attributes; support both safely
        if isinstance(location_data, dict):
            lat = location_data.get('latitude')
            lng = location_data.get('longitude')
            city = location_data.get('city', 'Unknown City')
        else:
            lat = getattr(location_data, 'latitude', None)
            lng = getattr(location_data, 'longitude', None)
            city = getattr(location_data, 'city', 'Unknown City')

        if lat is None or lng is None:
            print("❌ Location data is incomplete (missing latitude/longitude).")
        else:
            print(f"✅ Location detected: {city} ({lat}, {lng})")

            # Step 2: Call the integrated endpoint with your coordinates
            params = {
                'lat': lat,
                'lng': lng,
                'include_ndvi': 'true',
                'include_soil': 'false',
                'coordinate_source': 'gps_auto_ip'
            }
            print("\n🌦️ Fetching integrated weather analysis for your location...")
            resp = client.get('/api/weather/integrated', query_string=params)
            print('Status code:', resp.status_code)
            try:
                data = resp.get_json()
                print(json.dumps(data, indent=2))
            except Exception as e:
                print('Failed to parse JSON response:', e)
                print(resp.data)
