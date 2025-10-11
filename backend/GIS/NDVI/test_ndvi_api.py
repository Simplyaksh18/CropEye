#!/usr/bin/env python3
"""
Comprehensive Test Script for Corrected NDVI System
Tests both real data and fallback scenarios
"""

import os
import requests
import json
import time
import subprocess
import sys
from datetime import datetime

class NDVISystemTester:
    def __init__(self):
        self.api_base = "http://127.0.0.1:5001/api"
        self.test_coordinates = [
            {"name": "Punjab Wheat", "lat": 30.3398, "lng": 76.3869, "expected_ndvi": 0.5},
            {"name": "Maharashtra Sugarcane", "lat": 18.1500, "lng": 74.5777, "expected_ndvi": 0.6},
            {"name": "California Vineyard", "lat": 36.7783, "lng": -119.4179, "expected_ndvi": 0.4},
        ]

    def test_api_health(self):
        """Test API health endpoint"""
        print("🔍 Testing API Health...")
        try:
            response = requests.get(f"{self.api_base}/health", timeout=10)

            if response.status_code == 200:
                health_data = response.json()
                print(f"✅ API Status: {health_data['status']}")
                print(f"   Services: {health_data['services']}")
                print(f"   Message: {health_data.get('message', 'N/A')}")
                return True
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Cannot connect to API: {e}")
            return False

    def test_debug_info(self):
        """Test debug endpoint"""
        print("\n🔧 Testing Debug Information...")
        try:
            response = requests.get(f"{self.api_base}/ndvi/debug", timeout=10)

            if response.status_code == 200:
                debug_data = response.json()
                print("✅ Debug Info Retrieved:")
                print(f"   Working Directory: {debug_data.get('working_directory', 'N/A')}")
                print(f"   Environment Variables: {debug_data.get('environment_variables', {})}")
                print(f"   Modules Available: {debug_data.get('modules_available', {})}")
                return True
            else:
                print(f"⚠️ Debug endpoint returned: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Debug test failed: {e}")
            return False

    def test_sample_data_analysis(self):
        """Test NDVI analysis with sample data"""
        print("\n🌱 Testing Sample Data Analysis...")

        all_passed = True

        for coord in self.test_coordinates:
            print(f"\n📍 Testing {coord['name']} ({coord['lat']}, {coord['lng']})")

            payload = {
                "latitude": coord["lat"],
                "longitude": coord["lng"],
                "use_real_data": False  # Use sample data
            }

            try:
                response = requests.post(
                    f"{self.api_base}/ndvi/analyze",
                    json=payload,
                    timeout=30
                )

                if response.status_code == 200:
                    result = response.json()
                    print(f"✅ Analysis Success!")
                    print(f"   NDVI Value: {result['ndvi']['value']}")
                    print(f"   Data Source: {result['data_source']}")
                    print(f"   Health Category: {result['health_analysis']['category']}")
                    print(f"   Health Score: {result['health_analysis']['health_score']}")

                    # Verify reasonable NDVI values
                    ndvi_val = result['ndvi']['value']
                    if -1 <= ndvi_val <= 1:
                        print(f"   ✅ NDVI in valid range: {ndvi_val}")
                    else:
                        print(f"   ⚠️ NDVI outside valid range: {ndvi_val}")
                        all_passed = False

                    # Check if it's marked as sample data
                    # For known locations, 'verified_ground_truth' is also a valid "sample" response.
                    is_sample_ok = not result['verification']['is_real_data'] or result['data_source'] == 'verified_ground_truth'
                    if is_sample_ok:
                        print(f"   ✅ Correctly marked as sample data")
                    else:
                        print(f"   ❌ Expected sample data, but got real data unexpectedly.")
                        all_passed = False

                else:
                    print(f"   ❌ Analysis failed: {response.status_code}")
                    print(f"   Response: {response.text[:200]}")
                    all_passed = False

            except Exception as e:
                print(f"   ❌ Request failed: {e}")
                all_passed = False

        return all_passed

    def test_real_data_analysis(self):
        """Test NDVI analysis with real data request"""
        print("\n🛰️ Testing Real Data Analysis...")

        # Test with Punjab coordinates (most likely to have good data)
        coord = self.test_coordinates[0]  # Punjab
        print(f"📍 Testing {coord['name']} with real data request...")

        payload = {
            "latitude": coord["lat"],
            "longitude": coord["lng"],
            "use_real_data": True,  # Try real data
            "days_back": 30,
            "cloud_cover_max": 50
        }

        try:
            response = requests.post(
                f"{self.api_base}/ndvi/analyze",
                json=payload,
                timeout=60  # Longer timeout for real data
            )

            if response.status_code == 200:
                result = response.json()
                print(f"✅ Real Data Analysis Complete!")
                print(f"   NDVI Value: {result['ndvi']['value']}")
                print(f"   Data Source: {result['data_source']}")
                print(f"   Is Real Data: {result['verification']['is_real_data']}")
                print(f"   Data Quality: {result['verification']['data_quality']}")
                print(f"   Processing Method: {result['verification']['processing_method']}")

                # Analyze what kind of data we got
                if result['verification']['is_real_data']:
                    print("   🎯 SUCCESS: Got real satellite data!")
                else:
                    print("   ⚠️ Fallback: Using sample data (real data not available)")

                return result['verification']['is_real_data']

            else:
                print(f"   ❌ Real data analysis failed: {response.status_code}")
                print(f"   Response: {response.text[:200]}")
                return False

        except Exception as e:
            print(f"   ❌ Real data request failed: {e}")
            return False

    def test_time_series(self):
        """Test time series endpoint"""
        print("\n📊 Testing Time Series Analysis...")

        coord = self.test_coordinates[0]  # Punjab
        payload = {
            "latitude": coord["lat"],
            "longitude": coord["lng"],
            "months_back": 6
        }

        try:
            response = requests.post(
                f"{self.api_base}/ndvi/time-series",
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                print("✅ Time Series Retrieved!")
                print(f"   Data Points: {len(result['time_series']['dates'])}")
                print(f"   Date Range: {result['time_series']['dates'][0]} to {result['time_series']['dates'][-1]}")
                print(f"   NDVI Range: {min(result['time_series']['ndvi_values']):.3f} - {max(result['time_series']['ndvi_values']):.3f}")
                print(f"   Data Source: {result['time_series']['data_source']}")
                return True
            else:
                print(f"❌ Time series failed: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Time series test failed: {e}")
            return False

    def test_visualization(self):
        """Test visualization endpoint"""
        print("\n🗺️ Testing Visualization Generation...")

        coord = self.test_coordinates[0]  # Punjab

        try:
            response = requests.get(
                f"{self.api_base}/ndvi/visualization/{coord['lat']}/{coord['lng']}",
                timeout=30
            )

            if response.status_code == 200:
                print("✅ Visualization Generated!")
                print(f"   Content Type: {response.headers.get('Content-Type', 'Unknown')}")
                print(f"   Content Length: {len(response.content)} bytes")

                # Save visualization for inspection
                with open("test_ndvi_visualization.png", "wb") as f:
                    f.write(response.content)
                print("   Saved as: test_ndvi_visualization.png")
                return True
            else:
                print(f"❌ Visualization failed: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Visualization test failed: {e}")
            return False

    def run_comprehensive_test(self):
        """Run all tests"""
        print("🧪 NDVI System Comprehensive Test Suite")
        print("=" * 60)
        print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Track test results
        results = {
            'health': False,
            'debug': False,
            'sample_data': False,
            'real_data': False,
            'time_series': False,
            'visualization': False
        }

        # Run tests
        results['health'] = self.test_api_health()
        results['debug'] = self.test_debug_info()
        results['sample_data'] = self.test_sample_data_analysis()
        results['real_data'] = self.test_real_data_analysis()
        results['time_series'] = self.test_time_series()
        results['visualization'] = self.test_visualization()

        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)

        passed = sum(results.values())
        total = len(results)

        for test, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{test.replace('_', ' ').title():.<40} {status}")

        print(f"\nOverall: {passed}/{total} tests passed ({passed/total*100:.0f}%)")

        if passed >= 4:  # At least basic functionality working
            print("🎉 System is functional and ready for use!")
        elif passed >= 2:  # Basic API working
            print("⚠️ System partially functional - some features may not work")
        else:
            print("❌ System has major issues - troubleshooting needed")

        return passed, total

def main():
    """Main test function"""
    tester = NDVISystemTester()
    passed, total = tester.run_comprehensive_test()

    if passed == total:
        sys.exit(0)  # All tests passed
    else:
        sys.exit(1)  # Some tests failed

if __name__ == "__main__":
    main()
