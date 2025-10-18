"""Verify GDAL/PROJ/rasterio environment.

Prints current PROJ_LIB, pyproj data dir and rasterio/gdal versions.
"""
import os
import sys
try:
    import pyproj
except Exception as e:
    pyproj = None
try:
    import rasterio
except Exception as e:
    rasterio = None

print("PROJ_LIB env:", os.environ.get('PROJ_LIB'))
if pyproj:
    try:
        # Prefer pyproj.datadir.get_data_dir() when available; import the datadir submodule to avoid static attribute checks
        try:
            from importlib import import_module
            _datadir = import_module("pyproj.datadir")
            if hasattr(_datadir, "get_data_dir"):
                print("pyproj data dir:", _datadir.get_data_dir())
            else:
                # Fallback: print package path so user can inspect data location
                print("pyproj package path:", os.path.dirname(pyproj.__file__))
        except Exception:
            # Fallback: print package path so user can inspect data location
            print("pyproj package path:", os.path.dirname(pyproj.__file__))
    except Exception as e:
        print("pyproj.datadir.get_data_dir() failed:", e)
else:
    print("pyproj not importable")

if rasterio:
    try:
        try:
            # rasterio 1.x exposes env functions
            from rasterio.env import gdal_version
            print("rasterio gdal_version:", gdal_version())
        except Exception:
            # fallback
            print("rasterio version:", rasterio.__version__)
    except Exception as e:
        print("rasterio info failed:", e)
else:
    print("rasterio not importable")

print("python sys.prefix:", sys.prefix)
print("python executable:", sys.executable)
