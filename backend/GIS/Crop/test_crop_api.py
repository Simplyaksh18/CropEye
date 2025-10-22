#!/usr/bin/env python3
"""
Crop Recommendation Flask API Test Suite
Tests all endpoints and displays actual vs computed values

Location: D:\\CropEye1\\backend\\GIS\\CropRecommendation\\test_crop_api.py

Author: CropEye1 System
Date: October 19, 2025
"""

import requests
import json
from datetime import datetime

# API URL
API_URL = "http://localhost:5004"

# Colors for terminal
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def print_header(text):
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'=' * 90}")
    print(f"{text.center(90)}")
    print(f"{'=' * 90}{Colors.RESET}\n")

def print_test(test_name):
    print(f"{Colors.BLUE}▸ {test_name}{Colors.RESET}")

def print_pass(message):
    print(f"  {Colors.GREEN}✓{Colors.RESET} {message}")

def print_fail(message):
    print(f"  {Colors.RED}✗{Colors.RESET} {message}")

def print_info(message):
    print(f"  {Colors.CYAN}ℹ{Colors.RESET} {message}")

def print_actual_vs_computed(location, official_data, computed_data):
    """Print official vs computed recommendations side-by-side"""
    print(f"\n{Colors.BOLD}  LOCATION: {location}{Colors.RESET}")
    print(f"  {'-' * 86}")
    
    print(f"\n  {Colors.YELLOW}{Colors.BOLD}OFFICIAL (Extension/Reference):{Colors.RESET}")
    print(f"    Most Suitable: {', '.join(official_data['most_suitable'])}")
    print(f"    Moderately Suitable: {', '.join(official_data.get('moderate', []))}")
    print(f"    Notes: {official_data.get('notes', 'N/A')}")
    
    print(f"\n  {Colors.YELLOW}{Colors.BOLD}COMPUTED (Module Output):{Colors.RESET}")
    if computed_data and 'recommendations' in computed_data:
        recs = computed_data['recommendations'][:5]
        for i, crop in enumerate(recs, 1):
            print(f"    {i}. {crop['crop'].upper()} - Score: {crop['score']}")
            print(f"       └─ pH: {crop['ph_suit']}, Rain: {crop['rain_suit']}, Temp: {crop['temp_suit']}, NDVI: {crop['ndvi']}")
    else:
        print(f"    {Colors.RED}No recommendations returned{Colors.RESET}")
    
    print(f"  {'-' * 86}\n")


# Test data with official recommendations
TEST_CASES = [
    {
        "location": "Punjab (Kharif Season)",
        "input": {
            "latitude": 30.8,
            "longitude": 75.8,
            "ph": 7.1,
            "rainfall": 900,
            "temp_mean": 30,
            "ndvi": 0.62
        },
        "official": {
            "most_suitable": ["rice", "maize"],
            "moderate": ["millets"],
            "notes": "Kharif: Rice ideal for pH 5.5-7.0, rainfall 800+mm, temp 28-32°C"
        }
    },
    {
        "location": "Maharashtra (Rabi Season)",
        "input": {
            "latitude": 19.5,
            "longitude": 76.0,
            "ph": 6.3,
            "rainfall": 650,
            "temp_mean": 23,
            "ndvi": 0.48
        },
        "official": {
            "most_suitable": ["wheat", "barley"],
            "moderate": ["gram"],
            "notes": "Rabi: Wheat for pH 6.0-7.5, rainfall 450-650mm, temp 20-25°C"
        }
    },
    {
        "location": "Tamil Nadu (Zaid/Summer)",
        "input": {
            "latitude": 10.5,
            "longitude": 78.3,
            "ph": 8.0,
            "rainfall": 600,
            "temp_mean": 29,
            "ndvi": 0.41
        },
        "official": {
            "most_suitable": ["cotton", "sunflower"],
            "moderate": ["sorghum"],
            "notes": "Summer: Cotton for pH 7.0-8.5, rainfall 500-900mm, sandy/black soil"
        }
    }
]


def test_health_check():
    """Test 1: Health check"""
    print_test("Test 1: Health Check")
    try:
        response = requests.get(f"{API_URL}/api/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_pass(f"Health check passed")
            print_info(f"Service: {data.get('service')}")
            print_info(f"Version: {data.get('version')}")
            print_info(f"Recommender loaded: {data.get('recommender_loaded')}")
        else:
            print_fail(f"Health check failed: {response.status_code}")
    except Exception as e:
        print_fail(f"Health check error: {e}")


def test_list_crops():
    """Test 2: List available crops"""
    print_test("Test 2: List Available Crops")
    try:
        response = requests.get(f"{API_URL}/api/crop/list", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print_pass(f"Crops list retrieved")
                print_info(f"Total crops: {data.get('total_crops')}")
                crops = data.get('crops', [])[:5]
                for crop in crops:
                    print_info(f"  • {crop['name']}: pH {crop['ph_range']}, Rain {crop['rainfall_range_mm']}mm")
            else:
                print_fail("Failed to retrieve crops list")
        else:
            print_fail(f"Failed with status: {response.status_code}")
    except Exception as e:
        print_fail(f"Error: {e}")


def test_basic_recommendation():
    """Test 3: Basic crop recommendation"""
    print_test("Test 3: Basic Crop Recommendation")
    
    for case in TEST_CASES:
        try:
            response = requests.post(
                f"{API_URL}/api/crop/recommend",
                json=case["input"],
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print_actual_vs_computed(
                        case["location"],
                        case["official"],
                        data
                    )
                else:
                    print_fail(f"Recommendation failed for {case['location']}")
            else:
                print_fail(f"HTTP {response.status_code} for {case['location']}")
                
        except Exception as e:
            print_fail(f"Error for {case['location']}: {e}")


def test_integrated_recommendation():
    """Test 4: Integrated recommendation (with other modules)"""
    print_test("Test 4: Integrated Recommendation (Soil + Weather + NDVI)")
    
    test_location = {
        "location": "Punjab (Integrated)",
        "input": {
            "latitude": 30.8,
            "longitude": 75.8
        },
        "official": {
            "most_suitable": ["rice", "wheat (seasonal)"],
            "moderate": ["maize", "cotton"],
            "notes": "Based on integrated soil, weather, and NDVI data"
        }
    }
    
    try:
        response = requests.post(
            f"{API_URL}/api/crop/recommend/integrated",
            json=test_location["input"],
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print_pass(f"Integrated recommendation successful")
                print_info(f"Data sources: {', '.join(data.get('data_sources', []))}")
                
                if 'input_parameters' in data:
                    params = data['input_parameters']
                    print_info(f"Detected pH: {params.get('ph')}")
                    print_info(f"Detected temp: {params.get('temp_mean')}°C")
                    print_info(f"Detected rainfall: {params.get('rainfall')}mm")
                    print_info(f"Detected NDVI: {params.get('ndvi')}")
                
                print_actual_vs_computed(
                    test_location["location"],
                    test_location["official"],
                    data
                )
            else:
                print_fail("Integrated recommendation failed")
                print_info(f"Error: {data.get('error', 'Unknown')}")
        else:
            print_fail(f"HTTP {response.status_code}")
            
    except Exception as e:
        print_fail(f"Error: {e}")


def test_invalid_input():
    """Test 5: Invalid input handling"""
    print_test("Test 5: Invalid Input Handling")
    
    # Test missing fields
    try:
        response = requests.post(
            f"{API_URL}/api/crop/recommend",
            json={"latitude": 30.0},  # Missing required fields
            timeout=5
        )
        
        if response.status_code == 400:
            print_pass("Missing fields rejected correctly (400 Bad Request)")
        else:
            print_fail(f"Unexpected status: {response.status_code}")
    except Exception as e:
        print_fail(f"Error: {e}")
    
    # Test invalid values
    try:
        response = requests.post(
            f"{API_URL}/api/crop/recommend",
            json={
                "latitude": 30.0,
                "longitude": 75.0,
                "ph": "invalid",  # Invalid type
                "rainfall": 900,
                "temp_mean": 30
            },
            timeout=5
        )
        
        if response.status_code in [400, 500]:
            print_pass("Invalid data types handled correctly")
        else:
            print_fail(f"Unexpected status: {response.status_code}")
    except Exception as e:
        print_fail(f"Error: {e}")


def test_response_time():
    """Test 6: Response time"""
    print_test("Test 6: Response Time Test")
    
    import time
    
    test_input = {
        "latitude": 30.8,
        "longitude": 75.8,
        "ph": 7.0,
        "rainfall": 850,
        "temp_mean": 28,
        "ndvi": 0.6
    }
    
    try:
        start = time.time()
        response = requests.post(
            f"{API_URL}/api/crop/recommend",
            json=test_input,
            timeout=10
        )
        elapsed = time.time() - start
        
        if response.status_code == 200:
            if elapsed < 1.0:
                print_pass(f"Response time: {elapsed:.3f}s (excellent)")
            elif elapsed < 3.0:
                print_pass(f"Response time: {elapsed:.3f}s (good)")
            else:
                print_fail(f"Response time: {elapsed:.3f}s (slow)")
        else:
            print_fail(f"Request failed: {response.status_code}")
            
    except Exception as e:
        print_fail(f"Error: {e}")


def main():
    """Run all tests"""
    print_header("CROP RECOMMENDATION API TEST SUITE")
    
    print(f"{Colors.BOLD}API URL:{Colors.RESET} {API_URL}")
    print(f"{Colors.BOLD}Date:{Colors.RESET} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Check if API is running
    try:
        response = requests.get(f"{API_URL}/api/health", timeout=3)
        print(f"{Colors.GREEN}✓ API is running on port 5004{Colors.RESET}\n")
    except:
        print(f"{Colors.RED}✗ API is not running! Start with: python crop_flask_backend.py{Colors.RESET}\n")
        return
    
    # Run tests
    print_header("RUNNING TESTS")
    
    test_health_check()
    print()
    
    test_list_crops()
    print()
    
    test_basic_recommendation()
    print()
    
    test_integrated_recommendation()
    print()
    
    test_invalid_input()
    print()
    
    test_response_time()
    print()
    
    print_header("TESTS COMPLETE")
    print(f"{Colors.BOLD}NOTE:{Colors.RESET} Compare 'Official' vs 'Computed' values above")
    print(f"Adjust crop_params_india.json if computed values differ significantly from official recommendations.\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Tests interrupted by user{Colors.RESET}\n")
    except Exception as e:
        print(f"\n\n{Colors.RED}Fatal error: {e}{Colors.RESET}\n")
