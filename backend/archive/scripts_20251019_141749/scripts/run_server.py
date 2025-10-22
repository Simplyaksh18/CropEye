#!/usr/bin/env python3
"""
Development server runner for CropEye Location-Based GIS API
"""
import os
import sys
from dotenv import load_dotenv

# Ensure we load the backend .env even when this script is run from the repository root.
# The backend folder is one level up from this scripts/ directory.
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ENV_PATH = os.path.join(BASE_DIR, '.env')
if os.path.exists(ENV_PATH):
    load_dotenv(ENV_PATH)
else:
    # Fallback to any .env found on the current working directory
    load_dotenv()

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

    # Ensure backend package path is importable regardless of current working directory
    BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if BACKEND_DIR not in sys.path:
        sys.path.insert(0, BACKEND_DIR)

    # Import and run the Flask app
    try:
        # Now `app.py` inside backend/ is importable as top-level module `app`.
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
