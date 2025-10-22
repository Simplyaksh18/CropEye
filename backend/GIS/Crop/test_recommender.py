import os

from crop_recomendation import CropRecommender


def test_recommender_loads_and_recommends():
    data_path = os.path.join(os.path.dirname(__file__), 'data', 'crop_params_india.json')
    assert os.path.exists(data_path), f"Crop params file not found at {data_path}"

    recommender = CropRecommender(crop_table_path=data_path)
    # Ensure crop table loaded
    assert isinstance(recommender.crop_table, dict)
    assert len(recommender.crop_table) > 0

    # Sample input (Punjab-like conditions)
    input_params = {
        'latitude': 30.3398,
        'longitude': 76.3869,
        'ph': 6.5,
        'rainfall': 850,
        'temp_mean': 30,
        'ndvi': 0.62
    }

    recs = recommender.recommend(input_params)
    assert isinstance(recs, list)
    assert len(recs) > 0

    top = recs[0]
    assert 'crop' in top and 'score' in top
    assert 0.0 <= top['score'] <= 1.0
    # Ensure known crop keys are present in results
    crops = [r['crop'] for r in recs]
    assert 'rice' in crops or 'wheat' in crops
