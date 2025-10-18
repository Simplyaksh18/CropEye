import socket
try:
    import requests
except Exception as e:
    requests = None
import json

host = 'rest.soilgrids.org'
lat = 12.9716
lon = 77.5946

print('Checking SoilGrids host resolution for', host)
try:
    ip = socket.gethostbyname(host)
    print('Resolved', host, '->', ip)
except Exception as e:
    print('DNS resolution failed:', e)

if not requests:
    print('\nrequests library not available in this environment; cannot perform HTTP request')
else:
    url = f'https://{host}/query?lon={lon}&lat={lat}&property=phh2o,soc,nitrogen,bdod,clay,sand,silt&depth=0-5cm&value=mean'
    print('\nRequesting:', url)
    try:
        r = requests.get(url, timeout=15)
        print('HTTP status:', r.status_code)
        # print pretty JSON up to a limit
        text = r.text
        if len(text) > 4000:
            print('Response (truncated to 4000 chars):')
            print(text[:4000])
        else:
            print('Response:')
            print(text)
    except Exception as e:
        print('HTTP request failed:', repr(e))
