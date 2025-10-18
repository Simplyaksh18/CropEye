"""Check for incompatible PROJ database and print guidance.

This script checks the PROJ_LIB environment variable and tries to detect
common PostGIS/PostgreSQL proj.db paths which are often incompatible with
modern rasterio/GDAL builds. If an incompatible path is detected, it prints
clear instructions to fix the environment using the project's `cropeye`
conda environment (conda-forge) and exits with code 2.
"""
import os
import sys
from pathlib import Path

def looks_like_postgis_proj(path: str) -> bool:
    if not path:
        return False
    p = path.lower()
    return ('postgres' in p) or ('postgis' in p) or ('pgsql' in p)

def find_better_candidate() -> str:
    # Prefer CONDA_PREFIX -> cropeye env if present
    conda_prefix = os.environ.get('CONDA_PREFIX')
    if conda_prefix:
        candidates = [
            Path(conda_prefix) / 'Library' / 'share' / 'proj',
            Path(conda_prefix) / 'share' / 'proj'
        ]
        for c in candidates:
            if c.exists():
                return str(c)
    # Try common cropeye env under user miniconda/anaconda
    home = Path.home()
    for base in ['\\miniconda3', '\\anaconda3', '\\Miniconda3', '']:
        p = home.joinpath(base, 'envs', 'cropeye', 'Library', 'share', 'proj')
        if p.exists():
            return str(p)
        p2 = home.joinpath(base, 'envs', 'cropeye', 'share', 'proj')
        if p2.exists():
            return str(p2)
    # OSGeo4W
    osgeo = Path(r"C:\OSGeo4W64\share\proj")
    if osgeo.exists():
        return str(osgeo)
    return ''


def main():
    proj_lib = os.environ.get('PROJ_LIB')
    if not proj_lib:
        print('PROJ_LIB is not set in the environment. That is often fine if you use an isolated conda env.')
        return 0

    print('Detected PROJ_LIB:', proj_lib)
    if looks_like_postgis_proj(proj_lib):
        better = find_better_candidate()
        print('\n⚠️  It looks like PROJ_LIB points to a PostGIS/PostgreSQL proj.db which is commonly incompatible with rasterio/GDAL builds.')
        print('   This typically causes errors like: "DATABASE.LAYOUT.VERSION.MINOR = 2 whereas a number >= 4 is expected"')
        print('\nRecommended fix: install GDAL/rasterio/proj in the `cropeye` conda environment from conda-forge and use that environment.')
        print('\nRun these PowerShell commands (copy & paste):')
        print('```powershell')
        print('conda activate cropeye')
        print('conda install -c conda-forge gdal rasterio proj -y')
        print('```')
        if better:
            print('\nAfter installation, set PROJ_LIB to the suggested candidate for this machine (example):')
            print(f"```powershell\n$env:PROJ_LIB = '{better}'\n```")
        else:
            print('\nAfter installation, verify with the verification script:')
            print('python backend/GIS/Soil/scripts/verify_gdal.py')
        print('\nExiting with code 2 to indicate incompatible PROJ detected.')
        return 2

    print('PROJ_LIB does not appear to be the PostGIS proj.db. No action required.')
    return 0

if __name__ == '__main__':
    rc = main()
    sys.exit(rc)
