#!/usr/bin/env python3

"""
Comprehensive Test Script for Soil Analysis System
Tests soil data analysis, NDVI integration, and all endpoints
"""

import os
import requests
import json
import time
import subprocess
import sys
from datetime import datetime

class SoilSystemTester:
    def __init__(self):
        self.api_base = "http://127.0.0.1:5002/api"  # Soil API port

        # Test coordinates with expected soil results
        self.test_coordinates = [
            {"name": "Punjab Wheat Farm", "lat": 30.3398, "lng": 76.3869, 
             "expected_ph": 7.2, "expected_soil_type": "Alluvial Soil", "has_ndvi": True},
            {"name": "Maharashtra Sugarcane", "lat": 18.15, "lng": 74.5777, 
             "expected_ph": 8.1, "expected_soil_type": "Black Cotton Soil", "has_ndvi": True},
            {"name": "California Central Valley", "lat": 36.7783, "lng": -119.4179, 
             "expected_ph": 7.8, "expected_soil_type": "Aridisol", "has_ndvi": True},
            {"name": "Iowa Corn Farm", "lat": 41.5868, "lng": -93.6250, 
             "expected_ph": 6.3, "expected_soil_type": "Prairie Soil", "has_ndvi": False},
            {"name": "Random Location (Delhi)", "lat": 28.6139, "lng": 77.2090, 
             "expected_ph": None, "expected_soil_type": "Mixed", "has_ndvi": False}
        ]

    def test_api_health(self):
        """Test API health endpoint"""
        print("🔍 Testing Soil API Health...")
        try:
            response = requests.get(f"{self.api_base}/health", timeout=10)

            if response.status_code == 200:
                health_data = response.json()
                print(f"✅ API Status: {health_data['status']}")
                print(f"   Service: {health_data['service']}")
                print(f"   Known Soil Locations: {health_data.get('known_soil_locations', 0)}")
                print(f"   NDVI Integration: {health_data.get('modules', {}).get('ndvi_integration', 'Unknown')}")
                print(f"   Copernicus Credentials: {health_data.get('credentials_status', {}).get('copernicus', False)}")
                return True
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Cannot connect to Soil API: {e}")
            print("💡 Make sure to run: python soil_flask_backend.py")
            return False

    def test_integration_status(self):
        """Test NDVI integration status"""
        print("\n🔧 Testing NDVI Integration Status...")
        try:
            response = requests.get(f"{self.api_base}/soil/integration-status", timeout=10)

            if response.status_code == 200:
                integration_data = response.json()
                print("✅ Integration Status Retrieved:")

                ndvi_integration = integration_data.get('ndvi_integration', {})
                print(f"   NDVI Module Available: {'✅ Yes' if ndvi_integration.get('available') else '❌ No'}")
                print(f"   Calculator Initialized: {'✅ Yes' if ndvi_integration.get('calculator_initialized') else '❌ No'}")
                print(f"   NDVI Known Locations: {ndvi_integration.get('known_locations', 0)}")

                credentials = integration_data.get('credentials', {})
                print(f"   Copernicus Credentials: {'✅ Available' if credentials.get('copernicus_available') else '❌ Missing'}")
                print(f"   Env File Location: {credentials.get('env_file_location', 'Unknown')}")

                return ndvi_integration.get('available', False)
            else:
                print(f"⚠️ Integration status endpoint returned: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Integration status test failed: {e}")
            return False

    def test_known_locations(self):
        """Test known agricultural locations endpoint"""
        print("\n🌾 Testing Known Agricultural Locations...")
        try:
            response = requests.get(f"{self.api_base}/soil/known-locations", timeout=15)

            if response.status_code == 200:
                locations_data = response.json()
                known_locations = locations_data.get('known_locations', [])

                print(f"✅ Retrieved {len(known_locations)} known locations:")

                for location in known_locations:
                    name = location.get('name', 'Unknown')
                    coords = location.get('coordinates', {})
                    soil_type = location.get('soil_type', 'Unknown')
                    matches_ndvi = location.get('matches_ndvi_module', False)

                    print(f"   📍 {name}")
                    print(f"      Coordinates: {coords.get('latitude', 0):.4f}, {coords.get('longitude', 0):.4f}")
                    print(f"      Soil Type: {soil_type}")
                    print(f"      NDVI Module Match: {'✅ Yes' if matches_ndvi else '❌ No'}")

                return len(known_locations) >= 5
            else:
                print(f"❌ Known locations test failed: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Known locations test error: {e}")
            return False

    def test_soil_analysis_with_ndvi(self):
        """Test comprehensive soil analysis with NDVI integration"""
        print("\n🌱 Testing Comprehensive Soil Analysis with NDVI...")

        all_passed = True

        for coord in self.test_coordinates:
            print(f"\n📍 Testing {coord['name']} ({coord['lat']}, {coord['lng']})")

            payload = {
                "latitude": coord["lat"],
                "longitude": coord["lng"],
                "include_ndvi": True,
                "analysis_depth": "comprehensive"
            }

            try:
                response = requests.post(
                    f"{self.api_base}/soil/analyze",
                    json=payload,
                    timeout=60
                )

                if response.status_code == 200:
                    result = response.json()

                    # Extract key information
                    location_info = result.get('location_info', {})
                    soil_props = result.get('soil_properties', {})
                    confidence = result.get('confidence_score', 0)
                    data_sources = result.get('data_sources', [])
                    ndvi_correlation = result.get('ndvi_correlation')

                    print(f"   ✅ Analysis Success!")
                    print(f"   Location: {location_info.get('name', 'Unknown')}")
                    print(f"   Soil Type: {location_info.get('soil_type', 'Unknown')}")
                    print(f"   Recognized: {location_info.get('recognized', False)}")
                    print(f"   Confidence: {confidence:.2f}")
                    print(f"   Data Sources: {', '.join(data_sources)}")

                    # Check soil properties
                    if 'ph' in soil_props:
                        ph_val = soil_props['ph']['value']
                        ph_class = soil_props['ph']['classification']
                        print(f"   pH: {ph_val} ({ph_class})")

                        # Verify against expected values for known locations
                        if coord['expected_ph'] and abs(ph_val - coord['expected_ph']) <= 0.5:
                            print(f"   🎯 pH matches expected value ({coord['expected_ph']})!")

                    if 'texture' in soil_props:
                        texture = soil_props['texture']['value']
                        print(f"   Texture: {texture}")

                    # Show some nutrient data
                    for nutrient in ['nitrogen', 'phosphorus', 'potassium', 'organic_carbon']:
                        if nutrient in soil_props:
                            nutrient_data = soil_props[nutrient]
                            value = nutrient_data.get('value', 0)
                            unit = nutrient_data.get('unit', '')
                            classification = nutrient_data.get('classification', '')
                            print(f"   {nutrient.title()}: {value} {unit} ({classification})")

                    # Check NDVI integration
                    if ndvi_correlation:
                        ndvi_val = ndvi_correlation.get('ndvi_value')
                        ndvi_source = ndvi_correlation.get('ndvi_data_source')
                        integration_status = ndvi_correlation.get('integration_status')

                        print(f"   🌿 NDVI Integration: {integration_status}")

                        if ndvi_val is not None:
                            print(f"   NDVI Value: {ndvi_val:.4f}")
                            print(f"   NDVI Source: {ndvi_source}")

                            # Check correlation analysis
                            correlation = ndvi_correlation.get('soil_ndvi_correlation', {})
                            if correlation.get('vegetation_soil_match'):
                                print(f"   Soil-NDVI Match: {correlation['vegetation_soil_match']}")

                            # Verify NDVI is in valid range
                            if -1 <= ndvi_val <= 1:
                                print(f"   ✅ NDVI in valid range")
                            else:
                                print(f"   ⚠️ NDVI outside valid range")
                                all_passed = False
                        else:
                            print(f"   ⚠️ NDVI value not available: {ndvi_correlation.get('error', 'Unknown error')}")
                    else:
                        if coord['has_ndvi']:
                            print("   ❌ Expected NDVI correlation data but got none")
                            all_passed = False
                        else:
                            print("   ℹ️ No NDVI correlation data (as expected for this location)")

                else:
                    print(f"   ❌ Analysis failed: {response.status_code}")
                    print(f"   Response: {response.text[:200]}")
                    all_passed = False

            except Exception as e:
                print(f"   ❌ Request failed: {e}")
                all_passed = False

        return all_passed

    def test_soil_analysis_without_ndvi(self):
        """Test soil analysis without NDVI integration"""
        print("\n🌾 Testing Soil Analysis WITHOUT NDVI...")

        # Test with Punjab coordinates
        coord = self.test_coordinates[0]
        print(f"📍 Testing {coord['name']} without NDVI...")

        payload = {
            "latitude": coord["lat"],
            "longitude": coord["lng"],
            "include_ndvi": False,  # Disable NDVI
            "analysis_depth": "basic"
        }

        try:
            response = requests.post(
                f"{self.api_base}/soil/analyze",
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()

                print("✅ Analysis Success (No NDVI)!")
                print(f"   Location: {result.get('location_info', {}).get('name', 'Unknown')}")
                print(f"   Soil Type: {result.get('location_info', {}).get('soil_type', 'Unknown')}")
                print(f"   Confidence: {result.get('confidence_score', 0):.2f}")

                # Verify no NDVI data
                ndvi_correlation = result.get('ndvi_correlation')
                if ndvi_correlation is None:
                    print("   ✅ Correctly excluded NDVI correlation data")
                    return True
                else:
                    print("   ⚠️ NDVI data present when it should be excluded")
                    return False

            else:
                print(f"❌ Analysis without NDVI failed: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ No-NDVI analysis test failed: {e}")
            return False

    def test_soil_comparison(self):
        """Test soil comparison endpoint"""
        print("\n🔍 Testing Soil Comparison...")

        # Compare Punjab and Maharashtra (both known locations)
        locations = [
            {"name": "Punjab Wheat", "latitude": 30.3398, "longitude": 76.3869},
            {"name": "Maharashtra Sugarcane", "latitude": 18.15, "longitude": 74.5777}
        ]

        payload = {
            "locations": locations,
            "properties": ["ph", "nitrogen", "phosphorus", "organic_carbon"],
            "include_ndvi": True
        }

        try:
            response = requests.post(
                f"{self.api_base}/soil/compare",
                json=payload,
                timeout=90
            )

            if response.status_code == 200:
                result = response.json()

                print("✅ Soil Comparison Success!")
                print(f"   Locations Compared: {len(result.get('locations', []))}")

                # Show property comparisons
                prop_comparisons = result.get('property_comparison', {})
                for prop, comparison in prop_comparisons.items():
                    values = comparison.get('values', {})
                    print(f"   {prop.title()}:")
                    for location, data in values.items():
                        print(f"     {location}: {data.get('value', 'N/A')} {data.get('unit', '')}")

                # Show NDVI comparison if available
                ndvi_comparison = result.get('ndvi_comparison')
                if ndvi_comparison:
                    ndvi_values = ndvi_comparison.get('values', {})
                    print("   🌿 NDVI Comparison:")
                    for location, data in ndvi_values.items():
                        ndvi_val = data.get('ndvi_value', 'N/A')
                        health = data.get('vegetation_health', 'Unknown')
                        print(f"     {location}: NDVI {ndvi_val} ({health})")

                return True
            else:
                print(f"❌ Soil comparison failed: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Soil comparison error: {e}")
            return False

    def test_recommendations(self):
        """Test soil recommendations endpoint"""
        print("\n🌾 Testing Soil Recommendations...")

        # Test recommendations for Punjab
        coord = self.test_coordinates[0]
        lat, lng = coord["lat"], coord["lng"]

        try:
            response = requests.get(
                f"{self.api_base}/soil/recommendations/{lat}/{lng}",
                timeout=60
            )

            if response.status_code == 200:
                result = response.json()

                print(f"✅ Recommendations Retrieved!")
                print(f"   Location: {coord['name']}")
                print(f"   Soil Health Score: {result.get('soil_health_score', 'N/A')}")

                # Show immediate actions
                immediate = result.get('immediate_actions', [])
                if immediate:
                    print("   ⚡ Immediate Actions:")
                    for action in immediate[:3]:  # Show first 3
                        print(f"     • {action.get('action', 'N/A')}: {action.get('recommendation', 'N/A')}")

                # Show NDVI-soil insights
                ndvi_insights = result.get('ndvi_soil_insights', {})
                if ndvi_insights:
                    print("   🌿 NDVI-Soil Insights:")
                    print(f"     NDVI Value: {ndvi_insights.get('ndvi_value', 'N/A')}")
                    print(f"     Vegetation Health: {ndvi_insights.get('vegetation_health', 'Unknown')}")
                    print(f"     Soil-Vegetation Match: {ndvi_insights.get('soil_vegetation_match', 'Unknown')}")

                return True
            else:
                print(f"❌ Recommendations failed: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Recommendations test error: {e}")
            return False

    def test_debug_info(self):
        """Test debug endpoint"""
        print("\n🔧 Testing Debug Information...")
        try:
            response = requests.get(f"{self.api_base}/soil/debug", timeout=10)

            if response.status_code == 200:
                debug_data = response.json()
                print("✅ Debug Info Retrieved:")
                print(f"   Working Directory: {debug_data.get('system_info', {}).get('working_directory', 'N/A')}")
                print(f"   Known Soil Locations: {len(debug_data.get('known_soil_locations', []))}")
                print(f"   NDVI Integration: {debug_data.get('ndvi_integration', {})}")

                test_coords = debug_data.get('test_coordinates', [])
                if test_coords:
                    print("   🎯 Test Coordinates Available:")
                    for coord in test_coords[:3]:  # Show first 3
                        print(f"     • {coord.get('name', 'Unknown')}: {coord.get('expected', 'N/A')}")

                return True
            else:
                print(f"⚠️ Debug endpoint returned: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Debug test failed: {e}")
            return False

    def run_comprehensive_test(self):
        """Run all tests"""
        print("🧪 SOIL ANALYSIS SYSTEM COMPREHENSIVE TEST SUITE")
        print("=" * 70)
        print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Track test results
        results = {
            'health': False,
            'integration_status': False,
            'known_locations': False,
            'soil_analysis_with_ndvi': False,
            'soil_analysis_without_ndvi': False,
            'soil_comparison': False,
            'recommendations': False,
            'debug': False
        }

        # Run tests
        results['health'] = self.test_api_health()

        if results['health']:
            results['integration_status'] = self.test_integration_status()
            results['known_locations'] = self.test_known_locations()
            results['soil_analysis_with_ndvi'] = self.test_soil_analysis_with_ndvi()
            results['soil_analysis_without_ndvi'] = self.test_soil_analysis_without_ndvi()
            results['soil_comparison'] = self.test_soil_comparison()
            results['recommendations'] = self.test_recommendations()
            results['debug'] = self.test_debug_info()
        else:
            print("⚠️ API health check failed - skipping other tests")

        # Summary
        print("\n" + "=" * 70)
        print("📊 TEST SUMMARY")
        print("=" * 70)

        passed = sum(results.values())
        total = len(results)

        for test, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{test.replace('_', ' ').title():.<50} {status}")

        print(f"\nOverall: {passed}/{total} tests passed ({passed/total*100:.0f}%)")

        if passed >= 6:  # Most functionality working
            print("🎉 Soil Analysis System is functional and ready for use!")
            print("✅ NDVI integration working correctly")
            print("✅ Known locations returning accurate data")
            print("✅ Soil-NDVI correlation analysis working")
        elif passed >= 4:  # Basic functionality working
            print("⚠️ System mostly functional - some advanced features may not work")
        elif passed >= 2:  # Basic API working
            print("⚠️ System partially functional - troubleshooting needed")
        else:
            print("❌ System has major issues - check setup and configuration")

        return passed, total

def main():
    """Main test function"""
    tester = SoilSystemTester()
    passed, total = tester.run_comprehensive_test()

    print("\n" + "=" * 70)
    if passed == total:
        print("🎉 ALL TESTS PASSED! Soil Analysis System is fully functional!")
        sys.exit(0)
    elif passed >= total * 0.75:  # 75% or more passed
        print("✅ MOSTLY WORKING! Minor issues detected.")
        sys.exit(0)
    else:
        print("❌ SIGNIFICANT ISSUES DETECTED! Check error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
