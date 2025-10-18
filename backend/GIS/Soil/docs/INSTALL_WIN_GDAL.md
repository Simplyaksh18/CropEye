# Windows GDAL / PROJ / Rasterio Setup Guide

## Purpose

This guide helps you install a consistent GDAL/PROJ/rasterio stack on Windows so that Python code (rasterio) can write GeoTIFFs and use EPSG codes reliably. It addresses common issues where PostgreSQL/PostGIS installs a different PROJ database that causes errors like:

PROJ: proj_create_from_database: C:\Program Files\PostgreSQL\...\proj.db contains DATABASE.LAYOUT.VERSION.MINOR = 2 whereas a number >= 4 is expected

Two recommended approaches (conda-forge and OSGeo4W). Choose the one that best fits your environment.

## Option A — Recommended: Use conda-forge (isolated, reproducible)

1. Install Miniconda or use an existing conda environment.

2. Use the existing `cropeye` conda environment (recommended):

```powershell
conda activate cropeye
```

3. Install or upgrade rasterio and GDAL from conda-forge (pins PROJ and GDAL to compatible builds):

```powershell
conda install -n cropeye -c conda-forge rasterio gdal proj -y
```

4. Verify installation inside the `cropeye` env:

```powershell
python -c "import rasterio; print('rasterio/gdal:', getattr(rasterio, '__gdal_version__', rasterio.__version__)); import pyproj; print('pyproj:', pyproj.__version__)"
```

5. Run a small write test (from repo root):

```powershell
python - <<'PY'
import numpy as np
import rasterio
from rasterio.transform import from_origin
arr = np.ones((100, 100), dtype='float32')
profile = {
  'driver':'GTiff','height':100,'width':100,'count':1,'dtype':'float32','crs':'EPSG:4326',
  'transform': from_origin(77.5, 13.0, 0.0001, 0.0001)
}
with rasterio.open('test.tif','w',**profile) as dst:
  dst.write(arr,1)
print('Wrote test.tif successfully')
PY
```

If this writes successfully, rasterio/GDAL/PROJ are consistent.

Notes for conda approach:

- Keep this environment separate from system Postgres installs. The conda environment ships its own PROJ and proj.db and will be used by rasterio when the conda environment is active.
- If you previously installed rasterio via pip, remove it from the environment to avoid conflicts.

## Option B — OSGeo4W (system-wide Windows install)

1. Download and run the OSGeo4W installer (https://trac.osgeo.org/osgeo4w/). Choose the 'Advanced Install' and include packages: gdal, proj, and Python bindings.

2. Use the OSGeo4W shell to run Python or adjust PATH to include OSGeo4W's bin directories. Example test in OSGeo4W shell:

```powershell
python -c "import rasterio; print(rasterio.__gdal_version__)"
```

3. If you use a separate Python (e.g., Anaconda), point your GDAL and PROJ environment variables to OSGeo4W installations (not recommended — prefer conda-forge isolation).

## Troubleshooting: PROJ database mismatch

- The error means another PROJ (often from PostGIS) is being found first. Solutions:
  1. Use the conda environment (preferred) which isolates PROJ.
  2. Set the environment variable PROJ_LIB to the correct proj.db directory for the PROJ installation used by rasterio/GDAL. For example (PowerShell):

```powershell
$env:PROJ_LIB = 'C:\Users\<youruser>\miniconda3\envs\cropeye-gdal\Library\share\proj'
```

3. Ensure PATH ordering places the desired PROJ/GDAL binaries before Postgres directories.

## Verifying which proj.db rasterio/pyproj is using

Run:

```powershell
python -c "import pyproj; print(pyproj.datadir.get_data_dir())"
python -c "import rasterio; print(rasterio.env.get_gdal_version())"
```

If pyproj points to an unexpected proj folder (e.g., under PostgreSQL), change PROJ_LIB to your desired proj data folder and restart your shell/IDE.

## If you must keep Postgres/PostGIS installed system-wide

- Prefer conda environment for Python projects to avoid system conflicts.
- If you need system-wide access, update the system PATH so the desired PROJ (OSGeo4W or conda) is first.

## Summary checklist

- [ ] Create a fresh conda env (recommended).
- [ ] Install rasterio/gdal/proj from conda-forge.
- [ ] Verify `rasterio` can write a GeoTIFF.
- [ ] If PROJ mismatch persists, set PROJ_LIB to the conda env's `share/proj`.

If you want, I can:

- Add commands to your README and a small Python verification script into the repo.
- Attempt to detect PROJ mismatch at runtime and automatically set PROJ_LIB when our Flask app starts (low-risk shim). Let me know which you prefer.

Note: This repository now includes a small runtime shim that attempts to set `PROJ_LIB` when `env_credentials.set_environment_variables()` runs. That shim prefers common conda/OSGeo4W locations. It is a best-effort fallback and only works when a viable proj data folder exists on the host. If you keep using a non-conda Python or your system has only a PostGIS `proj.db`, you should create/activate a conda env (recommended) and run the verification steps below.

Repository helper script:

- `backend/GIS/Soil/scripts/verify_gdal.py` (prints current pyproj and rasterio PROJ/GDAL information and current PROJ_LIB env var). Use this to quickly inspect what your Python environment is using.

If you'd like, I can add an automated check that fails early with a clear message when an incompatible `proj.db` is detected.

## Pre-flight checker (project helper)

This repository includes a small pre-flight checker that runs when the Flask app starts: `backend/GIS/Soil/scripts/check_proj_compat.py`.

- It looks at the `PROJ_LIB` environment variable and attempts to detect common PostGIS/PostgreSQL `proj.db` locations that are typically incompatible with rasterio/GDAL builds.
- If it finds a likely incompatible `proj.db`, it exits startup and prints clear PowerShell commands to fix the `cropeye` conda environment (install gdal/rasterio/proj from conda-forge) and optionally set `PROJ_LIB` to a suitable folder.

Usage (manual):

```powershell
# Run the checker standalone
python backend/GIS/Soil/scripts/check_proj_compat.py

# Run the verification script to inspect what Python is currently using
python backend/GIS/Soil/scripts/verify_gdal.py
```

If the checker exits with code 2, follow the printed instructions to update your `cropeye` environment and re-run the Flask app.
