from typing import Any
from datetime import datetime, timedelta
import dotenv, os

import jwt

from framework.resources.base_resource import BaseResource
from app.models.user import User
from app.models.token import Token
from app.services.service_factory import ServiceFactory

dotenv.load_dotenv()
db = os.getenv('DB_NAME')
collection = os.getenv('DB_COLLECTION')

# JWT Info
JWT_SECRET = os.getenv('JWT_SECRET')
ALGORITHM = "HS256"
MINUTES_TO_EXPIRATION = 60


def create_user_jwt(user: User) -> str:
    """Create a JWT token with the given data.

    Data should be a dictionary with the info to be stored in the token.
    For us this will be the user's Spotify ID and scopes.
    """

    data = {
        "sub": user.id,
        "iat": datetime.utcnow()
    }
    encoded_jwt = jwt.encode(data, JWT_SECRET, algorithm=ALGORITHM)
    return encoded_jwt

class UserResource(BaseResource):

    def __init__(self, config):
        super().__init__(config)

        self.data_service = ServiceFactory.get_service("UserResourceDataService")
        self.database = db
        self.collection = 'spotify_user'
        self.token_collection = 'token'
        self.key_field = "id"
        self.token_key_field = 'access_token'

    def get_by_key(self, key: str) -> User:

        d_service = self.data_service

        result = d_service.get_data_object(
            self.database, self.collection, key_field=self.key_field, key_value=key
        )
        if result:
            result = User(**result)
        return result

    def get_by_token(self, token: str) -> Token:

        d_service = self.data_service

        result = d_service.get_data_object(
            self.database, self.collection, key_field=self.key_field, key_value=token
        )

        result = Token(**result)
        return result

    def add_user(self, user: User):
        d_service = self.data_service

        # Generate JWT for new user
        token = create_user_jwt(user)
        user.jwt = token

        result = d_service.add_data_object(
            self.database, self.collection, user.model_dump()
        )
        print(f"Added user: {result}")
        return result

    def update_user(self, user: User):
        d_service = self.data_service
        try:
            user_data = user.model_dump()
            user_update_result = d_service.update_data_object(
                self.database, self.collection, key_field=self.key_field, user_data=user_data
            )
            print(f"Updated user: {user_update_result}")
            return user_update_result

        except Exception as e:
            print(f"Error updating user or token: {e}")
            return None
