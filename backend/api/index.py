"""
Vercel Serverless Function Entry Point for CropEye Backend

This file serves as the entry point for Vercel's serverless deployment.
It imports the Flask app from app.py and exports it as the handler.
"""

import sys
import os

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import the Flask app instance
from app import app

# Export the Flask app as the handler
handler = app
