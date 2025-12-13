"""
Vercel Serverless Function Entry Point for CropEye Backend

This file serves as the entry point for Vercel's serverless deployment.
It imports the Flask app from app.py and exports it as the handler.
"""

import sys
import os

# Add the parent directory (backend) to Python path so we can import app
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)

# Import the Flask app instance
from app import app

# Export the Flask app as the handler for Vercel
handler = app

# Also ensure app is exposed if imported directly
__all__ = ['app', 'handler']
