import os
import requests


def test_pest_used_flags_when_disabled():
    # ensure flag disables real weather usage
    os.environ['USE_REAL_WEATHER'] = 'false'

    resp = requests.post('http://127.0.0.1:5006/api/threats/integrated', json={
        'latitude': 30.3398,
        'longitude': 76.3869,
        'crop_type': 'wheat'
    }, timeout=5)

    assert resp.status_code == 200
    j = resp.json()
    assert 'used_weather_service' in j
    assert j['used_weather_service'] is False
    assert isinstance(j.get('used_fallback_reason', {}), dict)
    assert 'weather' in j['used_fallback_reason']


def test_water_used_flags_when_disabled():
    # ensure flags disable real weather/soil usage
    os.environ['USE_REAL_WEATHER'] = 'false'
    os.environ['USE_REAL_SOIL'] = 'false'

    resp = requests.post('http://127.0.0.1:5005/api/water/irrigation/integrated', json={
        'latitude': 30.3398,
        'longitude': 76.3869,
        'crop_type': 'wheat',
        'growth_stage': 'mid'
    }, timeout=5)

    assert resp.status_code == 200
    j = resp.json()
    assert 'used_weather_service' in j and j['used_weather_service'] is False
    assert 'used_soil_service' in j and j['used_soil_service'] is False
    assert isinstance(j.get('used_fallback_reason', {}), dict)
    assert 'weather' in j['used_fallback_reason']
    assert 'soil' in j['used_fallback_reason']
