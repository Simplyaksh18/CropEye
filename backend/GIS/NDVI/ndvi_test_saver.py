"""
Helper to save NDVI test reports into the NDVI module outputs folder.

Exposes save_test_ndvi_report(ndvi_array, prefix=None) -> absolute path to saved PNG.
This wraps the Weather ndvi_report.generate_ndvi_report() function but places
outputs under backend/GIS/NDVI/outputs so frontend/tests can reference them.
"""
from __future__ import annotations
import os
import json
from datetime import datetime
from typing import Optional

# This saver has been intentionally turned into a no-op image saver.
# It will NOT generate PNG reports. Instead it will persist any provided
# metrics and metadata as a JSON file in the outputs directory and return None.

NDVI_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'outputs')


def save_test_ndvi_report(ndvi_array, prefix: Optional[str] = None, metadata: Optional[dict] = None, metrics: Optional[dict] = None) -> Optional[str]:
    """No-op saver for NDVI reports.

    - Does not invoke the image generator or matplotlib.
    - If metrics or metadata are provided, writes them to a JSON file in the outputs folder
      so other test tooling can still consume numeric results.
    - Returns None (no image path).
    """
    os.makedirs(NDVI_OUTPUT_DIR, exist_ok=True)
    ts = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    prefix_part = f"{prefix}_" if prefix else ''
    json_path = os.path.join(NDVI_OUTPUT_DIR, f"{prefix_part}ndvi_{ts}.json")

    payload = {
        'timestamp': datetime.utcnow().isoformat(),
        'metrics': metrics,
        'metadata': metadata,
        # We intentionally do not serialize the ndvi_array to avoid large files.
        'note': 'Image generation disabled; only metrics/metadata persisted.'
    }

    try:
        with open(json_path, 'w', encoding='utf-8') as fh:
            json.dump(payload, fh, indent=2, default=str)
    except Exception:
        # Fail silently — saving metrics is best-effort in test mode.
        return None

    # Return None because there is no image saved.
    return None
