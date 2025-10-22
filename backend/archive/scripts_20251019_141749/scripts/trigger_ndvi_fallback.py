# Ensure backend package root is on sys.path
import os
import sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
	sys.path.insert(0, ROOT)

from GIS.Weather.weather_data_collector import WeatherDataCollector

w = WeatherDataCollector()
# force unreachable NDVI microservice
w.ndvi_api_url = 'http://127.0.0.1:59999/api/ndvi/calculate'
res = w._get_ndvi_data(30.3398,76.3869)
if res is None:
	print('NDVI request failed; no data returned')
else:
	print('NDVI payload keys:', list(res.keys()))
	print('report_image:', res.get('report_image'))
