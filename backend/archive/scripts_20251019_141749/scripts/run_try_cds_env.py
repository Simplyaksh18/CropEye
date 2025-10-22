import os,sys,subprocess,re
cds = os.path.join(os.path.expanduser('~'), '.cdsapirc')
if not os.path.exists(cds):
    print('ERROR: .cdsapirc not found at', cds)
    sys.exit(1)
raw = open(cds,'r',encoding='utf-8').read()
m = re.search(r'key:\s*(.+)', raw)
if not m:
    print('ERROR: no key found in .cdsapirc')
    sys.exit(1)
rawKey = m.group(1).strip()
if ':' in rawKey:
    rawKey = rawKey.split(':',1)[1]
env = os.environ.copy()
env['COPERNICUS_CDS_KEY'] = rawKey
env['COPERNICUS_CDS_URL'] = 'https://cds.climate.copernicus.eu/api'
print('Running try_cds_retrieve.py with COPERNICUS_CDS_KEY set in-session (no file modification)...')
proc = subprocess.run([sys.executable, r'D:/CropEye1/backend/scripts/try_cds_retrieve.py'], env=env, capture_output=True, text=True)
print(proc.stdout)
if proc.stderr:
    print(proc.stderr, file=sys.stderr)
