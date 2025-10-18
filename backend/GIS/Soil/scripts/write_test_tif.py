import numpy as np
import rasterio
from rasterio.transform import from_origin
arr = np.ones((100, 100), dtype='float32')
profile = {
  'driver':'GTiff','height':100,'width':100,'count':1,'dtype':'float32','crs':'EPSG:4326',
  'transform': from_origin(77.5, 13.0, 0.0001, 0.0001)
}
with rasterio.open(r'D:\CropEye1\test.tif','w',**profile) as dst:
  dst.write(arr,1)
print('Wrote test.tif successfully')
