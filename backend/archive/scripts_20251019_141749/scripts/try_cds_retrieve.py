"""Try a tiny Copernicus CDS ERA5 retrieve to validate .cdsapirc and netCDF path.

This script is conservative: it requests a single day and a single variable at native grid,
writes a small netCDF to the backend temp directory (or /tmp), processes it via
netCDF4 if available, then removes the file and prints a short summary.

Run from repo root: python backend/scripts/try_cds_retrieve.py
"""
from __future__ import annotations
import os
import sys
import json
from pathlib import Path
import tempfile
import shutil

# add backend to path so imports from the project work
root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(root / 'backend'))

from GIS.Weather import copernicus_weather_api as cwa

out = {
    'cdsapirc_found': [],
    'client_initialized': False,
    'attempted_retrieve': False,
    'retrieve_success': False,
    'error': None,
    'file_path': None,
    'data_points': None,
    'data_source': None,
}

# check usual .cdsapirc locations
home = Path(os.path.expanduser('~'))
candidates = [home / '.cdsapirc', Path.cwd() / '.cdsapirc', Path('D:/CropEye1/backend/.cdsapirc')]
out['cdsapirc_found'] = [str(p) for p in candidates if p.exists()]

api = cwa.CopernicusWeatherAPI()
out['client_initialized'] = api.is_available()

if not api.is_available():
    out['error'] = 'CDS client not initialized (missing .cdsapirc or cdsapi library)'
    print(json.dumps(out))
    sys.exit(0)

# conservative retrieve params
lat, lon = 30.3398, 76.3869
start = '2025-10-01'
end = '2025-10-01'
vars = ['2m_temperature']

out['attempted_retrieve'] = True

# defaults
res = None
saved_path = None
file_saved = False
out['original_file_path'] = None

try:
    res = api.get_era5_hourly_data(lat, lon, start, end, variables=vars)
    out['data_points'] = res.get('data_points')
    fp = res.get('file_path')
    # capture data source reported by the API (copernicus_era5 or fallback)
    out['data_source'] = res.get('data_source')
    # surface any CDS diagnostic fields returned by the API
    for k in ('cds_error', 'cds_http_status', 'cds_http_text', 'cds_request'):
        if k in res:
            out[k] = res.get(k)

    # Preserve the downloaded NetCDF in outputs. The copernicus client sometimes
    # writes to a different temp filename, so search the temp dir for the newest
    # .nc if the returned output_path is missing.
    outputs_dir = Path(root) / 'backend' / 'GIS' / 'Weather' / 'outputs'
    outputs_dir.mkdir(parents=True, exist_ok=True)

    candidate = None
    if fp:
        out['original_file_path'] = str(fp)
    if fp and Path(fp).exists():
        candidate = Path(fp)
    else:
        # search temp dir
        tmpdir = Path(tempfile.gettempdir()) / 'cropeye_weather'
        if tmpdir.exists():
            nc_files = list(tmpdir.glob('*.nc'))
            if nc_files:
                candidate = max(nc_files, key=lambda p: p.stat().st_mtime)
    # If we found a candidate .nc file in temp, copy it into project outputs
    if candidate and candidate.exists():
        dest = outputs_dir / candidate.name
        counter = 0
        while dest.exists():
            counter += 1
            dest = outputs_dir / f"{candidate.stem}.{counter}{candidate.suffix}"
        try:
            shutil.copy2(str(candidate), str(dest))
            saved_path = str(dest)
            file_saved = True
        except Exception:
            try:
                candidate.replace(dest)
                saved_path = str(dest)
                file_saved = True
            except Exception:
                file_saved = False

except Exception as e:
    # include nested HTTP response info if present
    resp = getattr(e, 'response', None)
    if resp is not None:
        out['http_status'] = getattr(resp, 'status_code', None)
        out['http_text'] = getattr(resp, 'text', None)
    out['error'] = str(e)
# Determine final file path (prefer saved copy, otherwise any path returned by the API)
res_fp = None
try:
    if isinstance(res, dict):
        res_fp = res.get('file_path')
except Exception:
    res_fp = None

final_file = saved_path or res_fp

# Consider this a true CDS download only if the API reported copernicus_era5 and
# we have an actual file preserved (either copied to outputs or reported by the API).
is_cds_download = (out.get('data_source') == 'copernicus_era5') and bool(final_file)

out['file_path'] = final_file
out['file_saved'] = file_saved
out['cds_download'] = bool(is_cds_download)
out['retrieve_success'] = bool(is_cds_download)

# Include a tiny 3-line sample (first three hourly points) if we have a file
sample = None
try:
    if final_file and Path(final_file).exists():
        # attempt to open with xarray if available, otherwise skip sample
        try:
            import xarray as xr
            ds = xr.open_dataset(final_file)
            # Heuristic: find the first data variable and extract first 3 time points
            data_vars = [v for v in ds.data_vars]
            if data_vars:
                var = data_vars[0]
                arr = ds[var]
                if 'time' in arr.coords:
                    times = arr.coords['time'].values[:3].tolist()
                    vals = arr.values
                    # flatten per-time
                    sample = []
                    for i, t in enumerate(times):
                        try:
                            value = float(vals[i].flatten()[0]) if hasattr(vals[i], 'flatten') else float(vals[i])
                        except Exception:
                            value = None
                        sample.append({'time': str(t), 'value': value})
            ds.close()
        except Exception:
            sample = None
except Exception:
    sample = None

out['sample'] = sample

print(json.dumps(out))
