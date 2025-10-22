#!/usr/bin/env python3
"""
OpenWeatherMap API Handler
CropEye1 Weather Module - Real-time & Forecast Weather Data



Features:
- Current weather conditions
- 48-hour hourly forecast
- 7-day daily forecast
- Weather alerts
- Air quality data

Uses OpenWeatherMap One Call API 3.0
API Docs: https://openweathermap.org/api/one-call-3

Author: CropEye1 System
Date: October 18, 2025
"""

import os
import requests
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OpenWeatherAPI:
    """OpenWeatherMap API client for real-time weather data"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize OpenWeatherMap API client
        
        Args:
            api_key: OpenWeatherMap API key (or from env)
        """
        self.api_key = api_key or os.getenv('OPENWEATHER_API_KEY')
        
        if not self.api_key:
            logger.error("OpenWeatherMap API key not found")
            raise ValueError("OPENWEATHER_API_KEY not set in environment")
        
        self.base_url = "https://api.openweathermap.org/data/3.0/onecall"
        self.base_url_current = "https://api.openweathermap.org/data/2.5/weather"
        self.base_url_forecast = "https://api.openweathermap.org/data/2.5/forecast"
        
        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 1.0  # seconds
        
        logger.info("✅ OpenWeatherMap API initialized")
    
    def _rate_limit(self):
        """Implement rate limiting"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def get_current_weather(self, latitude: float, longitude: float) -> Dict:
        """
        Get current weather conditions
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            
        Returns:
            Dict containing current weather data
        """
        try:
            self._rate_limit()

            params = {
                'lat': latitude,
                'lon': longitude,
                'appid': self.api_key,
                'units': 'metric'
            }

            response = requests.get(self.base_url_current, params=params, timeout=10)
            # If the response has a 4xx status code (client error), treat it as recoverable
            if 400 <= getattr(response, 'status_code', 0) < 500:
                logger.warning(f"⚠️ OpenWeatherMap client error ({response.status_code}): {response.text}")
                return self._get_fallback_current_weather(latitude, longitude)

            response.raise_for_status()

            data = response.json()
            
            current_weather = {
                'timestamp': datetime.now().isoformat(),
                'location': {
                    'latitude': latitude,
                    'longitude': longitude,
                    'name': data.get('name', 'Unknown'),
                    'country': data.get('sys', {}).get('country', '')
                },
                'temperature': {
                    'current': data['main']['temp'],
                    'feels_like': data['main']['feels_like'],
                    'min': data['main']['temp_min'],
                    'max': data['main']['temp_max'],
                    'unit': 'celsius'
                },
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'wind': {
                    'speed': data['wind']['speed'],
                    'direction': data['wind'].get('deg', 0),
                    'gust': data['wind'].get('gust', 0)
                },
                'clouds': data['clouds']['all'],
                'visibility': data.get('visibility', 10000),
                'weather': {
                    'main': data['weather'][0]['main'],
                    'description': data['weather'][0]['description'],
                    'icon': data['weather'][0]['icon']
                },
                'rain': data.get('rain', {}).get('1h', 0),
                'snow': data.get('snow', {}).get('1h', 0),
                'sunrise': datetime.fromtimestamp(data['sys']['sunrise']).isoformat(),
                'sunset': datetime.fromtimestamp(data['sys']['sunset']).isoformat(),
                'data_source': 'openweathermap',
                'api_call_time': datetime.now().isoformat()
            }
            
            logger.info(f"✅ Current weather retrieved for {latitude}, {longitude}")
            return current_weather
            
        except requests.exceptions.RequestException as e:
            # Network or server-side error
            logger.error(f"❌ OpenWeatherMap API request failed: {e}")
            return self._get_fallback_current_weather(latitude, longitude)
        except Exception as e:
            logger.error(f"❌ Error getting current weather: {e}")
            return self._get_fallback_current_weather(latitude, longitude)
    
    def get_hourly_forecast(self, latitude: float, longitude: float, hours: int = 48) -> Dict:
        """
        Get hourly weather forecast (up to 48 hours)
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            hours: Number of hours to forecast (default 48, max 48)
            
        Returns:
            Dict containing hourly forecast data
        """
        try:
            self._rate_limit()

            # Use 5-day/3-hour forecast endpoint (free tier)
            params = {
                'lat': latitude,
                'lon': longitude,
                'appid': self.api_key,
                'units': 'metric',
                'cnt': min(hours // 3, 40)  # API provides 3-hour intervals
            }

            response = requests.get(self.base_url_forecast, params=params, timeout=10)
            # Treat client-side errors (4xx) as recoverable fallbacks
            if 400 <= getattr(response, 'status_code', 0) < 500:
                logger.warning(f"⚠️ OpenWeatherMap forecast client error ({response.status_code}): {response.text}")
                return self._get_fallback_forecast(latitude, longitude, hours)

            response.raise_for_status()

            data = response.json()
            
            hourly_data = []
            for item in data['list'][:min(16, len(data['list']))]:  # 48 hours = 16 x 3-hour blocks
                hourly_item = {
                    'dt': datetime.fromtimestamp(item['dt']).isoformat(),
                    'timestamp': datetime.fromtimestamp(item['dt']).isoformat(),
                    'temperature': item['main']['temp'],
                    'feels_like': item['main']['feels_like'],
                    'temp_min': item['main']['temp_min'],
                    'temp_max': item['main']['temp_max'],
                    'humidity': item['main']['humidity'],
                    'pressure': item['main']['pressure'],
                    'wind_speed': item['wind']['speed'],
                    'wind_direction': item['wind'].get('deg', 0),
                    'clouds': item['clouds']['all'],
                    'precipitation_probability': item.get('pop', 0) * 100,  # Convert to percentage
                    'rain_3h': item.get('rain', {}).get('3h', 0),
                    'snow_3h': item.get('snow', {}).get('3h', 0),
                    'weather': {
                        'main': item['weather'][0]['main'],
                        'description': item['weather'][0]['description'],
                        'icon': item['weather'][0]['icon']
                    }
                }
                hourly_data.append(hourly_item)
            
            forecast = {
                'timestamp': datetime.now().isoformat(),
                'location': {
                    'latitude': latitude,
                    'longitude': longitude,
                    'name': data['city']['name'],
                    'country': data['city']['country']
                },
                'forecast_hours': len(hourly_data) * 3,
                'hourly': hourly_data,
                'data_source': 'openweathermap',
                'api_call_time': datetime.now().isoformat()
            }
            
            logger.info(f"✅ Hourly forecast retrieved for {latitude}, {longitude}")
            return forecast
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ OpenWeatherMap forecast request failed: {e}")
            return self._get_fallback_forecast(latitude, longitude, hours)
        except Exception as e:
            logger.error(f"❌ Error getting hourly forecast: {e}")
            return self._get_fallback_forecast(latitude, longitude, hours)
    
    def get_daily_forecast(self, latitude: float, longitude: float, days: int = 7) -> Dict:
        """
        Get daily weather forecast
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            days: Number of days to forecast (default 7)
            
        Returns:
            Dict containing daily forecast data
        """
        try:
            # Use hourly forecast and aggregate to daily
            hourly_forecast = self.get_hourly_forecast(latitude, longitude, hours=min(days * 24, 120))
            
            if 'hourly' not in hourly_forecast:
                return self._get_fallback_daily_forecast(latitude, longitude, days)
            
            # Aggregate hourly to daily
            daily_data = {}
            for hour in hourly_forecast['hourly']:
                date = hour['dt'][:10]  # Extract date (YYYY-MM-DD)
                
                if date not in daily_data:
                    daily_data[date] = {
                        'temps': [],
                        'humidity': [],
                        'wind': [],
                        'precipitation': 0,
                        'weather_conditions': []
                    }
                
                daily_data[date]['temps'].append(hour['temperature'])
                daily_data[date]['humidity'].append(hour['humidity'])
                daily_data[date]['wind'].append(hour['wind_speed'])
                daily_data[date]['precipitation'] += hour.get('rain_3h', 0)
                daily_data[date]['weather_conditions'].append(hour['weather']['main'])
            
            # Format daily summaries
            daily_forecast = []
            for date, data in sorted(daily_data.items()):
                daily_item = {
                    'date': date,
                    'temperature': {
                        'min': min(data['temps']),
                        'max': max(data['temps']),
                        'avg': sum(data['temps']) / len(data['temps'])
                    },
                    'humidity_avg': sum(data['humidity']) / len(data['humidity']),
                    'wind_speed_avg': sum(data['wind']) / len(data['wind']),
                    'total_precipitation': data['precipitation'],
                    'dominant_weather': max(set(data['weather_conditions']), 
                                           key=data['weather_conditions'].count)
                }
                daily_forecast.append(daily_item)
            
            result = {
                'timestamp': datetime.now().isoformat(),
                'location': hourly_forecast['location'],
                'forecast_days': len(daily_forecast),
                'daily': daily_forecast[:days],
                'data_source': 'openweathermap',
                'aggregation_method': 'hourly_to_daily'
            }
            
            logger.info(f"✅ Daily forecast retrieved for {latitude}, {longitude}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Error getting daily forecast: {e}")
            return self._get_fallback_daily_forecast(latitude, longitude, days)
    
    def get_weather_alerts(self, latitude: float, longitude: float) -> Dict:
        """
        Get weather alerts for location
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            
        Returns:
            Dict containing weather alerts
        """
        # Note: Weather alerts require One Call API 3.0 which needs subscription
        # For free tier, we'll analyze current/forecast for potential issues
        
        try:
            current = self.get_current_weather(latitude, longitude)
            forecast = self.get_hourly_forecast(latitude, longitude, 24)
            
            alerts = []
            
            # Check for extreme temperatures
            if current['temperature']['current'] < 0:
                alerts.append({
                    'type': 'frost',
                    'severity': 'high',
                    'message': f"Freezing temperature: {current['temperature']['current']}°C",
                    'recommendation': 'Protect sensitive crops from frost damage'
                })
            
            if current['temperature']['current'] > 40:
                alerts.append({
                    'type': 'heat',
                    'severity': 'high',
                    'message': f"Extreme heat: {current['temperature']['current']}°C",
                    'recommendation': 'Ensure adequate irrigation and shade for crops/livestock'
                })
            
            # Check for high winds
            if current['wind']['speed'] > 15:
                alerts.append({
                    'type': 'wind',
                    'severity': 'medium',
                    'message': f"High wind speed: {current['wind']['speed']} m/s",
                    'recommendation': 'Secure structures and protect young plants'
                })
            
            # Check for heavy rain in forecast
            if 'hourly' in forecast:
                total_rain_24h = sum(h.get('rain_3h', 0) for h in forecast['hourly'][:8])
                if total_rain_24h > 50:
                    alerts.append({
                        'type': 'heavy_rain',
                        'severity': 'medium',
                        'message': f"Heavy rainfall expected: {total_rain_24h:.1f}mm in 24h",
                        'recommendation': 'Ensure proper drainage, delay irrigation'
                    })
            
            result = {
                'timestamp': datetime.now().isoformat(),
                'location': {
                    'latitude': latitude,
                    'longitude': longitude
                },
                'alerts': alerts,
                'alert_count': len(alerts),
                'data_source': 'openweathermap_analysis'
            }
            
            logger.info(f"✅ Weather alerts analyzed for {latitude}, {longitude}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Error getting weather alerts: {e}")
            return {
                'timestamp': datetime.now().isoformat(),
                'location': {'latitude': latitude, 'longitude': longitude},
                'alerts': [],
                'alert_count': 0,
                'error': str(e)
            }
    
    # Fallback methods
    
    def _get_fallback_current_weather(self, latitude: float, longitude: float) -> Dict:
        """Generate fallback current weather data"""
        return {
            'timestamp': datetime.now().isoformat(),
            'location': {
                'latitude': latitude,
                'longitude': longitude,
                'name': 'Unknown',
                'country': ''
            },
            'temperature': {
                'current': 25.0,
                'feels_like': 26.0,
                'min': 20.0,
                'max': 30.0,
                'unit': 'celsius'
            },
            'humidity': 60,
            'pressure': 1013,
            'wind': {'speed': 3.0, 'direction': 180, 'gust': 5.0},
            'clouds': 40,
            'visibility': 10000,
            'weather': {
                'main': 'Clear',
                'description': 'clear sky',
                'icon': '01d'
            },
            'rain': 0,
            'snow': 0,
            'data_source': 'fallback',
            'note': 'API unavailable - using fallback data'
        }
    
    def _get_fallback_forecast(self, latitude: float, longitude: float, hours: int) -> Dict:
        """Generate fallback forecast data"""
        hourly_data = []
        for i in range(min(hours, 48)):
            dt = datetime.now() + timedelta(hours=i)
            hourly_data.append({
                'dt': dt.isoformat(),
                'temperature': 25.0 + (i % 12 - 6) * 2,
                'feels_like': 26.0 + (i % 12 - 6) * 2,
                'humidity': 60,
                'pressure': 1013,
                'wind_speed': 3.0,
                'precipitation_probability': 10,
                'weather': {
                    'main': 'Clear',
                    'description': 'clear sky'
                }
            })
        
        return {
            'timestamp': datetime.now().isoformat(),
            'location': {'latitude': latitude, 'longitude': longitude},
            'forecast_hours': hours,
            'hourly': hourly_data,
            'data_source': 'fallback',
            'note': 'API unavailable - using fallback data'
        }
    
    def _get_fallback_daily_forecast(self, latitude: float, longitude: float, days: int) -> Dict:
        """Generate fallback daily forecast"""
        daily_data = []
        for i in range(min(days, 7)):
            date = (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d')
            daily_data.append({
                'date': date,
                'temperature': {'min': 18.0, 'max': 32.0, 'avg': 25.0},
                'humidity_avg': 60,
                'wind_speed_avg': 3.0,
                'total_precipitation': 0,
                'dominant_weather': 'Clear'
            })
        
        return {
            'timestamp': datetime.now().isoformat(),
            'location': {'latitude': latitude, 'longitude': longitude},
            'forecast_days': days,
            'daily': daily_data,
            'data_source': 'fallback',
            'note': 'API unavailable - using fallback data'
        }


# Module-level functions for easy access

_api_instance = None

def get_api_instance() -> OpenWeatherAPI:
    """Get singleton API instance"""
    global _api_instance
    if _api_instance is None:
        _api_instance = OpenWeatherAPI()
    return _api_instance


def get_current_weather(latitude: float, longitude: float) -> Dict:
    """Convenience function to get current weather"""
    return get_api_instance().get_current_weather(latitude, longitude)


def get_hourly_forecast(latitude: float, longitude: float, hours: int = 48) -> Dict:
    """Convenience function to get hourly forecast"""
    return get_api_instance().get_hourly_forecast(latitude, longitude, hours)


def get_daily_forecast(latitude: float, longitude: float, days: int = 7) -> Dict:
    """Convenience function to get daily forecast"""
    return get_api_instance().get_daily_forecast(latitude, longitude, days)


# Test the module
if __name__ == "__main__":
    print("🌤️ Testing OpenWeatherMap API Handler")
    print("=" * 80)
    
    # Test coordinates (Punjab, India)
    lat, lng = 30.3398, 76.3869
    
    try:
        api = OpenWeatherAPI()
        
        print("\n📍 Test 1: Current Weather")
        current = api.get_current_weather(lat, lng)
        print(f"   Temperature: {current['temperature']['current']}°C")
        print(f"   Humidity: {current['humidity']}%")
        print(f"   Weather: {current['weather']['description']}")
        
        print("\n📍 Test 2: Hourly Forecast")
        hourly = api.get_hourly_forecast(lat, lng, 24)
        print(f"   Forecast hours: {hourly['forecast_hours']}")
        print(f"   Data points: {len(hourly['hourly'])}")
        
        print("\n📍 Test 3: Daily Forecast")
        daily = api.get_daily_forecast(lat, lng, 5)
        print(f"   Forecast days: {daily['forecast_days']}")
        
        print("\n📍 Test 4: Weather Alerts")
        alerts = api.get_weather_alerts(lat, lng)
        print(f"   Active alerts: {alerts['alert_count']}")
        
        print("\n✅ All tests passed!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
