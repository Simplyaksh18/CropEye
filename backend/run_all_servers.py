#!/usr/bin/env python3
"""
Runs all backend microservices (Main App, NDVI, Soil) concurrently.

This script opens a new terminal window for each service, making it easy
to see the logs for each one independently.
"""
import subprocess
import sys
import os
import time

# Get the base directory of the backend
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Define the servers to run
servers = {
    "Main App": {
        "script": os.path.join(BASE_DIR, 'app.py'),
        "port": 5000
    },
    "NDVI Service": {
        "script": os.path.join(BASE_DIR, 'GIS', 'NDVI', 'ndvi_flask_backend.py'),
        "port": 5001
    },
    "Soil Service": {
        "script": os.path.join(BASE_DIR, 'GIS', 'Soil', 'soil_flask_backend.py'),
        "port": 5002
    },
    "Weather Service": {
        "script": os.path.join(BASE_DIR, 'GIS', 'Weather', 'weather_flask_backend.py'),
        "port": 5003
    }
}

def main():
    print("=" * 80)
    print("🚀 Launching CropEye Backend Microservices...")
    print("=" * 80)

    processes = []
    for name, config in servers.items():
        # Use PowerShell windows so developers get familiar PowerShell shells
        # Build a single command string that uses the Windows `start` to open
        # a new PowerShell window which runs the Python script and stays open.
        ps_command = (
            f"start powershell -NoExit -Command \"& '{sys.executable}' '{config['script']}'\""
        )
        print(f"  -> Starting {name} on port {config['port']} in a new PowerShell window...")
        # Use shell=True so the `start` builtin is executed by cmd.exe
        proc = subprocess.Popen(ps_command, shell=True, cwd=BASE_DIR)
        processes.append(proc)
        time.sleep(1)  # Stagger the launches slightly

    print("\n✅ All services have been launched in separate windows.")
    print("   You can monitor the logs for each service in its respective window.")
    print("   To stop the services, close each of the new terminal windows.")

if __name__ == "__main__":
    main()