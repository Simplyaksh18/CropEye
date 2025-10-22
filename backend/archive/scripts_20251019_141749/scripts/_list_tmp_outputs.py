from pathlib import Path
import os
import tempfile
outputs = Path(r'D:/CropEye1/backend/GIS/Weather/outputs')
for p in outputs.iterdir():
    try:
        st = p.stat()
        print('OUT', p.name, st.st_size, st.st_mtime)
    except Exception as e:
        print('ERR', p, e)
tempd = Path(os.getenv('TEMP') or tempfile.gettempdir()) / 'cropeye_weather'
for p in tempd.iterdir():
    try:
        st = p.stat()
        print('TMP', p.name, st.st_size, st.st_mtime)
    except Exception as e:
        print('ERR', p, e)
