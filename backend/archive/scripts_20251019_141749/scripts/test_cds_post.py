"""Attempt a minimal POST to the CDS retrieve/process endpoint using the client's session.

This script re-uses the CopernicusWeatherAPI client and attempts to POST a small
request to the retrieve processes endpoint to see whether POST operations are permitted.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(root / 'backend'))

from GIS.Weather import copernicus_weather_api as cwa


def main():
    api = cwa.get_api_instance()
    client = getattr(api, 'client', None)

    out = {'client_created': api.is_available() and client is not None, 'post_check': None}

    if client is None:
        out['post_check'] = 'no client available'
        print(json.dumps(out, indent=2))
        return

    # Attempt to POST a very small request to the 'processes' endpoint
    base = getattr(client, 'url', None) or getattr(client, 'api_url', None) or ''
    url = base.rstrip('/') + '/retrieve/v1/processes'

    session = getattr(client, 'session', None)
    if session is None:
        out['post_check'] = 'client has no session object to perform POST'
        print(json.dumps(out, indent=2))
        return

    try:
        # perform a POST with minimal payload; the CDS server may require different structure,
        # so we only want to see if the server allows POST at this endpoint from your token.
        payload = {'dummy': 'ping'}
        resp = session.post(url, json=payload, timeout=30)
        out['post_check'] = {'status_code': resp.status_code, 'text_snippet': resp.text[:400]}
    except Exception as e:
        out['post_check'] = {'error': str(e)}

    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
