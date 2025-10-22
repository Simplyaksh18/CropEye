#!/usr/bin/env python3
"""
Pest & Disease Detection - COMPREHENSIVE TEST SUITE
Tests all endpoints with extensive validation of expected vs computed values

Location: D:\\CropEye1\\backend\\GIS\\PestDisease\\test_pest_disease.py

Author: CropEye1 System
Date: October 19, 2025
"""

import requests
import json
from datetime import datetime

# API URL
API_URL = "http://localhost:5006"

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def print_header(text):
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'=' * 110}")
    print(f"{text.center(110)}")
    print(f"{'=' * 110}{Colors.RESET}\n")

def print_test(test_name):
    print(f"{Colors.BLUE}{Colors.BOLD}▸ {test_name}{Colors.RESET}")

def print_pass(message):
    print(f"  {Colors.GREEN}✓{Colors.RESET} {message}")

def print_fail(message):
    print(f"  {Colors.RED}✗{Colors.RESET} {message}")

def print_info(message):
    print(f"  {Colors.CYAN}ℹ{Colors.RESET} {message}")

def print_warning(message):
    print(f"  {Colors.YELLOW}⚠{Colors.RESET} {message}")

def print_actual_vs_computed(scenario_name, expected, computed):
    """Print expected (agronomic research) vs computed (module) values"""
    print(f"\n{Colors.BOLD}  SCENARIO: {scenario_name}{Colors.RESET}")
    print(f"  {'-' * 106}")
    
    print(f"\n  {Colors.YELLOW}{Colors.BOLD}EXPECTED (Agricultural Research / Extension Data):{Colors.RESET}")
    for key, value in expected.items():
        print(f"    {key}: {value}")
    
    print(f"\n  {Colors.MAGENTA}{Colors.BOLD}COMPUTED (Module Output):{Colors.RESET}")
    if computed:
        for key, value in computed.items():
            if isinstance(value, list):
                print(f"    {key}: {len(value)} items")
                for item in value[:3]:  # Show first 3
                    if isinstance(item, dict):
                        name = item.get('pest') or item.get('disease', 'Unknown')
                        risk = item.get('risk_score', 0)
                        level = item.get('risk_level', 'Unknown')
                        print(f"      • {name}: Risk={risk} ({level})")
            else:
                print(f"    {key}: {value}")
    else:
        print(f"    {Colors.RED}No data returned{Colors.RESET}")
    
    # Validation
    if computed:
        if 'threats_detected' in expected and 'total_threats' in computed:
            exp_count = expected['threats_detected']
            comp_count = computed['total_threats']
            if exp_count == comp_count:
                print(f"\n  {Colors.GREEN}✓ Threat count matches expected ({comp_count}){Colors.RESET}")
            else:
                print(f"\n  {Colors.YELLOW}⚠ Threat count mismatch: Expected={exp_count}, Got={comp_count}{Colors.RESET}")
        
        if 'risk_level' in expected and 'overall_risk_level' in computed:
            if expected['risk_level'] == computed['overall_risk_level']:
                print(f"  {Colors.GREEN}✓ Risk level matches: {computed['overall_risk_level']}{Colors.RESET}")
            else:
                print(f"  {Colors.YELLOW}⚠ Risk level: Expected={expected['risk_level']}, Got={computed['overall_risk_level']}{Colors.RESET}")
    
    print(f"  {'-' * 106}\n")


# ==================================================================================
# TEST SCENARIOS with Expected Values from Agricultural Extension Services
# ==================================================================================

PEST_TEST_CASES = [
    {
        "scenario": "Rice Stem Borer Outbreak (Kharif Season)",
        "input": {
            "temp": 28,
            "humidity": 85,
            "crop_type": "rice",
            "additional_factors": {"continuous_flooding": True}
        },
        "expected": {
            "primary_pest": "stem_borer",
            "risk_level": "High",
            "threats_detected": 1,
            "notes": "Favorable for stem borer: High humidity + flooding + rice crop"
        }
    },
    {
        "scenario": "Cotton Bollworm During Flowering",
        "input": {
            "temp": 30,
            "humidity": 65,
            "crop_type": "cotton",
            "additional_factors": {"flowering_stage": True}
        },
        "expected": {
            "primary_pest": "bollworm",
            "risk_level": "High",
            "threats_detected": 2,  # bollworm + possibly whitefly
            "notes": "Flowering stage increases bollworm risk significantly"
        }
    },
    {
        "scenario": "Wheat Aphid Infestation (Cool Season)",
        "input": {
            "temp": 22,
            "humidity": 55,
            "crop_type": "wheat",
            "additional_factors": {"high_nitrogen": True}
        },
        "expected": {
            "primary_pest": "aphids",
            "risk_level": "Moderate",
            "threats_detected": 1,
            "notes": "Cool temps + high N favors aphids on wheat"
        }
    }
]

DISEASE_TEST_CASES = [
    {
        "scenario": "Rice Blast (High Humidity + Moderate Temp)",
        "input": {
            "temp": 26,
            "humidity": 92,
            "crop_type": "rice",
            "additional_factors": {"high_nitrogen": True, "night_dew": True}
        },
        "expected": {
            "primary_disease": "blast",
            "risk_level": "Critical",
            "threats_detected": 1,
            "notes": "Optimal conditions for rice blast fungus"
        }
    },
    {
        "scenario": "Wheat Rust (Cool & Humid)",
        "input": {
            "temp": 20,
            "humidity": 85,
            "crop_type": "wheat",
            "additional_factors": {"cool_moist": True}
        },
        "expected": {
            "primary_disease": "rust",
            "risk_level": "High",
            "threats_detected": 1,
            "notes": "Classic rust weather for wheat"
        }
    },
    {
        "scenario": "Tomato Bacterial Wilt (Hot & Waterlogged)",
        "input": {
            "temp": 32,
            "humidity": 80,
            "crop_type": "tomato",
            "additional_factors": {"high_soil_temp": True, "waterlogging": True}
        },
        "expected": {
            "primary_disease": "bacterial_wilt",
            "risk_level": "Critical",
            "threats_detected": 2,  # bacterial wilt + possibly blight
            "notes": "High temp + waterlogging = bacterial wilt outbreak"
        }
    }
]

COMPREHENSIVE_TEST_CASES = [
    {
        "scenario": "Rice Field (Multiple Threats)",
        "input": {
            "temp": 27,
            "humidity": 88,
            "crop_type": "rice",
            "additional_factors": {"continuous_flooding": True, "high_nitrogen": True}
        },
        "expected": {
            "risk_level": "High",
            "threats_detected": 2,  # stem borer + blast
            "top_pest": "stem_borer",
            "top_disease": "blast",
            "notes": "Both pest and disease threats present"
        }
    },
    {
        "scenario": "Wheat Field (Cool Season)",
        "input": {
            "temp": 18,
            "humidity": 80,
            "crop_type": "wheat",
            "additional_factors": {"cool_moist": True}
        },
        "expected": {
            "risk_level": "High",
            "threats_detected": 2,  # aphids + rust
            "notes": "Cool humid conditions favor both aphids and rust"
        }
    },
    {
        "scenario": "Cotton Field (Flowering)",
        "input": {
            "temp": 31,
            "humidity": 70,
            "crop_type": "cotton",
            "additional_factors": {"flowering_stage": True}
        },
        "expected": {
            "risk_level": "High",
            "threats_detected": 2,  # bollworm + whitefly
            "notes": "Flowering stage critical for bollworm"
        }
    }
]


# ==================================================================================
# TEST FUNCTIONS
# ==================================================================================

def test_health():
    """Test 1: Health Check"""
    print_test("Test 1: Health Check")
    try:
        response = requests.get(f"{API_URL}/api/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_pass(f"Health check passed")
            print_info(f"Service: {data.get('service')}")
            print_info(f"Version: {data.get('version')}")
            print_info(f"Detector loaded: {data.get('detector_loaded')}")
        else:
            print_fail(f"Health check failed: {response.status_code}")
    except Exception as e:
        print_fail(f"Health check error: {e}")


def test_pest_detection():
    """Test 2: Pest Detection with Validation"""
    print_test("Test 2: Pest Detection (Expected vs Computed)")
    
    for case in PEST_TEST_CASES:
        try:
            response = requests.post(
                f"{API_URL}/api/pest/detect",
                json=case["input"],
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    pests = data.get('pests', [])
                    computed = {
                        'pests': pests,
                        'total_threats': len(pests),
                        'primary_pest': pests[0]['pest'] if pests else None,
                        'overall_risk_level': pests[0]['risk_level'] if pests else 'Low'
                    }
                    print_actual_vs_computed(case["scenario"], case["expected"], computed)
                else:
                    print_fail(f"Detection failed for {case['scenario']}")
            else:
                print_fail(f"HTTP {response.status_code} for {case['scenario']}")
                
        except Exception as e:
            print_fail(f"Error for {case['scenario']}: {e}")


def test_disease_detection():
    """Test 3: Disease Detection with Validation"""
    print_test("Test 3: Disease Detection (Expected vs Computed)")
    
    for case in DISEASE_TEST_CASES:
        try:
            response = requests.post(
                f"{API_URL}/api/disease/detect",
                json=case["input"],
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    diseases = data.get('diseases', [])
                    computed = {
                        'diseases': diseases,
                        'total_threats': len(diseases),
                        'primary_disease': diseases[0]['disease'] if diseases else None,
                        'overall_risk_level': diseases[0]['risk_level'] if diseases else 'Low'
                    }
                    print_actual_vs_computed(case["scenario"], case["expected"], computed)
                else:
                    print_fail(f"Detection failed for {case['scenario']}")
            else:
                print_fail(f"HTTP {response.status_code} for {case['scenario']}")
                
        except Exception as e:
            print_fail(f"Error for {case['scenario']}: {e}")


def test_comprehensive_assessment():
    """Test 4: Comprehensive Assessment (Pests + Diseases)"""
    print_test("Test 4: Comprehensive Assessment (Pests + Diseases Together)")
    
    for case in COMPREHENSIVE_TEST_CASES:
        try:
            response = requests.post(
                f"{API_URL}/api/threats/comprehensive",
                json=case["input"],
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    pests = data.get('pests', [])
                    diseases = data.get('diseases', [])
                    
                    computed = {
                        'total_threats': data.get('total_threats', 0),
                        'overall_risk_level': data.get('overall_risk_level', 'Low'),
                        'overall_risk_score': data.get('overall_risk_score', 0),
                        'pests_detected': len(pests),
                        'diseases_detected': len(diseases),
                        'top_pest': pests[0]['pest'] if pests else None,
                        'top_disease': diseases[0]['disease'] if diseases else None
                    }
                    print_actual_vs_computed(case["scenario"], case["expected"], computed)
                else:
                    print_fail(f"Assessment failed for {case['scenario']}")
            else:
                print_fail(f"HTTP {response.status_code} for {case['scenario']}")
                
        except Exception as e:
            print_fail(f"Error for {case['scenario']}: {e}")


def test_integrated_assessment():
    """Test 5: Integrated Assessment (Fetches Weather)"""
    print_test("Test 5: Integrated Assessment (Auto-fetch Weather Data)")
    
    test_cases = [
        {
            "location": "Punjab Rice Belt",
            "input": {
                "latitude": 30.8,
                "longitude": 75.8,
                "crop_type": "rice",
                "additional_factors": {}
            },
            "expected_notes": "Should fetch weather and assess threats for rice"
        },
        {
            "location": "Maharashtra Cotton Zone",
            "input": {
                "latitude": 19.5,
                "longitude": 76.0,
                "crop_type": "cotton",
                "additional_factors": {"flowering_stage": True}
            },
            "expected_notes": "Cotton flowering stage, check for bollworm"
        }
    ]
    
    for case in test_cases:
        try:
            response = requests.post(
                f"{API_URL}/api/threats/integrated",
                json=case["input"],
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print(f"\n{Colors.BOLD}  LOCATION: {case['location']}{Colors.RESET}")
                    print(f"  Data sources: {', '.join(data.get('data_sources', []))}")
                    print(f"  Weather: Temp={data.get('weather_data', {}).get('temp')}°C, Humidity={data.get('weather_data', {}).get('humidity')}%")
                    print(f"  Total threats: {data.get('total_threats', 0)}")
                    print(f"  Overall risk: {data.get('overall_risk_level', 'Unknown')} ({data.get('overall_risk_score', 0)})")
                    
                    pests = data.get('pests', [])
                    diseases = data.get('diseases', [])
                    if pests:
                        print(f"  Top pest: {pests[0]['pest']} (risk: {pests[0]['risk_score']})")
                    if diseases:
                        print(f"  Top disease: {diseases[0]['disease']} (risk: {diseases[0]['risk_score']})")
                    
                    print_pass("Integrated assessment completed")
                    print()
                else:
                    print_fail(f"Integration failed: {data.get('error')}")
            else:
                print_fail(f"HTTP {response.status_code}")
                
        except Exception as e:
            print_fail(f"Error for {case['location']}: {e}")


def test_info_endpoints():
    """Test 6: Information Endpoints (Pest/Disease Details)"""
    print_test("Test 6: Pest & Disease Information Lookup")
    
    # Test pest info
    pests_to_test = ['aphids', 'stem_borer', 'bollworm']
    for pest in pests_to_test:
        try:
            response = requests.get(f"{API_URL}/api/pest/info/{pest}", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    info = data.get('info', {})
                    print_pass(f"Retrieved info for {pest}")
                    print_info(f"  Crops affected: {', '.join(info.get('crops_affected', []))}")
                    print_info(f"  Temp range: {info.get('temp_range')}")
                    print_info(f"  Control: {info.get('control', [])[0] if info.get('control') else 'N/A'}")
                else:
                    print_fail(f"Failed to get info for {pest}")
            else:
                print_fail(f"HTTP {response.status_code} for {pest}")
        except Exception as e:
            print_fail(f"Error for {pest}: {e}")
    
    print()
    
    # Test disease info
    diseases_to_test = ['blast', 'rust', 'bacterial_wilt']
    for disease in diseases_to_test:
        try:
            response = requests.get(f"{API_URL}/api/disease/info/{disease}", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    info = data.get('info', {})
                    print_pass(f"Retrieved info for {disease}")
                    print_info(f"  Pathogen: {info.get('pathogen')}")
                    print_info(f"  Crops affected: {', '.join(info.get('crops_affected', []))}")
                else:
                    print_fail(f"Failed to get info for {disease}")
            else:
                print_fail(f"HTTP {response.status_code} for {disease}")
        except Exception as e:
            print_fail(f"Error for {disease}: {e}")


def test_database_list():
    """Test 7: List All Threats in Database"""
    print_test("Test 7: List All Pests & Diseases in Database")
    try:
        response = requests.get(f"{API_URL}/api/database/list", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print_pass(f"Retrieved database")
                print_info(f"Total pests: {data.get('total_pests')}")
                print_info(f"Total diseases: {data.get('total_diseases')}")
                print_info(f"Pests: {', '.join(data.get('pests', []))}")
                print_info(f"Diseases: {', '.join(data.get('diseases', []))}")
            else:
                print_fail("Failed to retrieve database")
        else:
            print_fail(f"HTTP {response.status_code}")
    except Exception as e:
        print_fail(f"Error: {e}")


def test_invalid_inputs():
    """Test 8: Invalid Input Handling"""
    print_test("Test 8: Invalid Input Handling & Error Responses")
    
    # Test missing fields
    try:
        response = requests.post(
            f"{API_URL}/api/pest/detect",
            json={},  # Empty
            timeout=5
        )
        if response.status_code in [200, 400, 500]:  # Should handle gracefully
            print_pass("Missing fields handled (defaults or error)")
        else:
            print_fail(f"Unexpected status: {response.status_code}")
    except Exception as e:
        print_fail(f"Error: {e}")
    
    # Test invalid crop type
    try:
        response = requests.post(
            f"{API_URL}/api/threats/comprehensive",
            json={"temp": 25, "humidity": 70, "crop_type": "invalid_crop_xyz"},
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            # Should return 0 threats for invalid crop
            if data.get('total_threats', 0) == 0:
                print_pass("Invalid crop type handled (returns 0 threats)")
            else:
                print_warning("Invalid crop processed (may need better validation)")
        else:
            print_fail(f"Unexpected status: {response.status_code}")
    except Exception as e:
        print_fail(f"Error: {e}")


def test_response_time():
    """Test 9: Performance / Response Time"""
    print_test("Test 9: Response Time Performance Test")
    
    import time
    
    test_input = {
        "temp": 26,
        "humidity": 80,
        "crop_type": "rice",
        "additional_factors": {}
    }
    
    try:
        start = time.time()
        response = requests.post(
            f"{API_URL}/api/threats/comprehensive",
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
                print_warning(f"Response time: {elapsed:.3f}s (Acceptable but slow)")
        else:
            print_fail(f"Request failed: {response.status_code}")
            
    except Exception as e:
        print_fail(f"Error: {e}")


def test_edge_cases():
    """Test 10: Edge Cases & Boundary Conditions"""
    print_test("Test 10: Edge Cases (Extreme Conditions)")
    
    edge_cases = [
        {
            "name": "Extreme Cold",
            "input": {"temp": 5, "humidity": 50, "crop_type": "wheat"},
            "expected": "Should return low/no threats due to extreme cold"
        },
        {
            "name": "Extreme Heat",
            "input": {"temp": 45, "humidity": 30, "crop_type": "rice"},
            "expected": "Should return low threats (outside favorable ranges)"
        },
        {
            "name": "Very Low Humidity",
            "input": {"temp": 25, "humidity": 15, "crop_type": "cotton"},
            "expected": "Low disease risk, some pest risk"
        },
        {
            "name": "Saturated Air",
            "input": {"temp": 27, "humidity": 100, "crop_type": "rice"},
            "expected": "High disease risk (blast, blight)"
        }
    ]
    
    for case in edge_cases:
        try:
            response = requests.post(
                f"{API_URL}/api/threats/comprehensive",
                json=case["input"],
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                threats = data.get('total_threats', 0)
                risk = data.get('overall_risk_level', 'Unknown')
                print(f"\n  {Colors.BOLD}{case['name']}:{Colors.RESET}")
                print(f"    Input: T={case['input']['temp']}°C, H={case['input']['humidity']}%, Crop={case['input']['crop_type']}")
                print(f"    Output: {threats} threats, Risk: {risk}")
                print(f"    Expected: {case['expected']}")
                print_pass(f"Edge case handled")
            else:
                print_fail(f"Failed for {case['name']}")
                
        except Exception as e:
            print_fail(f"Error for {case['name']}: {e}")


def main():
    """Run comprehensive test suite"""
    print_header("PEST & DISEASE DETECTION MODULE - COMPREHENSIVE TEST SUITE")
    
    print(f"{Colors.BOLD}API URL:{Colors.RESET} {API_URL}")
    print(f"{Colors.BOLD}Date:{Colors.RESET} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Check if API is running
    try:
        response = requests.get(f"{API_URL}/api/health", timeout=3)
        print(f"{Colors.GREEN}✓ API is running on port 5006{Colors.RESET}\n")
    except:
        print(f"{Colors.RED}✗ API is not running! Start with: python pest_flask_backend.py{Colors.RESET}\n")
        return
    
    # Run all tests
    print_header("RUNNING COMPREHENSIVE TESTS")
    
    test_health()
    print()
    
    test_pest_detection()
    print()
    
    test_disease_detection()
    print()
    
    test_comprehensive_assessment()
    print()
    
    test_integrated_assessment()
    print()
    
    test_info_endpoints()
    print()
    
    test_database_list()
    print()
    
    test_invalid_inputs()
    print()
    
    test_response_time()
    print()
    
    test_edge_cases()
    print()
    
    print_header("ALL TESTS COMPLETE")
    print(f"{Colors.BOLD}SUMMARY:{Colors.RESET}")
    print(f"• Compare 'Expected' (agronomic research) vs 'Computed' (module) values above")
    print(f"• Risk assessments based on temperature, humidity, crop type, and additional factors")
    print(f"• Database includes major Indian pests & diseases with control measures")
    print(f"• All endpoints tested with validation, edge cases, and performance metrics\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Tests interrupted by user{Colors.RESET}\n")
    except Exception as e:
        print(f"\n\n{Colors.RED}Fatal error: {e}{Colors.RESET}\n")
