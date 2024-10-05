import requests
from pydantic import ValidationError

from app.models.user import User


class LoginService:

    def __init__(self, url: str):
        self.url = url

    def get_user_info(self, auth_code):
        payload = {'auth_code': auth_code}

        # Send a POST request to the Spotify integration service to exchange the auth code for user info
        try:
            response = requests.post(f"{self.url}/login", json=payload)

            # Check if the request was successful
            if response.status_code != 200:
                return None

            try:
                data = response.json()
                user = User.parse_obj(data)
                return user
            except ValidationError as e:
                print(f"Validation error: {str(e)}")
                return None


        except requests.RequestException as e:
            print(f"Request failed: {str(e)}")
            return None
