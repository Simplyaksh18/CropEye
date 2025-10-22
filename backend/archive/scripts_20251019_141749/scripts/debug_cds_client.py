#!/usr/bin/env python3
"""
A simple script to debug the initialization of the cdsapi.Client.

This helps verify that the `cdsapi` library can find and read the
~/.cdsapirc file or environment variables correctly.
"""

import os

print("="*60)
print("🧪 Testing Copernicus CDS API Client Initialization")
print("="*60)

try:
    import cdsapi
    print("✅ `cdsapi` library imported successfully.")

    # This is the line you provided
    c = cdsapi.Client()

    print(f"✅ Client created: {bool(c)}")
    print(f"   Client URL: {getattr(c, 'url', 'Not available')}")
    print(f"   Client Key: {'********' if getattr(c, 'key', None) else 'Not available'}")
    print("\nSUCCESS: The cdsapi library is correctly configured.")
except Exception as e:
    print(f"\n❌ FAILED: An error occurred during client initialization.")
    print(f"   Error: {e}")
    print("   Please check that your ~/.cdsapirc file is correctly formatted and accessible.")