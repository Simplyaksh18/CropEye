from pathlib import Path
import os
import tempfile
outputs = Path(r'D:/CropEye1/backend/GIS/Weather/outputs')
print('outputs exists', outputs.exists())
if outputs.exists():
    for p in outputs.iterdir():
        try:
            st = p.stat()
            print('OUT', p.name, st.st_size, st.st_mtime)
        except Exception as e:
            print('ERR', p, e)
temp_dir = os.getenv('TEMP') or tempfile.gettempdir()
tempd = Path(temp_dir) / 'cropeye_weather'
print('temp path', tempd)
print('temp exists', tempd.exists())
if tempd.exists():
    for p in tempd.iterdir():
        try:
            st = p.stat()
            print('TMP', p.name, st.st_size, st.st_mtime)
        except Exception as e:
            print('ERR', p, e)
            print('ERR', p, e)
