#!/usr/bin/env python3
"""
Crop Recommendation System Module (Starter Template)
Uses: Weather, Soil, NDVI, & Extension Data
Author: CropEye1 System
Date: October 19, 2025
"""

import os
import json
from dotenv import load_dotenv

# Load from .env file automatically
load_dotenv("file.env")

class CropRecommender:
    def __init__(self, crop_table_path='data/crop_params_india.json', weights=None):
        # Load static rule-based crop info (official/extension values)
        with open(crop_table_path, 'r', encoding='utf-8') as f:
            self.crop_table = json.load(f)
        # Default weights (can be overridden by `weights` dict or env vars)
        # importance: ph, rainfall, temperature, ndvi
        env_w = {
            'ph': os.getenv('WEIGHT_PH'),
            'rainfall': os.getenv('WEIGHT_RAIN'),
            'temp': os.getenv('WEIGHT_TEMP'),
            'ndvi': os.getenv('WEIGHT_NDVI')
        }
        # sensible defaults favoring NDVI slightly and rainfall
        defaults = {'ph': 0.2, 'rainfall': 0.35, 'temp': 0.2, 'ndvi': 0.25}
        # start from defaults, override with provided weights/env where present
        final = defaults.copy()
        if weights and isinstance(weights, dict):
            for k in final.keys():
                if k in weights:
                    try:
                        final[k] = float(weights[k])
                    except:
                        pass
        # override from env if set
        for k, v in env_w.items():
            if v is not None:
                try:
                    final[k] = float(v)
                except:
                    pass
        # normalize so weights sum to 1.0
        s = sum(final.values())
        if s <= 0:
            s = 1.0
        for k in final:
            final[k] = final[k] / s
        self.weights = final
    
    def recommend(self, input_params):
        """
        input_params: dict with keys:
            - latitude
            - longitude
            - ph
            - rainfall
            - temp_mean
            - ndvi
        Returns ranked crops and reasoning (list of dict)
        """
        suitability = []
        for crop, params in self.crop_table.items():
            # Calculate component suitability scores (0..1)
            ph_suit = self._scorer(input_params.get('ph'), params.get('ph_min'), params.get('ph_max'))
            rain_suit = self._scorer(input_params.get('rainfall'), params.get('rain_min_mm'), params.get('rain_max_mm'))
            temp_suit = self._scorer(input_params.get('temp_mean'), params.get('tmin'), params.get('tmax'))
            ndvi_val = input_params.get('ndvi', 0.5)
            ndvi_suit = float(ndvi_val) if ndvi_val is not None else 0.5
            # Weighted sum
            w = self.weights
            overall = (ph_suit * w['ph'] + rain_suit * w['rainfall'] + temp_suit * w['temp'] + ndvi_suit * w['ndvi'])
            suitability.append({
                'crop': crop,
                'score': round(overall, 3),
                'components': {
                    'ph': round(ph_suit, 3),
                    'rainfall': round(rain_suit, 3),
                    'temp': round(temp_suit, 3),
                    'ndvi': round(ndvi_suit, 3)
                },
                'weights': {k: round(v, 3) for k, v in self.weights.items()}
            })
        suitability.sort(key=lambda x: x['score'], reverse=True)
        return suitability
    
    @staticmethod
    def _scorer(val, minv, maxv):
        """Returns 1.0 if inside band, 0.0 if far, linear ramp otherwise"""
        try:
            v = float(val)
            if minv <= v <= maxv:
                return 1.0
            # Soft ramp: within 30% outside band, linearly decrease
            ramp = (maxv - minv) * 0.3
            if v < minv and minv - v < ramp:
                return max(0.0, 1 - (minv-v)/ramp)
            if v > maxv and v - maxv < ramp:
                return max(0.0, 1 - (v-maxv)/ramp)
            return 0.0
        except:
            return 0.0
