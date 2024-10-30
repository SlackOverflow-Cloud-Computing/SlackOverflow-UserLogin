import requests
import json
from datetime import datetime

# API endpoint
BASE_URL = "http://localhost:8088"  # Adjust if your service runs on a different port
UPDATE_USER_ENDPOINT = f"{BASE_URL}/update_user"

# Sample test data
test_user = {
    "id": "31r3oo7j5aprbprysabzqq2iflqp",
    "username": "notyixuan",
    "email": "notyixuan@gmail.com",
    "profile_image": None,
    "country": "US",
    "created_at": "2024-10-28T23:09:20",
    "last_login": "2024-10-28T23:09:23"
}

# Sample token (modify as needed)
test_token = {
    "access_token": "sample_access_token",
    "token_type": "Bearer",
    "expires_in": 3600,
    "refresh_token": "sample_refresh_token",
    "scope": "user-read-private user-read-email"
}

# Request payload
payload = {
    "user": test_user,
    "token": test_token
}

def test_update_user():
    try:
        # Make POST request
        response = requests.post(
            UPDATE_USER_ENDPOINT,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        # Print response details
        print(f"Status Code: {response.status_code}")
        print("\nResponse Headers:")
        print(json.dumps(dict(response.headers), indent=2))
        print("\nResponse Body:")
        print(json.dumps(response.json(), indent=2))
        
        # Check if request was successful
        if response.status_code == 200:
            print("\n✅ Test passed: User update successful")
        else:
            print(f"\n❌ Test failed: Received status code {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Test failed: {str(e)}")

def main():
    print("🚀 Starting API test for update_user endpoint...")
    print("\nTest payload:")
    print(json.dumps(payload, indent=2))
    print("\nSending request...")
    test_update_user()

if __name__ == "__main__":
    main()