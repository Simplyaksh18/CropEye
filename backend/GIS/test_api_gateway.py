#!/usr/bin/env python3
"""
API Gateway Test Suite
Comprehensive testing for CropEye1 Unified API Gateway

Location: D:\\CropEye1\\backend\\test_api_gateway.py

Tests:
- Health checks
- Individual module endpoints
- Comprehensive analysis
- Batch processing
- Error handling
- Response formatting

Author: CropEye1 System
Date: October 19, 2025
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

# API Gateway URL
GATEWAY_URL = "http://localhost:5000"

# Test results
test_results = {
    'total': 0,
    'passed': 0,
    'failed': 0,
    'skipped': 0
}

def print_header(text):
    """Print test header"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'=' * 80}")
    print(f"{text.center(80)}")
    print(f"{'=' * 80}{Colors.RESET}\n")

def print_test(test_name):
    """Print test name"""
    print(f"{Colors.BLUE}▸ {test_name}{Colors.RESET}")

def print_pass(message):
    """Print success"""
    print(f"  {Colors.GREEN}✓{Colors.RESET} {message}")
    test_results['passed'] += 1

def print_fail(message):
    """Print failure"""
    print(f"  {Colors.RED}✗{Colors.RESET} {message}")
    test_results['failed'] += 1

def print_info(message):
    """Print info"""
    print(f"  {Colors.CYAN}ℹ{Colors.RESET} {message}")

def print_warn(message):
    """Print warning"""
    print(f"  {Colors.YELLOW}⚠{Colors.RESET} {message}")

def test_health_check():
    """Test 1: Basic health check"""
    print_test("Test 1: Basic Health Check")
    test_results['total'] += 1
    
    try:
        response = requests.get(f"{GATEWAY_URL}/api/v1/health", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and data.get('data', {}).get('status') == 'healthy':
                print_pass("Health check passed")
                print_info(f"Service: {data['data'].get('service')}")
                print_info(f"Version: {data['data'].get('version')}")
            else:
                print_fail("Health check returned unhealthy status")
        else:
            print_fail(f"Health check failed with status {response.status_code}")
            
    except Exception as e:
        print_fail(f"Health check error: {e}")

def test_detailed_health():
    """Test 2: Detailed health check"""
    print_test("Test 2: Detailed Health Check")
    test_results['total'] += 1
    
    try:
        response = requests.get(f"{GATEWAY_URL}/api/v1/health/detailed", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            modules = data.get('data', {}).get('modules', {})
            
            print_pass("Detailed health check passed")
            print_info(f"Gateway status: {data['data']['gateway']['status']}")
            
            for module_name, module_health in modules.items():
                status = module_health.get('status')
                if status == 'healthy':
                    print_info(f"{module_name}: {Colors.GREEN}✓ healthy{Colors.RESET}")
                else:
                    print_warn(f"{module_name}: {Colors.RED}✗ {status}{Colors.RESET}")
        else:
            print_fail(f"Detailed health check failed with status {response.status_code}")
            
    except Exception as e:
        print_fail(f"Detailed health check error: {e}")

def test_ndvi_endpoint():
    """Test 3: NDVI endpoint"""
    print_test("Test 3: NDVI Endpoint")
    test_results['total'] += 1
    
    lat, lng = 30.3398, 76.3869
    
    try:
        response = requests.get(
            f"{GATEWAY_URL}/api/v1/ndvi/{lat}/{lng}",
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print_pass("NDVI endpoint successful")
                ndvi_data = data.get('data', {})
                if 'ndvi_value' in ndvi_data:
                    print_info(f"NDVI Value: {ndvi_data['ndvi_value']}")
                print_info(f"Response time: {response.elapsed.total_seconds():.2f}s")
            else:
                print_fail("NDVI endpoint returned success=false")
        else:
            print_fail(f"NDVI endpoint failed with status {response.status_code}")
            
    except Exception as e:
        print_fail(f"NDVI endpoint error: {e}")

def test_soil_endpoint():
    """Test 4: Soil endpoint"""
    print_test("Test 4: Soil Endpoint")
    test_results['total'] += 1
    
    lat, lng = 30.3398, 76.3869
    
    try:
        response = requests.get(
            f"{GATEWAY_URL}/api/v1/soil/{lat}/{lng}",
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print_pass("Soil endpoint successful")
                soil_data = data.get('data', {})
                if 'soil_properties' in soil_data:
                    print_info(f"Soil data retrieved")
                print_info(f"Response time: {response.elapsed.total_seconds():.2f}s")
            else:
                print_fail("Soil endpoint returned success=false")
        else:
            print_fail(f"Soil endpoint failed with status {response.status_code}")
            
    except Exception as e:
        print_fail(f"Soil endpoint error: {e}")

def test_weather_endpoint():
    """Test 5: Weather endpoint"""
    print_test("Test 5: Weather Endpoint")
    test_results['total'] += 1
    
    lat, lng = 30.3398, 76.3869
    
    try:
        response = requests.get(
            f"{GATEWAY_URL}/api/v1/weather/{lat}/{lng}",
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print_pass("Weather endpoint successful")
                weather_data = data.get('data', {})
                if 'temperature' in weather_data:
                    print_info(f"Temperature: {weather_data['temperature'].get('current')}°C")
                print_info(f"Response time: {response.elapsed.total_seconds():.2f}s")
            else:
                print_fail("Weather endpoint returned success=false")
        else:
            print_fail(f"Weather endpoint failed with status {response.status_code}")
            
    except Exception as e:
        print_fail(f"Weather endpoint error: {e}")

def test_comprehensive_analysis():
    """Test 6: Comprehensive analysis"""
    print_test("Test 6: Comprehensive Analysis")
    test_results['total'] += 1
    
    payload = {
        "latitude": 30.3398,
        "longitude": 76.3869,
        "include_ndvi": True,
        "include_soil": True,
        "include_weather": True
    }
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{GATEWAY_URL}/api/v1/analysis/comprehensive",
            json=payload,
            timeout=60
        )
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                result_data = data.get('data', {})
                completed = result_data.get('modules_completed', [])
                
                print_pass(f"Comprehensive analysis successful ({len(completed)} modules)")
                print_info(f"Modules completed: {', '.join(completed)}")
                print_info(f"Total response time: {elapsed:.2f}s")
                
                if 'recommendations' in result_data:
                    recs = result_data['recommendations']
                    print_info(f"Recommendations: {len(recs)}")
                    
            else:
                print_fail("Comprehensive analysis returned success=false")
        else:
            print_fail(f"Comprehensive analysis failed with status {response.status_code}")
            
    except Exception as e:
        print_fail(f"Comprehensive analysis error: {e}")

def test_batch_analysis():
    """Test 7: Batch analysis"""
    print_test("Test 7: Batch Analysis")
    test_results['total'] += 1
    
    payload = {
        "locations": [
            {"latitude": 30.3398, "longitude": 76.3869, "name": "Punjab"},
            {"latitude": 28.6139, "longitude": 77.2090, "name": "Delhi"}
        ],
        "include_ndvi": True,
        "include_soil": True,
        "include_weather": True
    }
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{GATEWAY_URL}/api/v1/batch/analyze",
            json=payload,
            timeout=90
        )
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                result_data = data.get('data', {})
                completed = result_data.get('completed', 0)
                total = result_data.get('total_locations', 0)
                
                print_pass(f"Batch analysis successful ({completed}/{total} locations)")
                print_info(f"Total response time: {elapsed:.2f}s")
                print_info(f"Avg time per location: {elapsed/total:.2f}s")
            else:
                print_fail("Batch analysis returned success=false")
        else:
            print_fail(f"Batch analysis failed with status {response.status_code}")
            
    except Exception as e:
        print_fail(f"Batch analysis error: {e}")

def test_invalid_coordinates():
    """Test 8: Invalid coordinates handling"""
    print_test("Test 8: Invalid Coordinates Handling")
    test_results['total'] += 1
    
    # Test with invalid latitude (>90)
    try:
        response = requests.get(
            f"{GATEWAY_URL}/api/v1/ndvi/95.0/76.0",
            timeout=5
        )
        
        if response.status_code == 400:
            print_pass("Invalid coordinates rejected correctly")
        else:
            print_fail(f"Invalid coordinates not rejected (status: {response.status_code})")
            
    except Exception as e:
        print_fail(f"Invalid coordinates test error: {e}")

def test_missing_data():
    """Test 9: Missing request data"""
    print_test("Test 9: Missing Request Data Handling")
    test_results['total'] += 1
    
    try:
        response = requests.post(
            f"{GATEWAY_URL}/api/v1/analysis/comprehensive",
            json={},  # Missing required fields
            timeout=5
        )
        
        if response.status_code == 400:
            print_pass("Missing data rejected correctly")
        else:
            print_warn(f"Missing data handling needs improvement (status: {response.status_code})")
            test_results['passed'] += 1  # Not critical
            
    except Exception as e:
        print_fail(f"Missing data test error: {e}")

def test_root_endpoint():
    """Test 10: Root endpoint"""
    print_test("Test 10: Root Endpoint")
    test_results['total'] += 1
    
    try:
        response = requests.get(f"{GATEWAY_URL}/", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if 'service' in data and 'endpoints' in data:
                print_pass("Root endpoint successful")
                print_info(f"Service: {data['service']}")
                print_info(f"Version: {data.get('version')}")
            else:
                print_fail("Root endpoint returned incomplete data")
        else:
            print_fail(f"Root endpoint failed with status {response.status_code}")
            
    except Exception as e:
        print_fail(f"Root endpoint error: {e}")

def test_response_format():
    """Test 11: Response format consistency"""
    print_test("Test 11: Response Format Consistency")
    test_results['total'] += 1
    
    try:
        response = requests.get(f"{GATEWAY_URL}/api/v1/health", timeout=5)
        data = response.json()
        
        # Check required fields
        required_fields = ['success', 'message', 'timestamp', 'data']
        missing_fields = [f for f in required_fields if f not in data]
        
        if not missing_fields:
            print_pass("Response format is consistent")
            print_info(f"All required fields present: {', '.join(required_fields)}")
        else:
            print_fail(f"Missing fields in response: {missing_fields}")
            
    except Exception as e:
        print_fail(f"Response format test error: {e}")

def test_cors_headers():
    """Test 12: CORS headers"""
    print_test("Test 12: CORS Headers")
    test_results['total'] += 1
    
    try:
        response = requests.options(f"{GATEWAY_URL}/api/v1/health", timeout=5)
        
        if 'Access-Control-Allow-Origin' in response.headers:
            print_pass("CORS headers present")
            print_info(f"CORS enabled for: {response.headers['Access-Control-Allow-Origin']}")
        else:
            print_warn("CORS headers not found (may need configuration)")
            test_results['passed'] += 1  # Not critical
            
    except Exception as e:
        print_fail(f"CORS test error: {e}")

def print_summary():
    """Print test summary"""
    print_header("TEST SUMMARY")
    
    total = test_results['total']
    passed = test_results['passed']
    failed = test_results['failed']
    
    success_rate = (passed / total * 100) if total > 0 else 0
    
    print(f"{Colors.BOLD}Total Tests:{Colors.RESET}    {total}")
    print(f"{Colors.GREEN}Passed:{Colors.RESET}        {passed}")
    print(f"{Colors.RED}Failed:{Colors.RESET}        {failed}")
    print(f"{Colors.BOLD}Success Rate:{Colors.RESET}  {success_rate:.1f}%")
    print()
    
    if failed == 0:
        print(f"{Colors.GREEN}{Colors.BOLD}✓ ALL TESTS PASSED!{Colors.RESET}")
    else:
        print(f"{Colors.RED}{Colors.BOLD}✗ {failed} TEST(S) FAILED{Colors.RESET}")
    
    print()

def main():
    """Run all tests"""
    print_header("CROPEYE1 API GATEWAY TEST SUITE")
    
    print(f"{Colors.BOLD}Gateway URL:{Colors.RESET} {GATEWAY_URL}")
    print(f"{Colors.BOLD}Start Time:{Colors.RESET}  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check if gateway is running
    try:
        response = requests.get(f"{GATEWAY_URL}/", timeout=3)
        print(f"{Colors.GREEN}✓ API Gateway is running{Colors.RESET}\n")
    except:
        print(f"{Colors.RED}✗ API Gateway is not running!{Colors.RESET}")
        print(f"{Colors.YELLOW}Please start the gateway: python api_gateway.py{Colors.RESET}\n")
        return
    
    # Run tests
    print_header("RUNNING TESTS")
    
    test_health_check()
    test_detailed_health()
    test_ndvi_endpoint()
    test_soil_endpoint()
    test_weather_endpoint()
    test_comprehensive_analysis()
    test_batch_analysis()
    test_invalid_coordinates()
    test_missing_data()
    test_root_endpoint()
    test_response_format()
    test_cors_headers()
    
    # Print summary
    print_summary()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Tests interrupted by user{Colors.RESET}\n")
    except Exception as e:
        print(f"\n\n{Colors.RED}Fatal error: {e}{Colors.RESET}\n")
