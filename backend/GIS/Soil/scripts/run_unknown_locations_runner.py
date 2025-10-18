import os
import sys

# Make sure parent directory (package root) is importable
HERE = os.path.abspath(os.path.dirname(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from ndvi_integration import ndvi_integration
from soil_data_collector import SoilDataCollector


def main():
    lat, lng = 12.9716, 77.5946  # Bangalore
    print(f"Running NDVI integration for lat={lat}, lng={lng}")
    ndvi = ndvi_integration.get_ndvi_for_location(lat, lng)
    print("NDVI result:")
    print(ndvi)
    print("\nRunning SoilDataCollector for same location (include_ndvi=True)")
    collector = SoilDataCollector()
    soil = collector.get_soil_data(lat, lng, include_ndvi=True)
    print("Soil result:")
    print(soil)


if __name__ == '__main__':
    main()
