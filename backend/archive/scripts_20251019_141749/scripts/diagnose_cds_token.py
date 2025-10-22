"""Diagnose which Copernicus CDS token & URL cdsapi will load.

This script does NOT print the token value. It reports:
 - whether cdsapi is installed
 - where the token was discovered (env / file)
 - token length and whether it contains a colon
 - whether a cdsapi.Client could be created
 - the resolved client URL discovered on the client object (best-effort)

Run from repo root with your cropeye Python. Example (PowerShell):
&lt;PS&gt; & "C:/path/to/cropeye/python.exe" "D:/CropEye1/backend/scripts/diagnose_cds_token.py" &lt;/PS&gt;
"""
from __future__ import annotations
import os
import re
import json
from pathlib import Path

REPORT = {
    'cdsapi_installed': False,
    'token_source': None,
    'token_length': None,
    'token_contains_colon': None,
    'client_created': False,
    'client_url': None,
    'client_url_attr': None,
    'notes': [],
}


def _parse_cdsapirc_text(text: str):
    # Try to find url: and key: entries
    url = None
    key = None
    # Simple regex that matches lines like: url: https://... or key: 123:abcd
    m_url = re.search(r"^\s*url\s*:\s*(\S+)", text, flags=re.IGNORECASE | re.M)
    m_key = re.search(r"^\s*key\s*:\s*(\S+)", text, flags=re.IGNORECASE | re.M)
    if m_url:
        url = m_url.group(1).strip().strip('"')
    if m_key:
        key = m_key.group(1).strip().strip('"')
    return url, key


def discover_token_and_url():
    # 1) Prefer explicit env var
    env_key = os.getenv('COPERNICUS_CDS_KEY')
    env_url = os.getenv('COPERNICUS_CDS_URL')
    if env_key:
        REPORT['token_source'] = 'env:COPERNICUS_CDS_KEY'
        REPORT['token_length'] = len(env_key)
        REPORT['token_contains_colon'] = ':' in env_key
        if env_url:
            REPORT['notes'].append('COPERNICUS_CDS_URL provided via env')
            REPORT['client_url'] = env_url
        return env_key, env_url

    # 2) Search common .cdsapirc locations
    home = Path.home()
    candidates = [home / '.cdsapirc', Path.cwd() / '.cdsapirc', Path(__file__).resolve().parents[2] / '.cdsapirc', Path(__file__).resolve().parents[2] / 'backend' / '.cdsapirc']
    for p in candidates:
        try:
            if p.exists():
                txt = p.read_text(encoding='utf-8', errors='ignore')
                url, key = _parse_cdsapirc_text(txt)
                if key:
                    REPORT['token_source'] = str(p)
                    REPORT['token_length'] = len(key)
                    REPORT['token_contains_colon'] = ':' in key
                    if url:
                        REPORT['client_url'] = url
                    return key, url
        except Exception as e:
            REPORT['notes'].append(f'failed reading {p}: {e}')

    # 3) Nothing found
    REPORT['notes'].append('No COPERNICUS token found in env or common .cdsapirc locations')
    return None, None


def try_create_client(token: str | None, url: str | None):
    try:
        import cdsapi
    except Exception:
        REPORT['cdsapi_installed'] = False
        REPORT['notes'].append('cdsapi not importable in this Python environment')
        return None

    REPORT['cdsapi_installed'] = True

    client = None
    try:
        if token and url:
            # Prefer explicit creation with discovered values
            client = cdsapi.Client(url=url, key=token, verify=True)
            REPORT['notes'].append('cdsapi.Client(url=..., key=...) created')
        elif token and not url:
            client = cdsapi.Client(key=token)
            REPORT['notes'].append('cdsapi.Client(key=...) created')
        else:
            client = cdsapi.Client()
            REPORT['notes'].append('cdsapi.Client() created (reads ~/.cdsapirc or env)')
        REPORT['client_created'] = True
    except Exception as e:
        REPORT['client_created'] = False
        REPORT['notes'].append(f'Failed to create cdsapi.Client: {e}')
        return None

    # Best-effort: find a URL attribute on the client
    possible_attrs = ['url', 'api_url', 'base_url', 'host', '_url']
    for a in possible_attrs:
        v = getattr(client, a, None)
        if v:
            REPORT['client_url'] = str(v)
            REPORT['client_url_attr'] = a
            break

    return client


def main():
    token, url = discover_token_and_url()
    # If token present, we've already populated REPORT fields
    if token is None:
        # still try to create a client so cdsapi can read user's ~/.cdsapirc
        client = try_create_client(None, None)
    else:
        client = try_create_client(token, url)

    # If we created a client but no client_url was discovered, try reading fallback attributes
    if REPORT.get('client_created') and REPORT.get('client_url') is None and client is not None:
        try:
            # attempt to inspect the client's internal config if present
            cfg = getattr(client, 'url', None) or getattr(client, 'api_url', None) or getattr(client, '_url', None)
            if cfg:
                REPORT['client_url'] = str(cfg)
        except Exception:
            pass

    # final safety: don't include token value
    if REPORT['token_length'] is None:
        REPORT['token_length'] = None

    print(json.dumps(REPORT, indent=2))


if __name__ == '__main__':
    main()
