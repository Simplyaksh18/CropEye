import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
from crop_recomendation import CropRecommender

data_path = os.path.join(os.path.dirname(__file__), 'data', 'crop_params_india.json')
print('data_path=', data_path)
print('exists=', os.path.exists(data_path))

recommender = CropRecommender(crop_table_path=data_path)
input_params = {
    'latitude': 30.3398,
    'longitude': 76.3869,
    'ph': 6.5,
    'rainfall': 850,
    'temp_mean': 30,
    'ndvi': 0.62
}

recs = recommender.recommend(input_params)
print('recommendations_count=', len(recs))
for r in recs[:8]:
    print('---')
    print(f"crop={r['crop']} score={r['score']}")
    print(' components:')
    for k, v in r['components'].items():
        print(f"  - {k}: {v}")
    print(' weights:')
    for k, v in r['weights'].items():
        print(f"  - {k}: {v}")
