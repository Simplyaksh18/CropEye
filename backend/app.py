import os
from datetime import datetime, timedelta
from collections import defaultdict
import statistics
from flask import Flask, request, jsonify
from contextlib import contextmanager
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import requests
import pathlib
import time

# Load backend/.env explicitly so configuration is correct regardless of current working directory.
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
ENV_PATH = os.path.join(BASE_DIR, '.env')
if os.path.exists(ENV_PATH):
    load_dotenv(ENV_PATH)
else:
    # fallback to default behavior (search CWD and parent dirs)
    load_dotenv()

AGRO_API_KEY = os.getenv("AGRO_API_KEY", "041eafb782c11c245450c23d485e8f9a")
built_in_real_farms = [
    {
        "id": "punjab",
        "name": "Punjab Agricultural University Research Farm",
        "country": "India",
        "coordinates": {"lat": 30.9010, "lng": 75.8573},
        "primary_crops": ["wheat", "maize", "cotton"],
    },
    {
        "id": "kerala",
        "name": "Kerala Rice Research Station",
        "country": "India",
        "coordinates": {"lat": 12.1848, "lng": 75.1588},
        "primary_crops": ["rice", "cassava", "coconut"],
    },
    {
        "id": "iari",
        "name": "IARI Regional Station Karnal",
        "country": "India",
        "coordinates": {"lat": 29.6857, "lng": 76.9905},
        "primary_crops": ["wheat", "mustard", "vegetables"],
    },
    {
        "id": "andhra",
        "name": "ANGRAU RARS Lam Farm",
        "country": "India",
        "coordinates": {"lat": 16.5167, "lng": 80.6167},
        "primary_crops": ["paddy", "maize", "pulses"],
    },
]
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "your_openweather_api_key")

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///cropeye.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Allow local dev frontends
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:3000", "http://127.0.0.1:3000"]}}, supports_credentials=True)
db = SQLAlchemy(app)
jwt = JWTManager(app)
# use Werkzeug security functions instead of flask_bcrypt; no app-level bcrypt instance required

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    farm_name = db.Column(db.String(120), nullable=True)
    location = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        # Werkzeug's generate_password_hash returns a string
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'firstName': self.first_name,
            'lastName': self.last_name,
            'farmName': self.farm_name,
            'location': self.location,
            'createdAt': self.created_at.isoformat()
        }

@contextmanager
def agromonitoring_polygon(lat, lon):
    """Context manager to create and automatically clean up a polygon."""
    polygon_id = None
    if not AGRO_API_KEY or AGRO_API_KEY == "c4c7629592bde2b6fe32de6e25ed1f09":
        print("⚠️ WARNING: AgroMonitoring API key is not configured or is the default key.")
        yield None
        return
    try:
        polygon_id = create_polygon(lat, lon)
        yield polygon_id
    finally:
        if polygon_id:
            print(f"Cleaning up polygon {polygon_id}...")
            requests.delete(f"http://api.agromonitoring.com/agro/1.0/polygons/{polygon_id}?appid={AGRO_API_KEY}")

def create_polygon(lat, lon, size=0.0005):
    coords = [[
        [lon-size, lat-size],
        [lon+size, lat-size],
        [lon+size, lat+size],
        [lon-size, lat+size],
        [lon-size, lat-size]
    ]]
    poly = {
        "name": "User Field",
        "geo_json": {
            "type": "Feature",
            "properties": {},
            "geometry": {"type": "Polygon", "coordinates": coords}
        }
    }
    resp = requests.post(
        f"http://api.agromonitoring.com/agro/1.0/polygons?appid={AGRO_API_KEY}",
        json=poly
    )
    data = resp.json()
    if resp.status_code != 201:
        raise requests.exceptions.HTTPError(f"Failed to create polygon: {data.get('message', 'Unknown error')}")
    
    print(f"Created polygon {data['id']} for location ({lat}, {lon})")
    return data["id"]

def get_ndvi(polygon_id, days=7):
    end = int(time.time())
    start = end - days*24*3600
    url = (
        f"http://api.agromonitoring.com/agro/1.0/ndvi/history?"
        f"start={start}&end={end}&polyid={polygon_id}&appid={AGRO_API_KEY}"
    )
    resp = requests.get(url)
    return resp.json()

def get_weather_forecast(polygon_id):
    url = (
        f"http://api.agromonitoring.com/agro/1.0/weather/forecast?"
        f"polyid={polygon_id}&appid={AGRO_API_KEY}"
    )
    resp = requests.get(url)
    return resp.json()

def get_detailed_weather(lat, lon):
    """Get detailed hourly weather from OpenWeatherMap"""
    try:
        if not OPENWEATHER_API_KEY or OPENWEATHER_API_KEY == 'your_openweather_api_key':
            print("⚠️ WARNING: OpenWeatherMap API key is not configured.")
            return {'error': 'Weather service is not configured.'}

        url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200:
            hourly_data = []
            for item in data['list'][:24]:  # Next 24 hours
                hourly_data.append({
                    'datetime': item['dt_txt'],
                    'temperature': item['main']['temp'],
                    'feels_like': item['main']['feels_like'],
                    'humidity': item['main']['humidity'],
                    'pressure': item['main']['pressure'],
                    'dew_point': item['main']['temp'] - ((100 - item['main']['humidity']) / 5),  # Approximation
                    'precipitation': item.get('rain', {}).get('3h', 0),
                    'rain_probability': item['pop'] * 100,
                    'wind_speed': item['wind']['speed'],
                    'wind_direction': item['wind']['deg'],
                    'weather': item['weather'][0]['description'],
                    'icon': item['weather'][0]['icon']
                })
            return {'hourly': hourly_data}
        else:
            print(f"OpenWeatherMap API Error: {data.get('message', 'Unknown error')}")
            return {'error': 'Weather data unavailable at the moment.'}
    except requests.exceptions.RequestException as e:
        print(f"Network error fetching weather data: {e}")
        return {'error': 'Could not connect to weather service.'}

def get_soil_fertility_data(lat, lon):
    """Mock soil fertility data - replace with actual API"""
    return {
        'ph_level': round(6.2 + (lat % 1) * 2, 1),
        'nitrogen': round(25 + (lon % 1) * 30, 1),
        'phosphorus': round(15 + (lat % 1) * 20, 1),
        'potassium': round(180 + (lon % 1) * 100, 1),
        'organic_matter': round(2.5 + (lat % 1) * 2, 1),
        'fertility_score': round(70 + (lat + lon) % 30, 1)
    }

def get_pest_alerts(lat, lon):
    """Mock pest alert data - replace with actual API"""
    alerts = [
        {
            'pest': 'Corn Borer',
            'severity': 'Medium',
            'description': 'Moderate activity detected in the region',
            'recommendation': 'Monitor crops weekly, consider preventive measures',
            'last_updated': datetime.utcnow().isoformat()
        },
        {
            'pest': 'Aphids',
            'severity': 'Low',
            'description': 'Low population levels',
            'recommendation': 'Continue regular monitoring',
            'last_updated': datetime.utcnow().isoformat()
        }
    ]
    return alerts

def get_ndvi_from_microservice(lat, lon):
    """
    Calls the standalone NDVI microservice to get detailed analysis.
    This function replaces the old agromonitoring logic.
    """
    ndvi_service_url = os.getenv('NDVI_SERVICE_URL', 'http://localhost:5001/api/ndvi/analyze')
    payload = {
        'latitude': lat,
        'longitude': lon,
        'use_real_data': True  # Always request real data from the microservice
    }
    try:
        # Set a long timeout because satellite data processing can take time
        response = requests.post(ndvi_service_url, json=payload, timeout=120)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Could not connect to NDVI microservice: {e}")
        return {
            'success': False,
            'error': 'NDVI analysis service is currently unavailable.',
            'data_source': 'service_unavailable'
        }


# ---------------------------------------------------------------------------
# Proxy endpoints: expose GIS microservice routes via the main dashboard server
# This keeps the microservices runnable independently but allows the frontend
# to talk to the main backend only (CORS, auth, single host).
# ---------------------------------------------------------------------------

# Service base URLs (can be overridden via env)
SOIL_SERVICE_URL = os.getenv('SOIL_API_URL', 'http://127.0.0.1:5002')
WEATHER_SERVICE_URL = os.getenv('WEATHER_API_URL', 'http://127.0.0.1:5003')
NDVI_SERVICE_URL = os.getenv('NDVI_API_URL', 'http://127.0.0.1:5001')
CROP_SERVICE_URL = os.getenv('CROP_API_URL', 'http://127.0.0.1:5004')


def _proxy_post(full_url, json_body=None, params=None, timeout=30):
    try:
        resp = requests.post(full_url, json=json_body, params=params, timeout=timeout)
        try:
            content = resp.json()
        except ValueError:
            content = {'raw_text': resp.text}
        return jsonify(content), resp.status_code
    except requests.RequestException as e:
        app.logger.warning(f"Proxy POST to {full_url} failed: {e}")
        return jsonify({'success': False, 'error': 'Upstream service unavailable', 'detail': str(e)}), 503


def _proxy_get(full_url, params=None, timeout=30):
    try:
        resp = requests.get(full_url, params=params, timeout=timeout)
        try:
            content = resp.json()
        except ValueError:
            content = {'raw_text': resp.text}
        return jsonify(content), resp.status_code
    except requests.RequestException as e:
        app.logger.warning(f"Proxy GET to {full_url} failed: {e}")
        return jsonify({'success': False, 'error': 'Upstream service unavailable', 'detail': str(e)}), 503


# NDVI: analyze
@app.route('/api/ndvi/analyze', methods=['POST'])
def proxy_ndvi_analyze():
    data = request.get_json(silent=True)
    return _proxy_post(f"{NDVI_SERVICE_URL}/api/ndvi/analyze", json_body=data)


# Soil: analyze
@app.route('/api/soil/analyze', methods=['POST'])
def proxy_soil_analyze():
    data = request.get_json(silent=True)
    return _proxy_post(f"{SOIL_SERVICE_URL}/api/soil/analyze", json_body=data)


# Weather: current and hourly endpoints (GET)
@app.route('/api/weather/current', methods=['GET'])
def proxy_weather_current():
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    params = {'lat': lat, 'lng': lng}
    return _proxy_get(f"{WEATHER_SERVICE_URL}/api/weather/current", params=params)


@app.route('/api/weather/hourly', methods=['GET'])
def proxy_weather_hourly():
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    hours = request.args.get('hours')
    params = {'lat': lat, 'lng': lng}
    if hours:
        params['hours'] = hours
    return _proxy_get(f"{WEATHER_SERVICE_URL}/api/weather/hourly", params=params)


# Crop: recommend, integrated, list
@app.route('/api/crop/recommend', methods=['POST'])
def proxy_crop_recommend():
    data = request.get_json(silent=True)
    return _proxy_post(f"{CROP_SERVICE_URL}/api/crop/recommend", json_body=data)


@app.route('/api/crop/recommend/integrated', methods=['POST'])
def proxy_crop_recommend_integrated():
    data = request.get_json(silent=True)
    return _proxy_post(f"{CROP_SERVICE_URL}/api/crop/recommend/integrated", json_body=data)


@app.route('/api/crop/list', methods=['GET'])
def proxy_crop_list():
    return _proxy_get(f"{CROP_SERVICE_URL}/api/crop/list")

def safe_mode(values, default='unknown'):
    try:
        return statistics.mode(values)
    except statistics.StatisticsError:
        return values[0] if values else default


def summarize_ndvi(ndvi_data):
    """
    Summarizes the detailed NDVI report from the microservice.
    """
    if not isinstance(ndvi_data, dict) or not ndvi_data.get('success'):
        return {
            'status': 'Data unavailable',
            'latestValue': None,
            'latestDate': None,
            'trend': 'unknown',
            'change': 0,
            'history': [],
            'error': ndvi_data.get('error', 'Invalid NDVI data format')
        }

    # The microservice provides a clean, pre-analyzed structure.
    ndvi_stats = ndvi_data.get('ndvi', {})
    health_analysis = ndvi_data.get('health_analysis', {})
    trend_analysis = ndvi_data.get('trend_analysis', {})

    latest_value = ndvi_stats.get('value')
    latest_date = ndvi_data.get('analysis_date')

    # Simulate a simple history for the summary card
    timeline = []
    if latest_value is not None and latest_date is not None:
        timeline.append({'date': latest_date, 'value': round(latest_value, 3)})
        # Add a couple of dummy historical points for trend calculation
        prev_date = (datetime.fromisoformat(latest_date) - timedelta(days=7)).isoformat()
        prev_value = latest_value - trend_analysis.get('change_last_7d', 0.02)
        timeline.insert(0, {'date': prev_date, 'value': round(prev_value, 3)})

    # If the microservice provided a time-series, we could use that instead.
    # For now, this simulation is sufficient for the summary.

    if not timeline:
        return {
            'status': 'Data unavailable',
            'latestValue': None,
            'latestDate': None,
            'trend': 'unknown',
            'change': 0,
            'history': []
        }

    timeline.sort(key=lambda item: item['date'])
    latest = timeline[-1]
    change = 0
    trend = 'stable'
    if len(timeline) > 1 and latest.get('value') is not None:
        previous = timeline[-2]
        change = round(latest.get('value', 0) - previous.get('value', 0), 3)
        if change > 0.03:
            trend = 'improving'
        elif change < -0.03:
            trend = 'declining'

    value = latest['value']
    if value is not None and value > 0.7:
        status = 'Excellent Vegetation'
    elif value > 0.5:
        status = 'Good Vegetation'
    elif value > 0.3:
        status = 'Moderate Vegetation'
    else:
        status = 'Low Vegetation'

    seasonal_average = round(
        statistics.mean(item['value'] for item in timeline[-6:]) if len(timeline) >= 2 else value, 3
    )

    return {
        'status': status,
        'latestValue': value,
        'latestDate': latest['date'],
        'trend': trend,
        'change': change,
        'seasonalAverage': seasonal_average,
        'history': timeline[-30:]
    }


def kelvin_to_celsius(temp):
    """Convert Kelvin-based readings to Celsius while preserving metric inputs."""
    if temp is None or not isinstance(temp, (int, float)):
        return None
    # AgroMonitoring & OpenWeather raw forecasts can arrive in Kelvin; convert values that exceed realistic Celsius bounds.
    if temp > 200:
        return temp - 273.15
    return temp


def transform_weather_forecast(raw_forecast):
    if isinstance(raw_forecast, dict):
        forecast_iterable = (
            raw_forecast.get('list')
            or raw_forecast.get('items')
            or raw_forecast.get('data')
            or []
        )
    else:
        forecast_iterable = raw_forecast

    if not forecast_iterable:
        return {'days': [], 'summary': 'Weather forecast unavailable.'}

    grouped = defaultdict(list)
    for entry in forecast_iterable:
        if not isinstance(entry, dict):
            continue
        timestamp = entry.get('dt') or entry.get('time')
        if not timestamp:
            continue
        if isinstance(timestamp, (int, float)):
            day = datetime.utcfromtimestamp(timestamp).date()
        else:
            try:
                day = datetime.fromisoformat(timestamp).date()
            except ValueError:
                continue
        grouped[day].append(entry)

    daily = []
    for day, entries in sorted(grouped.items()):
        temperatures = []
        temp_mins = []
        temp_maxs = []
        for item in entries:
            base_temp = item.get('temp')
            if base_temp is None and isinstance(item.get('main'), dict):
                base_temp = item['main'].get('temp')
            converted = kelvin_to_celsius(base_temp)
            if converted is not None:
                temperatures.append(converted)

            min_candidate = kelvin_to_celsius(
                item.get('temp_min')
                or item.get('main', {}).get('temp_min')
                or item.get('main', {}).get('temp_minimum')
            )
            max_candidate = kelvin_to_celsius(
                item.get('temp_max')
                or item.get('main', {}).get('temp_max')
                or item.get('main', {}).get('temp_maximum')
            )
            if min_candidate is not None:
                temp_mins.append(min_candidate)
            if max_candidate is not None:
                temp_maxs.append(max_candidate)

        humidity_values = [item.get('humidity') or item.get('main', {}).get('humidity') for item in entries]
        humidity_values = [h for h in humidity_values if isinstance(h, (int, float))]

        precipitation_values = []
        for item in entries:
            if isinstance(item.get('rain'), dict):
                precipitation_values.append(item['rain'].get('24h') or item['rain'].get('3h') or 0)
            elif isinstance(item.get('precipitation'), (int, float)):
                precipitation_values.append(item['precipitation'])

        weather_descriptions = []
        for item in entries:
            if isinstance(item.get('weather'), list) and item['weather']:
                weather_descriptions.append(item['weather'][0].get('description'))

        avg_temp = round(statistics.mean(temperatures), 1) if temperatures else None
        min_temp = round(min(temp_mins), 1) if temp_mins else (
            round(min(temperatures), 1) if temperatures else None
        )
        max_temp = round(max(temp_maxs), 1) if temp_maxs else (
            round(max(temperatures), 1) if temperatures else None
        )

        daily.append({
            'date': day.isoformat(),
            'temperature': {
                'min': min_temp,
                'max': max_temp,
                'avg': avg_temp,
            },
            'humidity': round(statistics.mean(humidity_values), 1) if humidity_values else None,
            'precipitation': round(sum(precipitation_values), 2) if precipitation_values else 0,
            'outlook': safe_mode(weather_descriptions),
            'wind': {
                'avg_speed': round(
                    statistics.mean(item.get('wind_speed') or item.get('wind', {}).get('speed') or 0 for item in entries),
                    1,
                ),
                'gust_max': round(
                    max((item.get('wind_gust') or item.get('wind', {}).get('gust') or 0) for item in entries),
                    1,
                ),
            },
        })

    climate_summary = 'Stable conditions expected.'
    if daily:
        avg_rain = statistics.mean(item['precipitation'] for item in daily)
        if avg_rain > 10:
            climate_summary = 'High precipitation expected—prepare for wet field conditions.'
        elif avg_rain < 1:
            climate_summary = 'Low rainfall forecast—consider irrigation planning.'

    return {
        'days': daily[:7],
        'summary': climate_summary,
    }


def build_crop_recommendations(soil_data, weather_report, ndvi_report, lat=None):
    base_recs = []
    if not soil_data:
        return base_recs

    ph = soil_data.get('ph_level')
    nitrogen = soil_data.get('nitrogen')
    organic_matter = soil_data.get('organic_matter')
    ndvi_status = (ndvi_report or {}).get('status', '').lower()

    def rec(crop, suitability, reason, success, practices):
        base_recs.append(
            {
                'crop': crop,
                'suitability': suitability,
                'reason': reason,
                'expectedHarvestSuccessRate': success,
                'recommendedPractices': practices,
            }
        )

    if lat is not None and 8 <= lat <= 20 and organic_matter and organic_matter > 1.5:
        reason = "Tropical climate with good organic matter supports these crops."
        rec(
            'Coconut', 'High', reason, '85% (regional board data)',
            ['Ensure good drainage', 'Apply potash regularly']
        )
        rec(
            'Banana', 'Medium-High', reason, '80% (regional board data)',
            ['Requires consistent moisture', 'Protect from high winds']
        )

    # Updated rule: trigger for arid latitude range, OR if high temps are detected in weather data
    if lat is not None and 25 <= lat <= 28 and (not weather_report or not weather_report.get('days') or any(day['temperature']['max'] > 35 for day in weather_report.get('days', []))):
        reason = "High heat and arid tolerance make these crops suitable."
        rec('Bajra', 'High', reason, '70% (rainfed baseline)', ['Sow with first monsoon rains'])
        rec('Cumin', 'Medium', reason, '65% (rainfed baseline)', ['Requires well-drained sandy soil'])

    if ph and 6.0 <= ph <= 7.2 and nitrogen and nitrogen > 20:
        reason = "Balanced soil pH with ample nitrogen supports fast-growing cereals."
        if ndvi_status in ['excellent vegetation', 'good vegetation']:
            reason += " Current vegetation vigor indicates the field is well-prepared."
        rec(
            'Maize',
            'High',
            reason,
            '82% (based on regional agronomy trials)',
            [
                'Use hybrid seed varieties suited to your region',
                'Monitor soil moisture weekly during tasseling',
                'Side-dress nitrogen at 35 days after germination',
            ],
        )

    if organic_matter and organic_matter >= 3:
        reason = "Rich organic matter retains moisture, ideal for legumes and oilseeds."
        if weather_report and any(day['precipitation'] > 5 for day in weather_report.get('days', [])):
            reason += " Forecasted rainfall supports pod development."
        rec(
            'Soybean',
            'Medium-High',
            reason,
            '75% (state agricultural universities average)',
            [
                'Inoculate seeds with Rhizobium culture before sowing',
                'Maintain 30-45 cm row spacing',
                'Schedule fungicide spray at flowering if humidity stays high',
            ],
        )

    rec(
        'Wheat',
        'Medium',
        'Adaptive cereal tolerant to moderate NDVI and soils between pH 5.5-7.5.',
        '78% (Punjab & Haryana extension data)',
        [
            'Prepare a fine tilth seedbed and ensure timely sowing',
            'Use seed treatment to reduce rust pressure',
            'Irrigate lightly at crown-root initiation stage',
        ],
    )

    if not base_recs:
        rec(
            'Millets',
            'Exploratory',
            'Hardy crop suitable for variable soils when limited data is available.',
            '65% (rainfed baseline)',
            [
                'Opt for drought-tolerant varieties',
                'Intercrop with legumes to fix nitrogen',
                'Conduct soil testing before fertilizer application',
            ],
        )

    return base_recs

# Authentication routes
@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        if not isinstance(data, dict):
            return jsonify({'message': 'Invalid JSON payload'}), 400

        required_fields = ['email', 'password', 'firstName', 'lastName']
        missing = [f for f in required_fields if not data.get(f)]
        if missing:
            return jsonify({'message': f"Missing required field(s): {', '.join(missing)}"}), 400

        email = (data.get('email') or '').strip().lower()
        if User.query.filter_by(email=email).first():
            return jsonify({'message': 'Email already registered'}), 400

        # Basic password quality check
        pwd = data.get('password', '')
        if len(pwd) < 6:
            return jsonify({'message': 'Password must be at least 6 characters'}), 400

        user = User()
        user.email = email
        user.first_name = data.get('firstName', '').strip()
        user.last_name = data.get('lastName', '').strip()
        user.farm_name = data.get('farmName')
        user.location = data.get('location')
        user.set_password(pwd)

        db.session.add(user)
        db.session.commit()

        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={'user': user.to_dict()}
        )
        return jsonify({'message': 'User registered successfully', 'token': access_token, 'user': user.to_dict()}), 201
    except (KeyError, TypeError, ValueError) as e:
        db.session.rollback()
        return jsonify({'message': f'Invalid registration data: {e}'}), 400
    except Exception as e:
        db.session.rollback()
        app.logger.exception("Registration failed")
        return jsonify({'message': 'Registration failed', 'error': str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json() or {}
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')

        if not email or not password:
            return jsonify({'message': 'Email and password are required'}), 400

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            access_token = create_access_token(
                identity=str(user.id),
                additional_claims={'user': user.to_dict()}
            )
            return jsonify({
                'message': 'Login successful',
                'token': access_token,
                'user': user.to_dict()
            }), 200
        return jsonify({'message': 'Invalid email or password'}), 401
    except (KeyError, TypeError):
        return jsonify({'message': 'Invalid login request format'}), 400
    except Exception as e:
        app.logger.exception("Unhandled login error")
        return jsonify({'message': 'Login failed', 'error': str(e)}), 500

@app.route('/api/logout', methods=['POST'])
@jwt_required()
def logout():
    # In a real application, you might want to blacklist the token
    return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/api/me', methods=['GET'])
@jwt_required()
def me():
    current_user_id = get_jwt_identity()
    try:
        current_user_id = int(current_user_id)
    except (TypeError, ValueError):
        return jsonify({'message': 'Invalid user identity in token'}), 400

    user = User.query.get(current_user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    return jsonify({'user': user.to_dict()})

@app.route('/api/analyze-location', methods=['POST'])
@jwt_required()
def analyze_location():
    try:
        current_user_id = get_jwt_identity()
        try:
            current_user_id = int(current_user_id)
        except (TypeError, ValueError):
            return jsonify({'message': 'Invalid user identity in token'}), 400
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        data = request.get_json()
        # Accept multiple param naming styles from legacy frontend
        lat = data.get('lat') or data.get('latitude')
        lon = data.get('lng') or data.get('lon') or data.get('longitude')
        try:
            lat = float(lat)
            lon = float(lon)
        except (TypeError, ValueError):
            return jsonify({'message': 'Latitude and longitude are required and must be numbers'}), 400
        
        if lat is None or lon is None:
            return jsonify({'message': 'Latitude and longitude are required'}), 400
        
        # NEW: Call our powerful NDVI microservice
        ndvi_report = get_ndvi_from_microservice(lat, lon)
        
        # Continue with other data sources (can be run in parallel in the future)
        weather_report = transform_weather_forecast(get_detailed_weather(lat, lon))
        soil_data = get_soil_fertility_data(lat, lon)
        crop_recommendations = build_crop_recommendations(soil_data, weather_report, ndvi_report, lat)
        pest_alerts = get_pest_alerts(lat, lon)

        return jsonify({
            'success': True,
            'location': {'lat': lat, 'lng': lon},
            'ndvi_report': ndvi_report,
            'weather_forecast': weather_report,
            'soil_fertility': soil_data,
            'crop_recommendations': crop_recommendations,
            'pest_alerts': pest_alerts,
            'analysis_timestamp': datetime.utcnow().isoformat()
        }), 200
            
    except requests.exceptions.RequestException as e:
        return jsonify({'message': 'A remote service is unavailable.', 'error': str(e)}), 503
    except (KeyError, TypeError) as e:
        return jsonify({'message': 'Invalid analysis request format.', 'error': str(e)}), 400


@app.route('/api/farms', methods=['GET'])
def list_reference_farms():
    return jsonify({'farms': built_in_real_farms})

@app.route('/')
def home():
    return jsonify({
        "message": "CropEye API with Authentication",
        "version": "2.0",
        "endpoints": [
            "/api/register",
            "/api/login",
            "/api/logout",
            "/api/analyze-location",
            "/api/farms"
        ]
    })

@app.route('/api/health')
def health():
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()})

@app.errorhandler(500)
def internal_error(e):
    app.logger.exception("Internal server error")
    return jsonify({'message': 'Internal server error', 'error': str(e)}), 500


@app.route('/api/health/aggregate', methods=['GET'])
def health_aggregate():
    """Ping configured GIS microservices and return a consolidated status."""
    services = {
        'ndvi': os.getenv('NDVI_API_URL', 'http://127.0.0.1:5001'),
        'soil': os.getenv('SOIL_API_URL', 'http://127.0.0.1:5002'),
        'weather': os.getenv('WEATHER_API_URL', 'http://127.0.0.1:5003'),
        'crop': os.getenv('CROP_API_URL', 'http://127.0.0.1:5004')
    }
    results = {}
    overall_ok = True
    for name, base in services.items():
        # determine health endpoint heuristically
        candidates = [f"{base}/api/health", f"{base}/api/{name}/health"]
        ok = False
        detail = None
        for url in candidates:
            try:
                r = requests.get(url, timeout=5)
                detail = {'status_code': r.status_code, 'body': None}
                try:
                    detail['body'] = r.json()
                except Exception:
                    detail['body'] = r.text[:200]
                if r.status_code == 200:
                    ok = True
                    break
            except requests.RequestException as e:
                detail = {'error': str(e)}
        results[name] = {'ok': ok, 'detail': detail}
        if not ok:
            overall_ok = False

    return jsonify({'overall_ok': overall_ok, 'services': results, 'timestamp': datetime.utcnow().isoformat()}), (200 if overall_ok else 503)

@app.cli.command("seed-demo")
def seed_demo():
    """Manually seed the demo user (idempotent)."""
    with app.app_context():
        db.create_all()
        demo_email = 'demo@cropeye.dev'
        if not User.query.filter_by(email=demo_email).first():
            demo = User()
            demo.email = demo_email
            demo.first_name = 'Demo'
            demo.last_name = 'User'
            demo.farm_name = 'Demo Farm'
            demo.location = 'Demo Valley'
            demo.set_password('DemoPass123!')
            db.session.add(demo)
            db.session.commit()
            print('✅ Seeded demo user.')
        else:
            print('ℹ️ Demo user already exists.')

@app.cli.command("db-init")
def db_init():
    """Initializes the database and creates tables."""
    with app.app_context():
        db.create_all()
    print("Database initialized and tables created.")

_seed_done = False

@app.before_request
def init_and_seed():
    global _seed_done
    if _seed_done:
        return
    db.create_all()
    demo_email = 'demo@cropeye.dev'
    if not User.query.filter_by(email=demo_email).first():
        demo = User()
        demo.email = demo_email
        demo.first_name = 'Demo'
        demo.last_name = 'User'
        demo.farm_name = 'Demo Farm'
        demo.location = 'Demo Valley'
        demo.set_password('DemoPass123!')
        db.session.add(demo)
        db.session.commit()
        print('Seeded demo user: demo@cropeye.dev / DemoPass123!')
    else:
        print('Demo user already exists.')
    _seed_done = True

if __name__ == '__main__':
    print("Starting CropEye API with Authentication...")
    print("AgroMonitoring API integration enabled")
    print("JWT Authentication enabled")
    host = os.environ.get('FLASK_RUN_HOST', '127.0.0.1')
    port = int(os.environ.get('FLASK_RUN_PORT', 5000))
    print(f"Listening on http://{host}:{port}")
    try:
        app.run(host=host, port=port, debug=True, threaded=True)
    except Exception as e:
        print(f"Failed to start Flask app: {e}")


# Duplicate health_aggregate removed — original implementation is defined earlier in the file.
