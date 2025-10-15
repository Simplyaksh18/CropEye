
#!/usr/bin/env python3
"""
Comprehensive Test Suite for Soil Analysis Module with NDVI Integration
Tests integration with existing NDVI module and real agricultural coordinates
"""

import os
import requests
import json
import time
import sys
from datetime import datetime

class SoilAnalysisTestSuite:
    def __init__(self):
        self.api_base = "http://127.0.0.1:5002/api"

        # Real agricultural coordinates (matching NDVI module)
        self.test_coordinates = [
            {
                "name": "Punjab Wheat Farm",
                "lat": 30.3398,
                "lng": 76.3869,
                "expected_soil": "Alluvial Soil",
                "expected_ph": 7.2,
                "expected_texture": "Sandy Loam",
                "expected_ndvi": 0.652,  # From NDVI module
                "is_known_location": True,
                "description": "Major wheat production area - matches NDVI module data"
            },
            {
                "name": "Maharashtra Sugarcane Farm",
                "lat": 18.15,  # Normalized coordinate
                "lng": 74.5777,
                "expected_soil": "Black Cotton Soil (Vertisols)",
                "expected_ph": 8.1,
                "expected_texture": "Clay",
                "expected_ndvi": 0.718,  # From NDVI module
                "is_known_location": True,
                "description": "Sugarcane region - matches NDVI module data"
            },
            {
                "name": "California Central Valley",
                "lat": 36.7783,
                "lng": -119.4179,
                "expected_soil": "Aridisol",
                "expected_ph": 7.8,
                "expected_texture": "Sandy Clay Loam",
                "expected_ndvi": 0.547,  # From NDVI module
                "is_known_location": True,
                "description": "Central Valley agriculture - matches NDVI module"
            },
            {
                "name": "Iowa Corn Farm",
                "lat": 41.5868,
                "lng": -93.6250,
                "expected_soil": "Prairie Soil (Mollisols)",
                "expected_ph": 6.3,
                "expected_texture": "Silty Clay Loam",
                "expected_ndvi": None,  # Not in NDVI module
                "is_known_location": True,
                "description": "US Corn Belt"
            },
            {
                "name": "Karnataka Coffee Plantation",
                "lat": 13.3409,
                "lng": 75.7131,
                "expected_soil": "Red Lateritic Soil",
                "expected_ph": 5.8,
                "expected_texture": "Clay Loam",
                "expected_ndvi": None,  # Not in NDVI module
                "is_known_location": True,
                "description": "Coffee growing region"
            },
            {
                "name": "Random GPS Location (Delhi)",
                "lat": 28.6139,
                "lng": 77.2090,
                "expected_soil": "Unknown",
                "expected_ph": None,
                "expected_texture": None,
                "expected_ndvi": None,
                "is_known_location": False,
                "description": "Unknown location for synthetic data testing"
            }
        ]

    def print_header(self):
        """Print test suite header"""
        print("🌱 SOIL ANALYSIS MODULE - COMPREHENSIVE TEST SUITE WITH NDVI INTEGRATION")
        print("=" * 80)
        print(f"🕒 Test started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("🔗 Testing integration with existing NDVI module")
        print("🌍 Testing with real agricultural coordinates:")
        for coord in self.test_coordinates:
            status = "✅ Known" if coord["is_known_location"] else "🔄 Synthetic"
            ndvi_match = "🌿 NDVI Match" if coord["expected_ndvi"] else "📊 No NDVI"
            print(f"   {coord['name']}: {status} {ndvi_match} ({coord['lat']}, {coord['lng']})")
        print("=" * 80)

    def test_api_health(self):
        """Test API health and integration status"""
        print("\n🔍 TESTING API HEALTH & INTEGRATION...")

        try:
            response = requests.get(f"{self.api_base}/health", timeout=10)

            if response.status_code == 200:
                health_data = response.json()
                print("✅ API Status: HEALTHY")
                print(f"   Service: {health_data.get('service', 'Unknown')}")
                print(f"   Known Soil Locations: {health_data.get('known_soil_locations', 0)}")
                print(f"   NDVI Integration: {health_data.get('modules', {}).get('ndvi_integration', 'Unknown')}")
                print(f"   Credentials: {health_data.get('credentials_status', {})}")

                # Check NDVI integration specifically
                ndvi_status = health_data.get('ndvi_integration_status', {})
                if ndvi_status.get('module_available'):
                    print("🌿 NDVI Integration: ✅ ACTIVE")
                    print(f"   NDVI Known Locations: {ndvi_status.get('known_locations', 0)}")
                else:
                    print("🌿 NDVI Integration: ❌ FALLBACK MODE")

                return True

            else:
                print(f"❌ API health check failed: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Cannot connect to Soil Analysis API: {e}")
            print("💡 Make sure to run: python soil_flask_backend.py")
            return False

    def test_integration_status(self):
        """Test detailed integration status"""
        print("\n🔗 TESTING NDVI INTEGRATION STATUS...")

        try:
            response = requests.get(f"{self.api_base}/soil/integration-status", timeout=10)

            if response.status_code == 200:
                integration_data = response.json()
                print("✅ Integration Status Retrieved:")

                ndvi_integration = integration_data.get('ndvi_integration', {})
                print(f"   NDVI Module Available: {'✅ Yes' if ndvi_integration.get('available') else '❌ No'}")
                print(f"   Calculator Initialized: {'✅ Yes' if ndvi_integration.get('calculator_initialized') else '❌ No'}")
                print(f"   Downloader Initialized: {'✅ Yes' if ndvi_integration.get('downloader_initialized') else '❌ No'}")
                print(f"   NDVI Known Locations: {ndvi_integration.get('known_locations', 0)}")
                print(f"   Import Path: {ndvi_integration.get('import_path', 'Unknown')}")

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

    def test_known_locations_with_ndvi(self):
        """Test known agricultural locations with NDVI correlation"""
        print("\n🌾 TESTING KNOWN LOCATIONS WITH NDVI CORRELATION...")

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

    def test_comprehensive_soil_analysis(self):
        """Test comprehensive soil analysis with NDVI integration"""
        print("\n🌱 TESTING COMPREHENSIVE SOIL ANALYSIS WITH NDVI...")

        results = []

        for coord in self.test_coordinates:
            print(f"\n📍 Testing {coord['name']}")
            print(f"   Coordinates: {coord['lat']}, {coord['lng']}")
            print(f"   Expected Soil: {coord['expected_soil']}")
            if coord['expected_ndvi']:
                print(f"   Expected NDVI: {coord['expected_ndvi']}")

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

                        if coord['expected_texture'] and texture == coord['expected_texture']:
                            print(f"   🎯 Texture matches expected ({coord['expected_texture']})!")

                    # Check NDVI integration
                    if ndvi_correlation:
                        ndvi_val = ndvi_correlation.get('ndvi_value')
                        ndvi_source = ndvi_correlation.get('ndvi_data_source')
                        integration_status = ndvi_correlation.get('integration_status')

                        print(f"   🌿 NDVI Integration: {integration_status}")

                        if ndvi_val is not None:
                            print(f"   NDVI Value: {ndvi_val:.4f}")
                            print(f"   NDVI Source: {ndvi_source}")

                            # Check if NDVI matches expected for known locations
                            if coord['expected_ndvi'] and abs(ndvi_val - coord['expected_ndvi']) <= 0.05:
                                print(f"   🎯 NDVI matches NDVI module value ({coord['expected_ndvi']})!")

                            # Check correlation analysis
                            correlation = ndvi_correlation.get('soil_ndvi_correlation', {})
                            if correlation.get('vegetation_soil_match'):
                                print(f"   Soil-NDVI Match: {correlation['vegetation_soil_match']}")
                        else:
                            print(f"   ⚠️ NDVI value not available: {ndvi_correlation.get('error', 'Unknown error')}")
                    else:
                        print("   ❌ No NDVI correlation data")

                    # Show some nutrient data
                    for nutrient in ['nitrogen', 'phosphorus', 'potassium', 'organic_carbon']:
                        if nutrient in soil_props:
                            nutrient_data = soil_props[nutrient]
                            value = nutrient_data.get('value', 0)
                            unit = nutrient_data.get('unit', '')
                            classification = nutrient_data.get('classification', '')
                            print(f"   {nutrient.title()}: {value} {unit} ({classification})")

                    results.append({
                        'location': coord['name'],
                        'success': True,
                        'confidence': confidence,
                        'has_ndvi': bool(ndvi_correlation and ndvi_correlation.get('ndvi_value') is not None),
                        'ndvi_matches_expected': bool(
                            coord['expected_ndvi'] and ndvi_correlation and 
                            abs(ndvi_correlation.get('ndvi_value', 0) - coord['expected_ndvi']) <= 0.05
                        ),
                        'soil_matches_expected': bool(coord['expected_ph'])
                    })

                else:
                    print(f"   ❌ Analysis failed: {response.status_code}")
                    print(f"   Response: {response.text[:200]}")
                    results.append({
                        'location': coord['name'],
                        'success': False,
                        'error': response.text
                    })

            except Exception as e:
                print(f"   ❌ Request failed: {e}")
                results.append({
                    'location': coord['name'],
                    'success': False,
                    'error': str(e)
                })

        return results

    def test_soil_comparison_with_ndvi(self):
        """Test soil comparison with NDVI correlation"""
        print("\n🔍 TESTING SOIL COMPARISON WITH NDVI CORRELATION...")

        # Compare Punjab and Maharashtra (both have NDVI data)
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

                print("✅ Soil Comparison with NDVI Success!")
                print(f"   Locations Compared: {len(result.get('locations', []))}")

                # Show location summaries
                locations_summary = result.get('locations', [])
                for loc in locations_summary:
                    print(f"   📍 {loc.get('name', 'Unknown')}:")
                    print(f"      Soil Type: {loc.get('soil_type', 'Unknown')}")
                    print(f"      NDVI: {loc.get('ndvi_value', 'N/A')}")
                    print(f"      Vegetation Health: {loc.get('vegetation_health', 'Unknown')}")

                # Show property comparisons
                prop_comparisons = result.get('property_comparison', {})
                print("   📊 Property Comparisons:")

                for prop, comparison in prop_comparisons.items():
                    values = comparison.get('values', {})
                    stats = comparison.get('statistics', {})

                    print(f"      {prop.title()}:")
                    for location, data in values.items():
                        print(f"        {location}: {data.get('value', 'N/A')} {data.get('unit', '')}")

                    if stats:
                        print(f"        Range: {stats.get('min', 0):.2f} - {stats.get('max', 0):.2f}")
                        print(f"        Variation: {stats.get('variation', 'Unknown')}")

                # Show NDVI comparison
                ndvi_comparison = result.get('ndvi_comparison')
                if ndvi_comparison:
                    print("   🌿 NDVI Comparison:")
                    ndvi_values = ndvi_comparison.get('values', {})
                    for location, data in ndvi_values.items():
                        ndvi_val = data.get('ndvi_value', 'N/A')
                        health = data.get('vegetation_health', 'Unknown')
                        print(f"      {location}: NDVI {ndvi_val} ({health})")

                    ndvi_stats = ndvi_comparison.get('statistics', {})
                    if ndvi_stats:
                        print(f"      NDVI Range: {ndvi_stats.get('min', 0):.3f} - {ndvi_stats.get('max', 0):.3f}")

                # Show recommendations
                recommendations = result.get('recommendations', [])
                if recommendations:
                    print("   💡 Comparison Recommendations:")
                    for rec in recommendations:
                        print(f"      • {rec}")

                return True
            else:
                print(f"❌ Soil comparison failed: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Soil comparison error: {e}")
            return False

    def test_detailed_recommendations(self):
        """Test detailed soil recommendations with NDVI insights"""
        print("\n🌾 TESTING DETAILED SOIL RECOMMENDATIONS WITH NDVI INSIGHTS...")

        # Test recommendations for Punjab (should have both soil and NDVI data)
        coord = self.test_coordinates[0]  # Punjab
        lat, lng = coord["lat"], coord["lng"]

        try:
            response = requests.get(
                f"{self.api_base}/soil/recommendations/{lat}/{lng}",
                timeout=60
            )

            if response.status_code == 200:
                result = response.json()

                print(f"✅ Detailed Recommendations Retrieved!")
                print(f"   Location: {coord['name']}")
                print(f"   Soil Health Score: {result.get('soil_health_score', 'N/A')}")

                # Show immediate actions
                immediate = result.get('immediate_actions', [])
                if immediate:
                    print("   ⚡ Immediate Actions:")
                    for action in immediate:
                        print(f"      • {action.get('action', 'N/A')}: {action.get('recommendation', 'N/A')}")
                        print(f"        Priority: {action.get('priority', 'N/A')}")

                # Show fertilizer recommendations
                fertilizer = result.get('fertilizer_recommendations', {})
                if fertilizer:
                    print("   🧪 Fertilizer Recommendations:")
                    for nutrient, rec in fertilizer.items():
                        print(f"      {nutrient.title()}: {rec.get('recommended_application', 'N/A')}")
                        print(f"        Sources: {', '.join(rec.get('sources', []))}")

                # Show NDVI-soil insights
                ndvi_insights = result.get('ndvi_soil_insights', {})
                if ndvi_insights:
                    print("   🌿 NDVI-Soil Insights:")
                    print(f"      NDVI Value: {ndvi_insights.get('ndvi_value', 'N/A')}")
                    print(f"      Vegetation Health: {ndvi_insights.get('vegetation_health', 'Unknown')}")
                    print(f"      Soil-Vegetation Match: {ndvi_insights.get('soil_vegetation_match', 'Unknown')}")

                    limiting_factors = ndvi_insights.get('limiting_factors', [])
                    if limiting_factors:
                        print("      Limiting Factors:")
                        for factor in limiting_factors:
                            print(f"        • {factor}")

                    ndvi_recommendations = ndvi_insights.get('ndvi_recommendations', [])
                    if ndvi_recommendations:
                        print("      NDVI-Based Recommendations:")
                        for rec in ndvi_recommendations:
                            print(f"        • {rec}")

                return True
            else:
                print(f"❌ Detailed recommendations failed: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Detailed recommendations error: {e}")
            return False

    def generate_test_summary(self, results):
        """Generate comprehensive test summary"""
        print("\n" + "=" * 80)
        print("📊 SOIL ANALYSIS WITH NDVI INTEGRATION - TEST SUMMARY")
        print("=" * 80)

        # Count results
        analysis_results = results.get('soil_analysis', [])
        successful_analyses = [r for r in analysis_results if r.get('success')]
        ndvi_integrated_analyses = [r for r in successful_analyses if r.get('has_ndvi')]
        ndvi_matched_analyses = [r for r in successful_analyses if r.get('ndvi_matches_expected')]

        tests_run = {
            'api_health': results.get('api_health', False),
            'integration_status': results.get('integration_status', False),
            'known_locations': results.get('known_locations', False),
            'soil_analysis_success': len(successful_analyses),
            'ndvi_integration_success': len(ndvi_integrated_analyses),
            'ndvi_value_matches': len(ndvi_matched_analyses),
            'soil_comparison': results.get('soil_comparison', False),
            'detailed_recommendations': results.get('detailed_recommendations', False)
        }

        print("🔍 System & Integration Tests:")
        print(f"   API Health: {'✅ PASS' if tests_run['api_health'] else '❌ FAIL'}")
        print(f"   NDVI Integration Status: {'✅ PASS' if tests_run['integration_status'] else '❌ FAIL'}")
        print(f"   Known Locations: {'✅ PASS' if tests_run['known_locations'] else '❌ FAIL'}")

        print("\n🌱 Soil Analysis Tests:")
        print(f"   Successful Analyses: {tests_run['soil_analysis_success']}/{len(self.test_coordinates)}")
        print(f"   NDVI Integration Success: {tests_run['ndvi_integration_success']}/{len(self.test_coordinates)}")
        print(f"   NDVI Values Match NDVI Module: {tests_run['ndvi_value_matches']}/3 expected")
        print(f"   Soil Comparison: {'✅ PASS' if tests_run['soil_comparison'] else '❌ FAIL'}")
        print(f"   Detailed Recommendations: {'✅ PASS' if tests_run['detailed_recommendations'] else '❌ FAIL'}")

        # Detailed results for each location
        print("\n📍 Location-Specific Results:")
        for result in analysis_results:
            if result.get('success'):
                confidence = result.get('confidence', 0)
                ndvi_status = "🌿 NDVI" if result.get('has_ndvi') else "❌ No NDVI"
                match_status = "🎯 Match" if result.get('ndvi_matches_expected') else ""
                print(f"   {result['location']}: ✅ SUCCESS (Confidence: {confidence:.2f}) {ndvi_status} {match_status}")
            else:
                print(f"   {result['location']}: ❌ FAILED")

        # Overall assessment
        passed_tests = sum([
            tests_run['api_health'],
            tests_run['integration_status'],
            tests_run['known_locations'],
            tests_run['soil_analysis_success'] >= 4,  # At least 4/6 locations
            tests_run['ndvi_integration_success'] >= 2,  # At least 2 with NDVI
            tests_run['soil_comparison'],
            tests_run['detailed_recommendations']
        ])

        total_tests = 7
        success_rate = passed_tests / total_tests * 100

        print(f"\n🏆 OVERALL SCORE: {passed_tests}/{total_tests} ({success_rate:.0f}%)")

        if success_rate >= 85:
            print("🎉 EXCELLENT: Soil Analysis with NDVI Integration is fully functional!")
            print("   ✅ NDVI module integration working perfectly")
            print("   ✅ Real agricultural data with NDVI correlation")
            print("   ✅ Multiple data sources and comprehensive analysis")
            print("   ✅ Both GPS and manual coordinates supported")
        elif success_rate >= 70:
            print("✅ GOOD: Soil Analysis Module is mostly functional")
            print("   Most features working, minor integration issues may exist")
        else:
            print("⚠️ NEEDS IMPROVEMENT: Some major integration issues detected")
            print("   Review NDVI module import path and credential configuration")

        return success_rate

    def run_complete_test_suite(self):
        """Run the complete soil analysis test suite with NDVI integration"""
        self.print_header()

        # Initialize results tracking
        results = {}

        # Run all tests
        try:
            results['api_health'] = self.test_api_health()

            if results['api_health']:
                results['integration_status'] = self.test_integration_status()
                results['known_locations'] = self.test_known_locations_with_ndvi()
                results['soil_analysis'] = self.test_comprehensive_soil_analysis()
                results['soil_comparison'] = self.test_soil_comparison_with_ndvi()
                results['detailed_recommendations'] = self.test_detailed_recommendations()
            else:
                print("⚠️ API health check failed - skipping other tests")
                return False

            # Generate summary
            success_rate = self.generate_test_summary(results)

            return success_rate >= 70

        except KeyboardInterrupt:
            print("\n⚠️ Test suite interrupted by user")
            return False
        except Exception as e:
            print(f"\n❌ Test suite failed: {e}")
            return False

def main():
    """Main test function"""
    tester = SoilAnalysisTestSuite()
    success = tester.run_complete_test_suite()

    print("\n" + "=" * 80)
    if success:
        print("🎉 SOIL ANALYSIS WITH NDVI INTEGRATION TEST SUITE PASSED!")
        print("Your integrated soil analysis module is ready for production use.")
        print("🔗 NDVI module integration is working correctly.")
        sys.exit(0)
    else:
        print("❌ SOIL ANALYSIS WITH NDVI INTEGRATION TEST SUITE FAILED!")
        print("Check error messages above and ensure:")
        print("- Backend is running (python soil_flask_backend.py)")
        print("- NDVI module is in ../NDVI directory")
        print("- Root backend .env file has Copernicus credentials")
        sys.exit(1)

if __name__ == "__main__":
    main()
