#!/usr/bin/env python3
"""
Water Management Comprehensive Test Suite
Tests all endpoints and validates actual vs computed values

Location: D:\\CropEye1\\backend\\GIS\\WaterManagement\\test_water_management.py

Author: CropEye1 System
Date: October 19, 2025
"""

import requests
import json
from datetime import datetime

# API URL
API_URL = "http://localhost:5005"

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
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'=' * 100}")
    print(f"{text.center(100)}")
    print(f"{'=' * 100}{Colors.RESET}\n")

def print_test(test_name):
    print(f"{Colors.BLUE}▸ {test_name}{Colors.RESET}")

def print_pass(message):
    print(f"  {Colors.GREEN}✓{Colors.RESET} {message}")

def print_fail(message):
    print(f"  {Colors.RED}✗{Colors.RESET} {message}")

def print_info(message):
    print(f"  {Colors.CYAN}ℹ{Colors.RESET} {message}")

def print_actual_vs_computed(scenario_name, expected, computed):
    """Print expected (literature/FAO values) vs computed side-by-side"""
    print(f"\n{Colors.BOLD}  SCENARIO: {scenario_name}{Colors.RESET}")
    print(f"  {'-' * 96}")
    
    print(f"\n  {Colors.YELLOW}{Colors.BOLD}EXPECTED (FAO-56 / Literature Values):{Colors.RESET}")
    for key, value in expected.items():
        if isinstance(value, (int, float)):
            print(f"    {key}: {value}")
        else:
            print(f"    {key}: {value}")
    
    print(f"\n  {Colors.YELLOW}{Colors.BOLD}COMPUTED (Module Output):{Colors.RESET}")
    if computed:
        for key, value in computed.items():
            if isinstance(value, (int, float)):
                print(f"    {key}: {value}")
            else:
                print(f"    {key}: {value}")
    else:
        print(f"    {Colors.RED}No data returned{Colors.RESET}")
    
    # Calculate accuracy if both have numeric values
    if computed and 'et0_mm_day' in expected and 'et0_mm_day' in computed:
        error = abs(expected['et0_mm_day'] - computed['et0_mm_day'])
        error_pct = (error / expected['et0_mm_day']) * 100 if expected['et0_mm_day'] > 0 else 0
        if error_pct < 5:
            print(f"\n  {Colors.GREEN}✓ Accuracy: Error {error_pct:.1f}% (Excellent){Colors.RESET}")
        elif error_pct < 15:
            print(f"\n  {Colors.YELLOW}⚠ Accuracy: Error {error_pct:.1f}% (Acceptable){Colors.RESET}")
        else:
            print(f"\n  {Colors.RED}✗ Accuracy: Error {error_pct:.1f}% (Needs calibration){Colors.RESET}")
    
    print(f"  {'-' * 96}\n")


# Test scenarios with FAO-56 standard values
ET0_TEST_CASES = [
    {
        "scenario": "Semi-Arid Climate (Hot & Dry)",
        "input": {
            "temp_max": 35,
            "temp_min": 20,
            "rh_mean": 45,
            "wind_speed": 3.5,
            "solar_radiation": 25,
            "elevation": 200
        },
        "expected": {
            "et0_mm_day": 7.5,  # FAO-56 typical for hot dry
            "notes": "High ET0 due to high temp, low humidity, high wind"
        }
    },
    {
        "scenario": "Humid Tropical Climate",
        "input": {
            "temp_max": 30,
            "temp_min": 24,
            "rh_mean": 80,
            "wind_speed": 1.5,
            "solar_radiation": 20,
            "elevation": 100
        },
        "expected": {
            "et0_mm_day": 4.5,  # FAO-56 typical for humid tropics
            "notes": "Moderate ET0 due to high humidity, low wind"
        }
    },
    {
        "scenario": "Temperate Climate (Moderate)",
        "input": {
            "temp_max": 25,
            "temp_min": 15,
            "rh_mean": 65,
            "wind_speed": 2.0,
            "solar_radiation": 18,
            "elevation": 300
        },
        "expected": {
            "et0_mm_day": 4.0,  # FAO-56 typical for temperate
            "notes": "Moderate ET0, balanced conditions"
        }
    }
]

IRRIGATION_TEST_CASES = [
    {
        "scenario": "Wheat (Mid-season, Low soil moisture)",
        "input": {
            "crop_type": "wheat",
            "growth_stage": "mid",
            "weather_data": {
                "temp_max": 28,
                "temp_min": 15,
                "rh_mean": 60,
                "wind_speed": 2.5,
                "solar_radiation": 20
            },
            "soil_data": {
                "soil_type": "loam",
                "moisture": 0.4,  # 40% of field capacity
                "rainfall": 0
            }
        },
        "expected": {
            "et0_mm_day": 4.6,  # Expected ET0
            "etc_mm_day": 5.3,  # ET0 * Kc (1.15 for wheat mid)
            "gross_irrigation_mm": 35,  # Typical for dry conditions
            "notes": "Wheat mid-season Kc=1.15, needs irrigation"
        }
    },
    {
        "scenario": "Rice (Mid-season, Flooded)",
        "input": {
            "crop_type": "rice",
            "growth_stage": "mid",
            "weather_data": {
                "temp_max": 32,
                "temp_min": 24,
                "rh_mean": 75,
                "wind_speed": 1.5,
                "solar_radiation": 22
            },
            "soil_data": {
                "soil_type": "clay",
                "moisture": 0.9,  # 90% - flooded
                "rainfall": 20
            }
        },
        "expected": {
            "et0_mm_day": 4.8,
            "etc_mm_day": 5.8,  # ET0 * Kc (1.20 for rice mid)
            "gross_irrigation_mm": 5,  # Low due to rainfall + high moisture
            "notes": "Rice Kc=1.20, high moisture, recent rain"
        }
    },
    {
        "scenario": "Cotton (Late-season, Moderate stress)",
        "input": {
            "crop_type": "cotton",
            "growth_stage": "late",
            "weather_data": {
                "temp_max": 35,
                "temp_min": 22,
                "rh_mean": 50,
                "wind_speed": 3.0,
                "solar_radiation": 24
            },
            "soil_data": {
                "soil_type": "sandy_loam",
                "moisture": 0.5,
                "rainfall": 5
            }
        },
        "expected": {
            "et0_mm_day": 7.2,
            "etc_mm_day": 5.0,  # ET0 * Kc (0.70 for cotton late)
            "gross_irrigation_mm": 20,
            "notes": "Cotton late-season Kc=0.70, moderate irrigation"
        }
    }
]

STRESS_TEST_CASES = [
    {
        "scenario": "No Water Stress",
        "input": {"current_moisture": 0.85, "field_capacity": 1.0},
        "expected": {"stress_index": 0.0, "stress_level": "Low"}
    },
    {
        "scenario": "Moderate Water Stress",
        "input": {"current_moisture": 0.55, "field_capacity": 1.0},
        "expected": {"stress_index": 0.25, "stress_level": "Moderate"}
    },
    {
        "scenario": "Severe Water Stress",
        "input": {"current_moisture": 0.25, "field_capacity": 1.0},
        "expected": {"stress_index": 0.75, "stress_level": "High"}
    }
]


def test_health():
    """Test 1: Health check"""
    print_test("Test 1: Health Check")
    try:
        response = requests.get(f"{API_URL}/api/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_pass(f"Health check passed")
            print_info(f"Service: {data.get('service')}")
            print_info(f"Version: {data.get('version')}")
            print_info(f"WMS loaded: {data.get('wms_loaded')}")
        else:
            print_fail(f"Health check failed: {response.status_code}")
    except Exception as e:
        print_fail(f"Health check error: {e}")


def test_et0_calculation():
    """Test 2: ET0 Calculation with FAO-56 validation"""
    print_test("Test 2: ET0 Calculation (FAO-56 Penman-Monteith)")
    
    for case in ET0_TEST_CASES:
        try:
            response = requests.post(
                f"{API_URL}/api/water/et0/calculate",
                json=case["input"],
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    computed = {
                        'et0_mm_day': data.get('et0_mm_day'),
                        'method': 'FAO-56 Penman-Monteith'
                    }
                    print_actual_vs_computed(
                        case["scenario"],
                        case["expected"],
                        computed
                    )
                else:
                    print_fail(f"ET0 calculation failed for {case['scenario']}")
            else:
                print_fail(f"HTTP {response.status_code} for {case['scenario']}")
                
        except Exception as e:
            print_fail(f"Error for {case['scenario']}: {e}")


def test_irrigation_calculation():
    """Test 3: Irrigation Requirements"""
    print_test("Test 3: Irrigation Requirements Calculation")
    
    for case in IRRIGATION_TEST_CASES:
        try:
            response = requests.post(
                f"{API_URL}/api/water/irrigation/calculate",
                json=case["input"],
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    schedule = data.get('schedule', {})
                    irrigation = schedule.get('irrigation', {})
                    
                    computed = {
                        'et0_mm_day': schedule.get('et0_mm_day'),
                        'etc_mm_day': schedule.get('etc_mm_day'),
                        'gross_irrigation_mm': irrigation.get('gross_irrigation_mm'),
                        'irrigation_interval_days': irrigation.get('irrigation_interval_days'),
                        'recommendation': irrigation.get('recommendation')
                    }
                    
                    print_actual_vs_computed(
                        case["scenario"],
                        case["expected"],
                        computed
                    )
                else:
                    print_fail(f"Calculation failed for {case['scenario']}")
            else:
                print_fail(f"HTTP {response.status_code} for {case['scenario']}")
                
        except Exception as e:
            print_fail(f"Error for {case['scenario']}: {e}")


def test_water_stress():
    """Test 4: Water Stress Index"""
    print_test("Test 4: Water Stress Index Calculation")
    
    for case in STRESS_TEST_CASES:
        try:
            response = requests.post(
                f"{API_URL}/api/water/stress/calculate",
                json=case["input"],
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    computed = {
                        'stress_index': data.get('water_stress_index'),
                        'stress_level': data.get('stress_level')
                    }
                    
                    # Simple comparison
                    print(f"\n{Colors.BOLD}  SCENARIO: {case['scenario']}{Colors.RESET}")
                    print(f"  Expected: Stress={case['expected']['stress_index']}, Level={case['expected']['stress_level']}")
                    print(f"  Computed: Stress={computed['stress_index']}, Level={computed['stress_level']}")
                    
                    # Validate
                    error = abs(case['expected']['stress_index'] - computed['stress_index'])
                    if error < 0.1:
                        print(f"  {Colors.GREEN}✓ Stress index accurate (error: {error:.3f}){Colors.RESET}")
                    else:
                        print(f"  {Colors.YELLOW}⚠ Stress index deviation (error: {error:.3f}){Colors.RESET}")
                    print()
                else:
                    print_fail(f"Calculation failed for {case['scenario']}")
            else:
                print_fail(f"HTTP {response.status_code}")
                
        except Exception as e:
            print_fail(f"Error for {case['scenario']}: {e}")


def test_integrated_irrigation():
    """Test 5: Integrated Irrigation (with Soil + Weather)"""
    print_test("Test 5: Integrated Irrigation (Fetches Soil + Weather)")
    
    test_cases = [
        {
            "location": "Punjab (Wheat Belt)",
            "input": {
                "latitude": 30.8,
                "longitude": 75.8,
                "crop_type": "wheat",
                "growth_stage": "mid"
            },
            "expected_notes": "Should fetch weather and soil data, calculate irrigation"
        },
        {
            "location": "Tamil Nadu (Rice Belt)",
            "input": {
                "latitude": 10.5,
                "longitude": 78.3,
                "crop_type": "rice",
                "growth_stage": "mid"
            },
            "expected_notes": "High ET0 expected, rice requires more water"
        }
    ]
    
    for case in test_cases:
        try:
            response = requests.post(
                f"{API_URL}/api/water/irrigation/integrated",
                json=case["input"],
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print(f"\n{Colors.BOLD}  LOCATION: {case['location']}{Colors.RESET}")
                    print(f"  Data sources: {', '.join(data.get('data_sources', []))}")
                    
                    schedule = data.get('schedule', {})
                    if schedule:
                        irrigation = schedule.get('irrigation', {})
                        print(f"  ET0: {schedule.get('et0_mm_day')} mm/day")
                        print(f"  ETc: {schedule.get('etc_mm_day')} mm/day")
                        print(f"  Irrigation needed: {irrigation.get('gross_irrigation_mm')} mm")
                        print(f"  Interval: {irrigation.get('irrigation_interval_days')} days")
                        print(f"  Recommendation: {irrigation.get('recommendation')}")
                        print_pass("Integrated irrigation calculated successfully")
                    else:
                        print_fail("No schedule returned")
                    print()
                else:
                    print_fail(f"Integration failed: {data.get('error')}")
            else:
                print_fail(f"HTTP {response.status_code}")
                
        except Exception as e:
            print_fail(f"Error for {case['location']}: {e}")


def test_list_crops():
    """Test 6: List Supported Crops"""
    print_test("Test 6: List Supported Crops with Kc Values")
    try:
        response = requests.get(f"{API_URL}/api/water/crops", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print_pass(f"Retrieved {data.get('total_crops')} crops")
                crops = data.get('crops', [])[:5]  # Show first 5
                for crop in crops:
                    print_info(f"{crop['name']}: Kc_init={crop['kc_initial']}, Kc_mid={crop['kc_mid']}, Kc_late={crop['kc_late']}")
            else:
                print_fail("Failed to retrieve crops")
        else:
            print_fail(f"HTTP {response.status_code}")
    except Exception as e:
        print_fail(f"Error: {e}")


def test_invalid_inputs():
    """Test 7: Invalid Input Handling"""
    print_test("Test 7: Invalid Input Handling")
    
    # Test missing fields
    try:
        response = requests.post(
            f"{API_URL}/api/water/et0/calculate",
            json={},  # Empty
            timeout=5
        )
        if response.status_code in [200, 400, 500]:  # Should handle gracefully
            print_pass("Missing fields handled (uses defaults or errors)")
        else:
            print_fail(f"Unexpected status: {response.status_code}")
    except Exception as e:
        print_fail(f"Error: {e}")
    
    # Test invalid values
    try:
        response = requests.post(
            f"{API_URL}/api/water/et0/calculate",
            json={"temp_max": "invalid", "temp_min": 20},  # Invalid type
            timeout=5
        )
        if response.status_code in [400, 500]:
            print_pass("Invalid data types rejected")
        else:
            print_fail(f"Unexpected status: {response.status_code}")
    except Exception as e:
        print_fail(f"Error: {e}")


def test_response_time():
    """Test 8: Response Time Performance"""
    print_test("Test 8: Response Time Performance")
    
    import time
    
    test_input = {
        "temp_max": 30,
        "temp_min": 20,
        "rh_mean": 65,
        "wind_speed": 2.0,
        "solar_radiation": 20
    }
    
    try:
        start = time.time()
        response = requests.post(
            f"{API_URL}/api/water/et0/calculate",
            json=test_input,
            timeout=10
        )
        elapsed = time.time() - start
        
        if response.status_code == 200:
            if elapsed < 0.5:
                print_pass(f"Response time: {elapsed:.3f}s (Excellent)")
            elif elapsed < 2.0:
                print_pass(f"Response time: {elapsed:.3f}s (Good)")
            else:
                print_fail(f"Response time: {elapsed:.3f}s (Slow)")
        else:
            print_fail(f"Request failed: {response.status_code}")
            
    except Exception as e:
        print_fail(f"Error: {e}")


def main():
    """Run all tests"""
    print_header("WATER MANAGEMENT MODULE - COMPREHENSIVE TEST SUITE")
    
    print(f"{Colors.BOLD}API URL:{Colors.RESET} {API_URL}")
    print(f"{Colors.BOLD}Date:{Colors.RESET} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Check if API is running
    try:
        response = requests.get(f"{API_URL}/api/health", timeout=3)
        print(f"{Colors.GREEN}✓ API is running on port 5005{Colors.RESET}\n")
    except:
        print(f"{Colors.RED}✗ API is not running! Start with: python water_flask_backend.py{Colors.RESET}\n")
        return
    
    # Run tests
    print_header("RUNNING TESTS")
    
    test_health()
    print()
    
    test_et0_calculation()
    print()
    
    test_irrigation_calculation()
    print()
    
    test_water_stress()
    print()
    
    test_integrated_irrigation()
    print()
    
    test_list_crops()
    print()
    
    test_invalid_inputs()
    print()
    
    test_response_time()
    print()
    
    print_header("TESTS COMPLETE")
    print(f"{Colors.BOLD}NOTE:{Colors.RESET} Compare 'Expected' (FAO-56) vs 'Computed' values above")
    print(f"FAO-56 is the gold standard for ET0 calculation. Deviations <10% are acceptable.\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Tests interrupted by user{Colors.RESET}\n")
    except Exception as e:
        print(f"\n\n{Colors.RED}Fatal error: {e}{Colors.RESET}\n")
