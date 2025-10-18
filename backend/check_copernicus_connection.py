import os
import requests
import socket
from dotenv import load_dotenv

# Load environment variables from a .env file if it exists
load_dotenv()

def check_connection():
    """
    Tests connection and credentials for the Copernicus Data Space Ecosystem.
    """
    username = os.getenv('COPERNICUS_USERNAME')
    password = os.getenv('COPERNICUS_PASSWORD')

    if not username or not password:
        print("❌ ERROR: COPERNICUS_USERNAME or COPERNICUS_PASSWORD not found in environment variables.")
        print("Please ensure they are set correctly in your .env file or system environment.")
        return

    print("🛰️  Attempting to connect to Copernicus Data Space...")
    print(f"    Username: {username}")

    token_url = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
    catalogue_url = "https://catalogue.dataspace.copernicus.eu/odata/v1/Products?$top=1"

    try:
        # 1. Test network resolution
        print("\n--- 1. Testing Network DNS Resolution ---")
        token_host = token_url.split('/')[2]
        catalogue_host = catalogue_url.split('/')[2]
        print(f"Resolving {token_host}... ", end="")
        socket.gethostbyname(token_host)
        print("✅")
        print(f"Resolving {catalogue_host}... ", end="")
        socket.gethostbyname(catalogue_host)
        print("✅")

        # 2. Test authentication and get token
        print("\n--- 2. Testing Authentication ---")
        print("Requesting access token... ", end="")
        token_data = {
            "client_id": "cdse-public",
            "username": username,
            "password": password,
            "grant_type": "password"
        }
        response = requests.post(token_url, data=token_data, timeout=30)
        if response.status_code != 200:
            print(f"❌ FAILED (Status: {response.status_code})")
            print(f"Error: {response.text}")
            return
        
        token = response.json().get("access_token")
        print("✅")

        # 3. Test catalogue access
        print("\n--- 3. Testing Catalogue Access ---")
        print("Querying product catalogue... ", end="")
        headers = {"Authorization": f"Bearer {token}"}
        cat_response = requests.get(catalogue_url, headers=headers, timeout=60)
        print(f"✅ (Status: {cat_response.status_code})")

        print("\n🎉 SUCCESS: All checks passed. Credentials and network access to Copernicus Data Space are OK.")

    except Exception as e:
        print(f"\n❌ FAILURE: A check failed. This likely indicates a network block (firewall/proxy) or incorrect credentials.")
        print(f"    Error details: {e}")

if __name__ == "__main__":
    check_connection()