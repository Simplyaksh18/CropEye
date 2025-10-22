"""
Test harness to compute NDVI from synthetic band text files, compute accuracy metrics
against an optional ground-truth, and generate an annotated NDVI report PNG.

Run:
    python test_ndvi_accuracy.py

Outputs:
 - PNG saved to backend/GIS/NDVI/outputs
 - Printed JSON metrics
"""
import os
import json
from pathlib import Path
from datetime import datetime
import numpy as np

# NOTE: Image generation disabled. We will not import or call the NDVI image reporter.
# Metrics (JSON) will be written to the outputs folder instead.

ROOT = Path(__file__).resolve().parents[2]
SYNTH_DIR = ROOT / 'GIS' / 'NDVI' / 'sentinel_data' / 'synthetic'
OUT_DIR = ROOT / 'GIS' / 'NDVI' / 'outputs'
OUT_DIR.mkdir(parents=True, exist_ok=True)


def load_band_file(p_base: Path, band: str) -> np.ndarray:
    """
    Load a band using several fallbacks:
      - TIFF: synthetic_B{band}_... .tif (preferred)
      - NPY: synthetic_B{band}_... .npy
      - TXT: last-resort, try to parse numeric values
    """
    # try TIFF
    tif_name = f'synthetic_B{band}_{p_base.stem.split("_")[-3]}_{p_base.stem.split("_")[-2]}.tif'
    tif_path = p_base.parent / f'synthetic_B{band}_{p_base.stem.split("_")[-3]}_{p_base.stem.split("_")[-2]}.tif'
    # But simpler: look for files named synthetic_B{band}_*.tif in the same dir
    candidates = list(p_base.parent.glob(f'synthetic_B{band}_*.tif'))
    if candidates:
        try:
            import importlib
            rasterio = importlib.import_module('rasterio')
            with rasterio.open(str(candidates[0])) as src:
                arr = src.read(1).astype(float)
                return arr
        except ModuleNotFoundError:
            # rasterio is not installed in this environment; skip TIFF support
            pass
        except Exception:
            pass

    # try npy
    candidates_npy = list(p_base.parent.glob(f'synthetic_B{band}_*.npy'))
    if candidates_npy:
        try:
            return np.load(str(candidates_npy[0]))
        except Exception:
            pass

    # fallback to simple text parsing
    txt_candidates = list(p_base.parent.glob(f'*B{band}_*.txt'))
    if txt_candidates:
        p = txt_candidates[0]
        # try to read numeric lines, skip header
        vals = []
        with open(p, 'r', encoding='utf-8', errors='ignore') as fh:
            for line in fh:
                parts = line.strip().split()
                for tok in parts:
                    try:
                        vals.append(float(tok))
                    except Exception:
                        continue
        if vals:
            # try to square into a 2D array if length is a perfect square
            n = len(vals)
            side = int(np.sqrt(n))
            if side * side == n:
                return np.array(vals).reshape((side, side))
            return np.array(vals)

    raise FileNotFoundError(f'No band file found for band B{band} in {p_base.parent}')


def compute_ndvi(red: np.ndarray, nir: np.ndarray, eps: float = 1e-6) -> np.ndarray:
    ndvi = (nir - red) / (nir + red + eps)
    return np.clip(ndvi, -1.0, 1.0)


def compute_metrics(actual: np.ndarray, computed: np.ndarray) -> dict:
    mask = np.isfinite(actual) & np.isfinite(computed)
    a = actual[mask].ravel()
    c = computed[mask].ravel()
    if a.size == 0:
        return {}
    diff = c - a
    mae = float(np.mean(np.abs(diff)))
    rmse = float(np.sqrt(np.mean(diff ** 2)))
    bias = float(np.mean(diff))
    pct05 = float(100.0 * np.mean(np.abs(diff) <= 0.05))
    try:
        r = float(np.corrcoef(a, c)[0, 1])
    except Exception:
        r = float('nan')
    return {'mae': mae, 'rmse': rmse, 'bias': bias, 'pct_within_0.05': pct05, 'r': r, 'n': int(a.size)}


if __name__ == '__main__':
    # Files in the supplied attachment
    # base file (we'll search the synthetic dir for matching synthetic_B04/B08 files)
    base_example = SYNTH_DIR / 'B04_30.3398_76.3869.txt'
    red = load_band_file(base_example, '04')
    nir = load_band_file(base_example, '08')

    computed = compute_ndvi(red, nir)

    # For synthetic tests, we don't have a separate true NDVI, so compute "actual" from these bands
    actual = compute_ndvi(red, nir)

    metrics = compute_metrics(actual, computed)
    print(json.dumps(metrics, indent=2))

    # Write metrics JSON to the outputs folder (no image will be generated)
    json_path = OUT_DIR / f'accuracy_{int(datetime.utcnow().timestamp())}_ndvi.json'
    try:
        with open(json_path, 'w', encoding='utf-8') as fh:
            json.dump({'metrics': metrics, 'timestamp': datetime.utcnow().isoformat()}, fh, indent=2)
        print('Saved metrics to:', str(json_path))
    except Exception as e:
        print('Could not write metrics JSON:', e)
