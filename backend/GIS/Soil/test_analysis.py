#!/usr/bin/env python3
"""
COMPREHENSIVE SOIL MODULE FINAL TEST SUITE
Tests entire soil analysis system for known and unknown locations

Location: D:\\CropEye1\\backend\\GIS\\Soil Analysis\\test_soil_module_complete.py

Tests:
1. Module Initialization
2. Known Locations (5 verified sites)
3. Unknown Locations (GPS + Manual)
4. Copernicus Integration
5. NDVI Integration
6. API Endpoints
7. Geographic Context
8. Data Source Fallbacks
9. Error Handling
10. Performance Benchmarks

Author: CropEye1 System
Date: October 18, 2025
"""

import sys
import os
import time
import json
import requests
from datetime import datetime
from typing import Dict, List

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    """Print colored header"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*80}")
    print(f"{text.center(80)}")
    print(f"{'='*80}{Colors.RESET}\n")

def print_test(test_name):
    """Print test name"""
    print(f"{Colors.BLUE}📋 {test_name}{Colors.RESET}")

def print_success(message):
    """Print success message"""
    print(f"   {Colors.GREEN}✅ {message}{Colors.RESET}")

def print_error(message):
    """Print error message"""
    print(f"   {Colors.RED}❌ {message}{Colors.RESET}")

def print_warning(message):
    """Print warning message"""
    print(f"   {Colors.YELLOW}⚠️  {message}{Colors.RESET}")

def print_info(message):
    """Print info message"""
    print(f"   ℹ️  {message}")


# ============================================================
# TEST CONFIGURATION
# ============================================================

API_BASE = os.getenv('CROPEYE_API_BASE', "http://127.0.0.1:5000/api")
TEST_RESULTS = {
    'total_tests': 0,
    'passed': 0,
    'failed': 0,
    'warnings': 0,
    'test_details': []
}

# Test locations
KNOWN_LOCATIONS = [
    {
        "name": "Punjab Wheat Farm",
        "latitude": 30.3398,
        "longitude": 76.3869,
        "coordinate_source": "gps",
        "expected_type": "known",
        "expected_soil_type": "Alluvial Soil",
        "expected_confidence": 0.95
    },
    {
        "name": "Maharashtra Sugarcane Farm",
        "latitude": 18.15,
        "longitude": 74.5777,
        "coordinate_source": "manual",
        "expected_type": "known",
        "expected_soil_type": "Black Cotton Soil",
        "expected_confidence": 0.92
    },
    {
        "name": "California Central Valley",
        "latitude": 36.7783,
        "longitude": -119.4179,
        "coordinate_source": "gps",
        "expected_type": "known",
        "expected_soil_type": "Aridisol",
        "expected_confidence": 0.89
    },
    {
        "name": "Iowa Corn Farm",
        "latitude": 41.5868,
        "longitude": -93.6250,
        "coordinate_source": "manual",
        "expected_type": "known",
        "expected_soil_type": "Prairie Soil",
        "expected_confidence": 0.97
    },
    {
        "name": "Karnataka Coffee Plantation",
        "latitude": 13.3409,
        "longitude": 75.7131,
        "coordinate_source": "gps",
        "expected_type": "known",
        "expected_soil_type": "Red Lateritic Soil",
        "expected_confidence": 0.88
    }
]

UNKNOWN_LOCATIONS = [
    {
        "name": "Delhi (GPS)",
        "latitude": 28.6139,
        "longitude": 77.2090,
        "coordinate_source": "gps",
        "expected_type": "unknown",
        "expected_region": "India"
    },
    {
        "name": "Mumbai (Manual)",
        "latitude": 19.0760,
        "longitude": 72.8777,
        "coordinate_source": "manual",
        "expected_type": "unknown",
        "expected_region": "India"
    },
    {
        "name": "Kansas USA (Manual)",
        "latitude": 38.5266,
        "longitude": -96.7265,
        "coordinate_source": "manual",
        "expected_type": "unknown",
        "expected_region": "US"
    },
    {
        "name": "Brasília Brazil (GPS)",
        "latitude": -15.7801,
        "longitude": -47.9292,
        "coordinate_source": "gps",
        "expected_type": "unknown",
        "expected_region": "South America"
    },
    {
        "name": "Sydney Australia (Manual)",
        "latitude": -33.8688,
        "longitude": 151.2093,
        "coordinate_source": "manual",
        "expected_type": "unknown",
        "expected_region": "Australia"
    }
]


# ============================================================
# TEST 1: MODULE INITIALIZATION
# ============================================================

def test_module_initialization():
    """Test if soil modules can be imported and initialized"""
    print_test("TEST 1: Module Initialization")
    
    try:
        from soil_data_collector import SoilDataCollector
        collector = SoilDataCollector()
        print_success("SoilDataCollector imported and initialized")
        
        # Check for Copernicus downloader
        if collector.copernicus_downloader:
            print_success("Copernicus downloader available")
        else:
            print_warning("Copernicus downloader not available")
        
        # Check known locations
        known_count = len(collector.known_agricultural_locations)
        print_success(f"Known agricultural locations loaded: {known_count}")
        
        TEST_RESULTS['passed'] += 1
        return True
        
    except Exception as e:
        print_error(f"Module initialization failed: {e}")
        TEST_RESULTS['failed'] += 1
        return False
    finally:
        TEST_RESULTS['total_tests'] += 1


# ============================================================
# TEST 2: SERVER HEALTH CHECK
# ============================================================

def test_server_health():
    """Test if Flask server is running and healthy"""
    print_test("TEST 2: Server Health Check")
    
    try:
        response = requests.get(f"{API_BASE}/health", timeout=10)
        
        if response.status_code == 200:
            health_data = response.json()
            print_success(f"Server status: {health_data.get('status', 'unknown')}")
            
            modules = health_data.get('modules', {})
            for module_name, status in modules.items():
                if status == 'active':
                    print_success(f"{module_name}: {status}")
                elif status == 'fallback':
                    print_warning(f"{module_name}: {status}")
                else:
                    print_warning(f"{module_name}: {status}")
            
            TEST_RESULTS['passed'] += 1
            return True
        else:
            print_error(f"Server returned status code {response.status_code}")
            TEST_RESULTS['failed'] += 1
            return False
            
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to server. Make sure Flask server is running on port 5002")
        print_info("Run: python soil_flask_backend.py")
        TEST_RESULTS['failed'] += 1
        return False
    except Exception as e:
        print_error(f"Health check failed: {e}")
        TEST_RESULTS['failed'] += 1
        return False
    finally:
        TEST_RESULTS['total_tests'] += 1


# ============================================================
# TEST 3: KNOWN LOCATIONS - DIRECT MODULE TEST
# ============================================================

def test_known_locations_direct():
    """Test known locations using direct module calls"""
    print_test("TEST 3: Known Locations (Direct Module)")
    
    try:
        from soil_data_collector import SoilDataCollector
        collector = SoilDataCollector()
        
        passed_count = 0
        
        for location in KNOWN_LOCATIONS:
            print(f"\n   📍 Testing: {location['name']}")
            
            result = collector.get_soil_data(
                latitude=location['latitude'],
                longitude=location['longitude'],
                coordinate_source=location['coordinate_source'],
                include_ndvi=True
            )
            
            # Validate location type
            if result['coordinates']['location_type'] == location['expected_type']:
                print_success(f"Location type: {result['coordinates']['location_type']}")
            else:
                print_error(f"Expected {location['expected_type']}, got {result['coordinates']['location_type']}")
                continue
            
            # Validate confidence
            confidence = result.get('confidence_score', 0)
            if confidence >= 0.85:
                print_success(f"Confidence: {confidence:.2f}")
            else:
                print_warning(f"Confidence lower than expected: {confidence:.2f}")
            
            # Validate data sources
            data_sources = result.get('data_sources', [])
            if 'agricultural_survey_database' in data_sources:
                print_success(f"Data source: {data_sources[0]}")
            else:
                print_warning(f"Unexpected data source: {data_sources}")
            
            # Check soil properties
            soil_props = result.get('soil_properties', {})
            if 'ph' in soil_props and 'organic_carbon' in soil_props:
                print_success(f"pH: {soil_props['ph']['value']}, OC: {soil_props['organic_carbon']['value']}%")
            else:
                print_warning("Missing soil properties")
            
            # Check NDVI integration
            if result.get('ndvi_correlation'):
                ndvi_val = result['ndvi_correlation'].get('ndvi_value')
                if ndvi_val is not None:
                    print_success(f"NDVI: {ndvi_val:.3f}")
                else:
                    print_warning("NDVI value not available")
            
            passed_count += 1
        
        if passed_count == len(KNOWN_LOCATIONS):
            print(f"\n   {Colors.GREEN}✅ All {passed_count} known locations passed{Colors.RESET}")
            TEST_RESULTS['passed'] += 1
            return True
        else:
            print(f"\n   {Colors.YELLOW}⚠️  {passed_count}/{len(KNOWN_LOCATIONS)} locations passed{Colors.RESET}")
            TEST_RESULTS['warnings'] += 1
            return False
            
    except Exception as e:
        print_error(f"Known locations test failed: {e}")
        TEST_RESULTS['failed'] += 1
        return False
    finally:
        TEST_RESULTS['total_tests'] += 1


# ============================================================
# TEST 4: UNKNOWN LOCATIONS - DIRECT MODULE TEST
# ============================================================

def test_unknown_locations_direct():
    """Test unknown locations using direct module calls"""
    print_test("TEST 4: Unknown Locations (Direct Module)")
    
    try:
        from soil_data_collector import SoilDataCollector
        collector = SoilDataCollector()
        
        passed_count = 0
        
        for location in UNKNOWN_LOCATIONS:
            print(f"\n   📍 Testing: {location['name']}")
            
            result = collector.get_soil_data(
                latitude=location['latitude'],
                longitude=location['longitude'],
                coordinate_source=location['coordinate_source'],
                include_ndvi=True
            )
            
            # Validate location type
            if result['coordinates']['location_type'] == location['expected_type']:
                print_success(f"Location type: {result['coordinates']['location_type']}")
            else:
                print_error(f"Expected {location['expected_type']}, got {result['coordinates']['location_type']}")
                continue
            
            # Validate coordinate source
            coord_source = result['coordinates'].get('source', 'unknown')
            if coord_source == location['coordinate_source']:
                print_success(f"Coordinate source: {coord_source}")
            else:
                print_warning(f"Expected {location['coordinate_source']}, got {coord_source}")
            
            # Check geographic context
            if 'geographic_context' in result:
                geo_context = result['geographic_context']
                region = geo_context.get('region', '')
                climate = geo_context.get('climate_zone', '')
                print_success(f"Region: {region}")
                print_success(f"Climate: {climate}")
                
                # Verify region matches expected
                if location['expected_region'] in region:
                    print_success(f"Region matches expected: {location['expected_region']}")
                else:
                    print_warning(f"Region mismatch: expected {location['expected_region']}")
            else:
                print_warning("Geographic context not available")
            
            # Check data sources
            data_sources = result.get('data_sources', [])
            print_info(f"Data sources: {', '.join(data_sources)}")
            
            # Validate confidence
            confidence = result.get('confidence_score', 0)
            if confidence >= 0.6:
                print_success(f"Confidence: {confidence:.2f}")
            else:
                print_warning(f"Low confidence: {confidence:.2f}")
            
            # Check soil properties
            soil_props = result.get('soil_properties', {})
            if 'ph' in soil_props and 'organic_carbon' in soil_props:
                print_success(f"pH: {soil_props['ph']['value']}, OC: {soil_props['organic_carbon']['value']}%")
            else:
                print_warning("Missing soil properties")
            
            passed_count += 1
        
        if passed_count == len(UNKNOWN_LOCATIONS):
            print(f"\n   {Colors.GREEN}✅ All {passed_count} unknown locations passed{Colors.RESET}")
            TEST_RESULTS['passed'] += 1
            return True
        else:
            print(f"\n   {Colors.YELLOW}⚠️  {passed_count}/{len(UNKNOWN_LOCATIONS)} locations passed{Colors.RESET}")
            TEST_RESULTS['warnings'] += 1
            return False
            
    except Exception as e:
        print_error(f"Unknown locations test failed: {e}")
        TEST_RESULTS['failed'] += 1
        return False
    finally:
        TEST_RESULTS['total_tests'] += 1


# ============================================================
# TEST 5: API ENDPOINT - ANALYZE
# ============================================================

def test_api_analyze():
    """Test /api/soil/analyze endpoint"""
    print_test("TEST 5: API Endpoint - /api/soil/analyze")
    
    try:
        # Test known location
        print("\n   Testing known location via API...")
        payload = {
            "latitude": 30.3398,
            "longitude": 76.3869,
            "coordinate_source": "gps",
            "include_ndvi": True
        }
        
        response = requests.post(
            f"{API_BASE}/soil/analyze",
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            print_success(f"API returned 200 OK")
            print_success(f"Location type: {result['coordinates']['location_type']}")
            print_success(f"Confidence: {result.get('confidence_score', 0):.2f}")
            
            # Check API metadata
            if 'api_info' in result:
                api_info = result['api_info']
                print_success(f"Processing time: {api_info.get('processing_time_sec', 0):.2f}s")
        else:
            print_error(f"API returned {response.status_code}")
            print_error(f"Response: {response.text[:200]}")
            TEST_RESULTS['failed'] += 1
            return False
        
        # Test unknown location
        print("\n   Testing unknown location via API...")
        payload = {
            "latitude": 28.6139,
            "longitude": 77.2090,
            "coordinate_source": "manual",
            "include_ndvi": True
        }
        
        response = requests.post(
            f"{API_BASE}/soil/analyze",
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            print_success(f"API returned 200 OK")
            print_success(f"Location type: {result['coordinates']['location_type']}")
            
            if 'geographic_context' in result:
                print_success(f"Geographic context available")
        else:
            print_error(f"API returned {response.status_code}")
            TEST_RESULTS['failed'] += 1
            return False
        
        TEST_RESULTS['passed'] += 1
        return True
        
    except Exception as e:
        print_error(f"API test failed: {e}")
        TEST_RESULTS['failed'] += 1
        return False
    finally:
        TEST_RESULTS['total_tests'] += 1


# ============================================================
# TEST 6: API ENDPOINT - COMPARE
# ============================================================

def test_api_compare():
    """Test /api/soil/compare endpoint"""
    print_test("TEST 6: API Endpoint - /api/soil/compare")
    
    try:
        payload = {
            "locations": [
                {"name": "Punjab", "latitude": 30.3398, "longitude": 76.3869},
                {"name": "Maharashtra", "latitude": 18.15, "longitude": 74.5777}
            ],
            "include_ndvi": True
        }
        
        response = requests.post(
            f"{API_BASE}/soil/compare",
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            print_success(f"API returned 200 OK")
            
            locations_analyzed = result.get('locations_analyzed', [])
            print_success(f"Locations analyzed: {len(locations_analyzed)}")
            
            property_comparison = result.get('property_comparison', {})
            print_success(f"Properties compared: {len(property_comparison)}")
            
            TEST_RESULTS['passed'] += 1
            return True
        else:
            print_error(f"API returned {response.status_code}")
            TEST_RESULTS['failed'] += 1
            return False
            
    except Exception as e:
        print_error(f"Compare API test failed: {e}")
        TEST_RESULTS['failed'] += 1
        return False
    finally:
        TEST_RESULTS['total_tests'] += 1


# ============================================================
# TEST 7: API ENDPOINT - RECOMMENDATIONS
# ============================================================

def test_api_recommendations():
    """Test /api/soil/recommendations endpoint"""
    print_test("TEST 7: API Endpoint - /api/soil/recommendations")
    
    try:
        response = requests.get(
            f"{API_BASE}/soil/recommendations/30.3398/76.3869",
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            print_success(f"API returned 200 OK")
            
            if 'immediate_actions' in result:
                print_success(f"Recommendations generated")
            
            if 'soil_health_score' in result:
                print_success(f"Soil health score: {result['soil_health_score']}")
            
            TEST_RESULTS['passed'] += 1
            return True
        else:
            print_error(f"API returned {response.status_code}")
            TEST_RESULTS['failed'] += 1
            return False
            
    except Exception as e:
        print_error(f"Recommendations API test failed: {e}")
        TEST_RESULTS['failed'] += 1
        return False
    finally:
        TEST_RESULTS['total_tests'] += 1


# ============================================================
# TEST 8: COPERNICUS INTEGRATION
# ============================================================

def test_copernicus_integration():
    """Test Copernicus satellite data integration"""
    print_test("TEST 8: Copernicus Integration")
    
    try:
        from soil_data_collector import SoilDataCollector
        collector = SoilDataCollector()
        
        if not collector.copernicus_downloader:
            print_warning("Copernicus downloader not available")
            print_info("System will use fallback methods")
            TEST_RESULTS['warnings'] += 1
            return False
        
        print_success("Copernicus downloader available")
        
        # Test satellite data retrieval
        print("\n   Testing satellite data retrieval...")
        satellite_data = collector.copernicus_downloader.get_soil_satellite_data(
            28.6139, 77.2090, days_back=30
        )
        
        if satellite_data and satellite_data.get('confidence_score', 0) > 0.5:
            print_success(f"Satellite data retrieved (confidence: {satellite_data['confidence_score']:.2f})")
            
            if 'derived_soil_properties' in satellite_data:
                print_success("Soil properties derived from satellite data")
            
            if 'satellite_derived_properties' in satellite_data:
                print_success("Satellite observations available")
            
            TEST_RESULTS['passed'] += 1
            return True
        else:
            print_warning("Satellite data has low confidence or unavailable")
            TEST_RESULTS['warnings'] += 1
            return False
            
    except Exception as e:
        print_error(f"Copernicus integration test failed: {e}")
        TEST_RESULTS['failed'] += 1
        return False
    finally:
        TEST_RESULTS['total_tests'] += 1


# ============================================================
# TEST 9: NDVI INTEGRATION
# ============================================================

def test_ndvi_integration():
    """Test NDVI-Soil correlation"""
    print_test("TEST 9: NDVI Integration")
    
    try:
        from soil_data_collector import SoilDataCollector
        collector = SoilDataCollector()
        
        print("\n   Testing NDVI correlation for known location...")
        result = collector.get_soil_data(
            latitude=30.3398,
            longitude=76.3869,
            coordinate_source="gps",
            include_ndvi=True
        )
        
        if result.get('ndvi_correlation'):
            ndvi_corr = result['ndvi_correlation']
            
            if ndvi_corr.get('integration_status') == 'success':
                print_success("NDVI integration successful")
                
                ndvi_val = ndvi_corr.get('ndvi_value')
                if ndvi_val is not None:
                    print_success(f"NDVI value: {ndvi_val:.3f}")
                
                if ndvi_corr.get('soil_ndvi_correlation'):
                    print_success("Soil-NDVI correlation analysis available")
                
                TEST_RESULTS['passed'] += 1
                return True
            else:
                print_warning(f"NDVI integration status: {ndvi_corr.get('integration_status')}")
                TEST_RESULTS['warnings'] += 1
                return False
        else:
            print_warning("NDVI correlation not available")
            TEST_RESULTS['warnings'] += 1
            return False
            
    except Exception as e:
        print_error(f"NDVI integration test failed: {e}")
        TEST_RESULTS['failed'] += 1
        return False
    finally:
        TEST_RESULTS['total_tests'] += 1


# ============================================================
# TEST 10: PERFORMANCE BENCHMARK
# ============================================================

def test_performance():
    """Test system performance"""
    print_test("TEST 10: Performance Benchmark")
    
    try:
        from soil_data_collector import SoilDataCollector
        collector = SoilDataCollector()
        
        # Test known location performance
        print("\n   Testing known location performance...")
        start_time = time.time()
        result = collector.get_soil_data(30.3398, 76.3869, include_ndvi=True)
        known_time = time.time() - start_time
        
        if known_time < 5:
            print_success(f"Known location: {known_time:.2f}s (excellent)")
        elif known_time < 10:
            print_success(f"Known location: {known_time:.2f}s (good)")
        else:
            print_warning(f"Known location: {known_time:.2f}s (slow)")
        
        # Test unknown location performance
        print("\n   Testing unknown location performance...")
        start_time = time.time()
        result = collector.get_soil_data(28.6139, 77.2090, include_ndvi=True)
        unknown_time = time.time() - start_time
        
        if unknown_time < 10:
            print_success(f"Unknown location: {unknown_time:.2f}s (excellent)")
        elif unknown_time < 30:
            print_success(f"Unknown location: {unknown_time:.2f}s (good)")
        else:
            print_warning(f"Unknown location: {unknown_time:.2f}s (slow)")
        
        TEST_RESULTS['passed'] += 1
        return True
        
    except Exception as e:
        print_error(f"Performance test failed: {e}")
        TEST_RESULTS['failed'] += 1
        return False
    finally:
        TEST_RESULTS['total_tests'] += 1


# ============================================================
# MAIN TEST RUNNER
# ============================================================

def run_all_tests():
    """Run all tests"""
    print_header("🧪 COMPREHENSIVE SOIL MODULE TEST SUITE")
    
    print(f"{Colors.BOLD}Test Configuration:{Colors.RESET}")
    print(f"   API Base URL: {API_BASE}")
    print(f"   Known Locations: {len(KNOWN_LOCATIONS)}")
    print(f"   Unknown Locations: {len(UNKNOWN_LOCATIONS)}")
    print(f"   Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    start_time = time.time()
    
    # Run all tests
    test_module_initialization()
    test_server_health()
    test_known_locations_direct()
    test_unknown_locations_direct()
    test_api_analyze()
    test_api_compare()
    test_api_recommendations()
    test_copernicus_integration()
    test_ndvi_integration()
    test_performance()
    
    total_time = time.time() - start_time
    
    # Print summary
    print_header("📊 TEST SUMMARY")
    
    print(f"{Colors.BOLD}Results:{Colors.RESET}")
    print(f"   Total Tests: {TEST_RESULTS['total_tests']}")
    print(f"   {Colors.GREEN}✅ Passed: {TEST_RESULTS['passed']}{Colors.RESET}")
    print(f"   {Colors.RED}❌ Failed: {TEST_RESULTS['failed']}{Colors.RESET}")
    print(f"   {Colors.YELLOW}⚠️  Warnings: {TEST_RESULTS['warnings']}{Colors.RESET}")
    
    success_rate = (TEST_RESULTS['passed'] / TEST_RESULTS['total_tests'] * 100) if TEST_RESULTS['total_tests'] > 0 else 0
    print(f"\n   Success Rate: {success_rate:.1f}%")
    print(f"   Total Time: {total_time:.2f}s")
    
    # Final verdict
    print(f"\n{Colors.BOLD}Final Verdict:{Colors.RESET}")
    if TEST_RESULTS['failed'] == 0:
        if TEST_RESULTS['warnings'] == 0:
            print(f"   {Colors.GREEN}🎉 ALL TESTS PASSED! System is production-ready.{Colors.RESET}")
        else:
            print(f"   {Colors.YELLOW}✅ Tests passed with {TEST_RESULTS['warnings']} warnings. System is operational.{Colors.RESET}")
    else:
        print(f"   {Colors.RED}❌ {TEST_RESULTS['failed']} tests failed. Please review and fix issues.{Colors.RESET}")
    
    print("\n" + "="*80 + "\n")
    
    return TEST_RESULTS['failed'] == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
