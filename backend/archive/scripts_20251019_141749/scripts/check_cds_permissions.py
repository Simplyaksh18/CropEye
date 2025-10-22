"""Check Copernicus CDS account permissions by probing lightweight endpoints.

This script will:
 - instantiate the CopernicusWeatherAPI (to reuse existing client logic)
 - attempt GET requests to a few lightweight CDS endpoints using the client's session
 - print a JSON report with HTTP status codes and short response snippets

Run with your cropeye Python to use the same environment: 
& "C:/path/to/cropeye/python.exe" "D:/CropEye1/backend/scripts/check_cds_permissions.py"
"""
from __future__ import annotations
import json
from pathlib import Path
import sys
from pathlib import Path

# ensure backend package is importable when running from repo root
root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(root / 'backend'))

from GIS.Weather import copernicus_weather_api as cwa

report = {
    'client_created': False,
    'client_url': None,
    'checks': [],
}


def short(text: str, n: int = 300):
    return text[:n].replace('\n', ' ') if text else ''


def main():
    api = cwa.get_api_instance()
    client = getattr(api, 'client', None)
    report['client_created'] = api.is_available() and client is not None

    if client is None:
        report['error'] = 'No cdsapi client available (cdsapi missing or client not initialized)'
        print(json.dumps(report, indent=2))
        return

    # Best-effort client URL
    client_url = getattr(client, 'url', None) or getattr(client, 'api_url', None) or None
    report['client_url'] = client_url

    # Candidate endpoints to probe (relative to client_url)
    base = client_url.rstrip('/') if client_url else ''
    endpoints = [
        '/v2/resources',
        '/resources',
        '/api/v2/resources',
        '/api/status',
        '/retrieve/v1/processes'
    ]

    session = getattr(client, 'session', None)

    for ep in endpoints:
        url = (base + ep) if base else ep
        entry = {'endpoint': url, 'status': None, 'snippet': None, 'error': None}
        try:
            if session is not None:
                resp = session.get(url, timeout=30)
                entry['status'] = resp.status_code
                entry['snippet'] = short(resp.text)
            else:
                # fallback: try using client's own request method if present
                req = getattr(client, 'session', None)
                if req is not None:
                    resp = req.get(url, timeout=30)
                    entry['status'] = resp.status_code
                    entry['snippet'] = short(resp.text)
                else:
                    entry['error'] = 'No session available on client to perform GET'
        except Exception as e:
            entry['error'] = str(e)
        report['checks'].append(entry)

    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
