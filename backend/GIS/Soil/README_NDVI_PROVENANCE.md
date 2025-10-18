# NDVI Provenance Schema

This document describes the `ndvi_provenance` object exposed in Soil API responses.

Fields (top-level):

- `is_real_data` (bool | null)

  - True when NDVI was derived from a real satellite product (Copernicus-derived synthetic or true bands).
  - False when NDVI was generated via simulation/fallback.
  - Null when provenance unavailable.

- `ndvi_data_source` (string | null)

  - Examples: `satellite_derived`, `realistic_synthetic_from_calculator`, `geographic_simulation`.

- `data_quality` (string | null)

  - `high`, `medium`, `low` to indicate confidence/quality of returned NDVI.

- `processing_details` (object | null)

  - Contains details of band file paths, file types, product metadata, and download source.
  - Keys commonly present when available:
    - `red_band_path` (string): Path to red band file used (e.g., `sentinel_data/.../B04_... .tif` or `.npy`).
    - `nir_band_path` (string): Path to NIR band file used.
    - `red_band_file_type` (string): File extension used (e.g., `.tif`, `.npy`).
    - `nir_band_file_type` (string)
    - `download_source` (string): e.g., `realistic_synthetic_from_copernicus`, `enhanced_synthetic`.
    - `product_id` (string | null): Product identifier from Copernicus catalogue (if real product found).
    - `product_name` (string | null): Product name string (SAFE name) when available.
    - `confidence` (float): 0..1 confidence score assigned by downloader/integration.

- `raw_download_result` (object | null)
  - When available, contains the raw dict returned by the NDVI downloader.
  - May include extra keys such as `products_found` and `cloud_cover`.

Example `ndvi_provenance`:

```json
{
  "is_real_data": true,
  "ndvi_data_source": "satellite_derived",
  "data_quality": "high",
  "processing_details": {
    "red_band_path": "sentinel_data\\synthetic_from_real\\B04_real_based_12.9716_77.5946.npy",
    "nir_band_path": "sentinel_data\\synthetic_from_real\\B08_real_based_12.9716_77.5946.npy",
    "red_band_file_type": ".npy",
    "nir_band_file_type": ".npy",
    "download_source": "realistic_synthetic_from_copernicus",
    "product_id": "3253645d-a5e4-4020-8333-4f5b5662090a",
    "product_name": "S2B_MSIL1C_20251014T050659_N0511_R019_T43PGQ_20251014T080203.SAFE",
    "confidence": 0.9
  },
  "raw_download_result": null
}
```

Notes:

- `processing_details` is intentionally lightweight; full raw download dict may be large and is available under `raw_download_result` when requested.
- File paths returned are relative to the repository root unless absolute paths are required by the downloader.
- If you need stricter typing or JSON Schema, I can add a `ndvi_provenance_schema.json` file and optional validation in the Flask endpoint.
