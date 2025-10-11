#!/usr/bin/env python3
"""
Development server runner for CropEye Location-Based GIS API
"""
import os
import sys

def main():
    """Run the development server with proper configuration"""

    print("=" * 70)
    print("🌱 CropEye Location-Based GIS API")
    print("=" * 70)
    print("📍 Accepts user location coordinates")
    print("🛰️  Processes satellite data (ready for your implementation)")
    print("🌾 Provides agricultural analysis and recommendations")
    print("=" * 70)

    # Check if .env file exists
    if not os.path.exists('.env'):
        print("⚠️  No .env file found - using default configuration")
        print("💡 Copy .env.example to .env to customize settings")

    # Import and run the Flask app
    try:
        from app import app

        print("\n🚀 Starting development server...")
        print("🌐 API available at: http://localhost:5000")
        print("🔗 Test with frontend at: http://localhost:3000")
        print("\n📝 API Endpoints:")
        print("   POST /api/analyze-location - Analyze coordinates")
        print("   GET  /api/status          - Implementation status") 
        print("   GET  /health             - Health check")
        print("\n🔨 Ready for your GIS implementation!")
        print("-" * 50)

        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True
        )

    except ImportError as e:
        print(f"❌ Error importing Flask app: {e}")
        print("💡 Make sure you're in the backend directory and have installed requirements")
        return 1
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
