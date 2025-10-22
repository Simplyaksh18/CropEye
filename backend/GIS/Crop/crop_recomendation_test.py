#!/usr/bin/env python3
"""
Crop Recommendation Test Suite
For each test input, print official (extension) recommended crops,
and the computed recommendations from the module, for validation.
Author: CropEye1 System
Date: October 19, 2025
"""

import json
import os
from dotenv import load_dotenv
from crop_recomendation import CropRecommender

# Load credentials/secrets
load_dotenv("file.env")

# Load test cases (can be loaded from CSV or JSON for real use)
TEST_CASES = [
    {
        "location": "Punjab (Kharif)",
        "coordinate_source": "gps",
        "input": {
            "latitude": 30.8,
            "longitude": 75.8,
            "ph": 7.1,
            "rainfall": 900,
            "temp_mean": 30,
            "ndvi": 0.62
        },
        "official": {
            "most_suitable": ["rice"],
            "moderate": ["maize", "millets"],
            "notes": "Rice recommended for pH 5.5-7.0, rainfall 800+, temp 28-32."
        }
    },
    {
        "location": "Maharashtra (Rabi)",
        "coordinate_source": "manual",
        "input": {
            "latitude": 19.5,
            "longitude": 76.0,
            "ph": 6.3,
            "rainfall": 700,
            "temp_mean": 23,
            "ndvi": 0.48
        },
        "official": {
            "most_suitable": ["wheat", "barley"],
            "moderate": ["gram"],
            "notes": "Wheat for pH 6.0-7.5, rainfall 450-650mm, temp 20-25."
        }
    },
    {
        "location": "Tamil Nadu (Sandy soil)",
        "coordinate_source": "gps",
        "input": {
            "latitude": 10.5,
            "longitude": 78.3,
            "ph": 8.0,
            "rainfall": 600,
            "temp_mean": 27,
            "ndvi": 0.41
        },
        "official": {
            "most_suitable": ["cotton"],
            "moderate": ["sorghum", "sunflower"],
            "notes": "Cotton for pH 7-8.5, rainfall 500-900mm, sandy soil."
        }
    }
]

# Add an unknown / edge-case location to ensure graceful handling
TEST_CASES.append({
    'location': 'Unknown Location (ocean)',
    'coordinate_source': 'manual',
    'input': {
        'latitude': 0.0,
        'longitude': 0.0,
        'ph': 7.0,
        'rainfall': 50,
        'temp_mean': 28,
        'ndvi': 0.2
    },
    'official': {
        'most_suitable': [],
        'moderate': [],
        'notes': 'No official recommendation for ocean coordinates; test fallback behavior.'
    }
})

# Load static crop info (for table lookup inside module)
crop_params_path = os.path.join(os.path.dirname(__file__), 'data', 'crop_params_india.json')
if not os.path.exists(crop_params_path):
    print(f"ERROR: Missing {crop_params_path}! Please provide official crop suitability tables.")
    exit(1)

recommender = CropRecommender(crop_table_path=crop_params_path)

for case in TEST_CASES:
    print(f"\nLOCATION: {case['location']}")
    cs = case.get('coordinate_source', 'unknown')
    print(f"  Coordinate source: {cs}")
    print("  Official Extension Recommendation:")
    official_most = case['official'].get('most_suitable', [])
    official_moderate = case['official'].get('moderate', [])
    print(f"    Most Suitable: {', '.join(official_most) if official_most else 'None'}")
    print(f"    Moderate: {', '.join(official_moderate) if official_moderate else 'None'}")
    print(f"    Notes: {case['official']['notes']}")

    computed = recommender.recommend(case["input"])
    print("  Computed by Module:")
    if not computed:
        print("    No recommendations produced by the module.")
        continue

    # Top predicted crop
    top = computed[0]
    predicted_crop = top.get('crop')
    print(f"    Top prediction: {predicted_crop} (score: {top.get('score')})")

    # Compare with official
    if predicted_crop in official_most:
        print("    => MATCH: Predicted crop is listed as official most suitable.")
    elif predicted_crop in official_moderate:
        print("    => PARTIAL MATCH: Predicted crop is listed as official moderate.")
    else:
        print("    => DIFFER: Predicted crop is not in official recommendations.")

    print("    Full top-5 ranking with components and weights:")
    for i, row in enumerate(computed[:5]):
        comps = row.get('components', {})
        w = row.get('weights', {})
        comp_str = ', '.join([f"{k}={comps.get(k)}" for k in ['ph','rainfall','temp','ndvi']])
        weight_str = ', '.join([f"{k}={w.get(k)}" for k in ['ph','rainfall','temp','ndvi']])
        print(f"      {i+1}. {row.get('crop')} (score={row.get('score')})")
        print(f"         components: {comp_str}")
        print(f"         weights: {weight_str}")

    print("  " + "-"*40)
