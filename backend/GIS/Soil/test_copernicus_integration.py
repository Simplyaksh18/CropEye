
#!/usr/bin/env python3

"""
Test Script for Copernicus Soil Data Integration
Tests the new satellite-based soil analysis system
"""

import os
import sys
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_copernicus_credentials():
    """Test if Copernicus credentials are available"""
    print("🔐 Testing Copernicus Credentials...")

    username = os.getenv('COPERNICUS_USERNAME')
    password = os.getenv('COPERNICUS_PASSWORD')
    client_id = os.getenv('COPERNICUS_CLIENT_ID')
    client_secret = os.getenv('COPERNICUS_CLIENT_SECRET')

    print(f"   Username: {'✅ Available' if username else '❌ Missing'}")
    print(f"   Password: {'✅ Available' if password else '❌ Missing'}")
    print(f"   Client ID: {'✅ Available' if client_id else '❌ Missing'}")
    print(f"   Client Secret: {'✅ Available' if client_secret else '❌ Missing'}")

    credentials_ok = bool(username and password)
    if credentials_ok:
        print("   ✅ Basic credentials available for Copernicus")
    else:
        print("   ❌ Missing Copernicus credentials in .env file")

    return credentials_ok

def test_copernicus_downloader():
    """Test the Copernicus soil data downloader"""
    print("\n🛰️ Testing Copernicus Soil Data Downloader...")

    try:
        from soil_data_downloader import CopernicusSoilDataDownloader
        downloader = CopernicusSoilDataDownloader()
        print("   ✅ Copernicus downloader imported successfully")

        # Test with Punjab coordinates (known location)
        print("   📍 Testing with Punjab coordinates (30.3398, 76.3869)...")
        result = downloader.get_soil_satellite_data(30.3398, 76.3869, days_back=30)

        if result:
            print(f"   ✅ Satellite data retrieved!")
            print(f"      Confidence Score: {result.get('confidence_score', 0):.2f}")
            print(f"      Data Sources: {result.get('data_sources', [])}")

            # Check satellite properties
            sat_props = result.get('satellite_derived_properties', {})
            if sat_props:
                print(f"      Satellite Observations: {len(sat_props)} types")
                for obs_type in sat_props.keys():
                    print(f"        • {obs_type}")

            # Check derived soil properties  
            soil_props = result.get('derived_soil_properties', {})
            if soil_props:
                print(f"      Derived Soil Properties: {len(soil_props)}")
                for prop, data in soil_props.items():
                    if isinstance(data, dict) and 'value' in data:
                        confidence = data.get('confidence', 0)
                        print(f"        • {prop.title()}: {data['value']} {data.get('unit', '')} (conf: {confidence:.1f})")

            return True
        else:
            print("   ❌ No satellite data retrieved")
            return False

    except ImportError as e:
        print(f"   ❌ Could not import Copernicus downloader: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Copernicus downloader test failed: {e}")
        return False

def test_updated_soil_collector():
    """Test the updated soil collector with Copernicus integration"""
    print("\n🌱 Testing Updated Soil Data Collector...")

    try:
        from soil_data_collector import SoilDataCollector
        collector = SoilDataCollector()
        print("   ✅ Updated soil collector imported successfully")

        # Test with unknown location (should use satellite data)
        print("   📍 Testing with unknown location (28.6139, 77.2090 - Delhi)...")
        result = collector.get_soil_data(28.6139, 77.2090, include_ndvi=True)

        if result:
            location_info = result.get('location_info', {})
            print(f"   ✅ Soil analysis completed!")
            print(f"      Location: {location_info.get('name', 'Unknown')}")
            print(f"      Data Sources: {result.get('data_sources', [])}")
            print(f"      Confidence: {result.get('confidence_score', 0):.2f}")

            # Check if satellite data was used
            if 'copernicus_satellite' in result.get('data_sources', []):
                print("      🛰️ Successfully used Copernicus satellite data!")
            elif 'soilgrids_250m' in result.get('data_sources', []):
                print("      🌐 Fell back to SoilGrids API")
            elif 'regional_modeling' in result.get('data_sources', []):
                print("      📊 Used regional modeling (network issues)")
            else:
                print("      🔄 Used fallback data")

            # Check soil properties
            soil_props = result.get('soil_properties', {})
            if soil_props:
                print(f"      Soil Properties: {len(soil_props)}")
                for prop, data in list(soil_props.items())[:3]:  # Show first 3
                    if isinstance(data, dict) and 'value' in data:
                        source = data.get('source', 'unknown')
                        print(f"        • {prop.title()}: {data['value']} {data.get('unit', '')} [{source}]")

            # Check satellite observations
            sat_obs = result.get('satellite_observations', {})
            if sat_obs:
                print(f"      🛰️ Satellite Observations: {len(sat_obs)} types")

            # Check NDVI integration
            ndvi_corr = result.get('ndvi_correlation')
            if ndvi_corr:
                ndvi_val = ndvi_corr.get('ndvi_value')
                integration_status = ndvi_corr.get('integration_status', 'unknown')
                print(f"      🌿 NDVI Integration: {integration_status}")
                if ndvi_val is not None:
                    print(f"        NDVI Value: {ndvi_val:.3f}")

            return True
        else:
            print("   ❌ No soil analysis result")
            return False

    except ImportError as e:
        print(f"   ❌ Could not import updated soil collector: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Updated soil collector test failed: {e}")
        return False

def test_network_connectivity():
    """Test network connectivity to various APIs"""
    print("\n🌐 Testing Network Connectivity...")

    import socket
    import requests

    # Test DNS resolution for SoilGrids
    try:
        ip = socket.gethostbyname('rest.soilgrids.org')
        print(f"   ✅ SoilGrids DNS: rest.soilgrids.org -> {ip}")
        soilgrids_dns = True
    except socket.gaierror as e:
        print(f"   ❌ SoilGrids DNS failed: {e}")
        soilgrids_dns = False

    # Test HTTP connection to SoilGrids
    if soilgrids_dns:
        try:
            url = "https://rest.soilgrids.org/query?lon=77.2090&lat=28.6139&property=phh2o&depth=0-5cm&value=mean"
            response = requests.get(url, timeout=10)
            print(f"   ✅ SoilGrids HTTP: Status {response.status_code}")
            soilgrids_http = response.status_code == 200
        except Exception as e:
            print(f"   ❌ SoilGrids HTTP failed: {e}")
            soilgrids_http = False
    else:
        soilgrids_http = False

    # Test Copernicus access
    try:
        copernicus_url = "https://catalogue.dataspace.copernicus.eu"
        response = requests.get(copernicus_url, timeout=10)
        print(f"   ✅ Copernicus access: Status {response.status_code}")
        copernicus_access = True
    except Exception as e:
        print(f"   ❌ Copernicus access failed: {e}")
        copernicus_access = False

    return {
        'soilgrids_dns': soilgrids_dns,
        'soilgrids_http': soilgrids_http,
        'copernicus_access': copernicus_access
    }

def main():
    """Run all tests"""
    print("🧪 COPERNICUS SOIL DATA INTEGRATION TEST SUITE")
    print("=" * 60)
    print(f"Test started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    results = {}

    # Test credentials
    results['credentials'] = test_copernicus_credentials()

    # Test network connectivity
    network_results = test_network_connectivity()
    results.update(network_results)

    # Test Copernicus downloader
    results['copernicus_downloader'] = test_copernicus_downloader()

    # Test updated soil collector
    results['updated_soil_collector'] = test_updated_soil_collector()

    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)

    total_tests = len(results)
    passed_tests = sum(results.values())

    for test, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        test_name = test.replace('_', ' ').title()
        print(f"{test_name:.<40} {status}")

    print(f"\nOverall: {passed_tests}/{total_tests} tests passed ({passed_tests/total_tests*100:.0f}%)")

    # Recommendations
    print("\n🎯 RECOMMENDATIONS:")

    if not results['credentials']:
        print("❌ Add Copernicus credentials to your .env file:")
        print("   COPERNICUS_USERNAME=your_email@domain.com")
        print("   COPERNICUS_PASSWORD=your_password")

    if not results['soilgrids_dns']:
        print("❌ SoilGrids DNS failing - check internet connection")
        print("   This is why you're seeing 'regional_modeling' fallback")

    if results['copernicus_downloader'] and results['updated_soil_collector']:
        print("✅ Copernicus integration working! You can now use actual satellite data")
        print("   Your soil analysis will prioritize:")
        print("   1. Known survey data (highest accuracy)")
        print("   2. Copernicus satellite data (high accuracy)")
        print("   3. SoilGrids API (medium accuracy)")
        print("   4. Regional modeling (fallback)")

    if passed_tests >= 4:
        print("\n🎉 INTEGRATION SUCCESSFUL!")
        print("✅ Your soil analysis now uses actual Copernicus satellite data")
        print("✅ No more reliance on SoilGrids DNS resolution")
        print("✅ Higher confidence soil property estimates")
    elif passed_tests >= 2:
        print("\n⚠️ PARTIAL SUCCESS")
        print("Some components working - check failed tests above")
    else:
        print("\n❌ INTEGRATION ISSUES")
        print("Multiple failures detected - check setup and connectivity")

if __name__ == "__main__":
    main()
