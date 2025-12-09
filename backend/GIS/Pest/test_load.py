#!/usr/bin/env python3
from pest_disease_detection import PestDiseaseDetector

detector = PestDiseaseDetector()
print('Pest database keys:', list(detector.PEST_DATABASE.keys()))
print('Disease database keys:', list(detector.DISEASE_DATABASE.keys()))
print('Sample pest symptoms:', detector.PEST_DATABASE['aphids']['symptoms'])
print('Sample disease control:', detector.DISEASE_DATABASE['blast']['control'])
