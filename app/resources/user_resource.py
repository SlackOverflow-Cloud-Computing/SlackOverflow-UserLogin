from typing import Any, Optional
from datetime import datetime, timedelta
import dotenv,os
import logging

import jwt

from framework.resources.base_resource import BaseResource
from app.models.user import User
from app.models.spotify_token import SpotifyToken
from app.services.service_factory import ServiceFactory

dotenv.load_dotenv()
db = os.getenv('DB_NAME')
collection = os.getenv('DB_COLLECTION')

logger = logging.getLogger("uvicorn")

# JWT Info
JWT_SECRET = os.getenv('JWT_SECRET')
ALGORITHM = "HS256"
MINUTES_TO_EXPIRATION = 60


def create_user_jwt(user: User, cid: str) -> str:
    """Create a JWT token with the given data.

    Data should be a dictionary with the info to be stored in the token.
    For us this will be the user's Spotify ID and scopes.
    """
    
    logger.info(f"Creating JWT - [{cid}]")

    def default_scopes(id):
        scopes = {
            "/auth/login": ["POST"],

            "/users/{user_id}/playlists": ["GET", "POST"],
            "/users/{user_id}": ["GET", "PUT"],
            "/users/{user_id}/spotify_token": ["GET", "PUT"],
            "/users/{user_id}/refreshed_token": ["GET"],

            "/playlists/{playlist_id}": ["GET", "POST", "DELETE"],
            "/playlists/{playlist_id}/tracks/{track_id}": ["DELETE"],

            "/songs": ["GET"],
            "/songs/{song_id}": ["GET"],

            "/recommendations": ["GET"],
            "/recommendations/playlist": ["GET"],

            "/chats": ["POST"],
            "/chat_info/{chat_id}": ["GET"],
            "/chat_details/{message_id}": ["GET"],
            "/chat_history": ["GET"],
            "/update_chat": ["POST"],
            "general_chat": ["GET"]
        }
        return scopes

    data = {
        "sub": user.id,
        "iat": datetime.utcnow(),
        "scopes": default_scopes(user.id)
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

    def validate_token(self, token: str, id: Optional[str]=None, scope: Optional[tuple[str, str]]=None) -> bool:
        """Validate a JWT token.

        Optionally checks that the token belongs to a specific user and
        that the token has the required scope for the endpoint.
        Scope is of the form ("/endpoint", "METHOD").
        """
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
            if id is not None and payload.get("sub") != id:
                return False
            if scope is not None and scope[1] not in payload.get("scopes").get(scope[0]):
                return False
            return True

        except jwt.exceptions.InvalidTokenError:
            return False

    def get_user_id(self, token: str, cid: str) -> Optional[str]:
        """Get the user ID from a JWT token."""
        logger.info(f"Getting user ID from token {token} - [{cid}]")
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
            return payload.get("sub")
        except jwt.exceptions.InvalidTokenError:
            logger.error(f"Invalid token: {token} - [{cid}]")
            return None

    def get_by_key(self, key: str, cid: str) -> User:
        logger.info(f"Getting user by key: {key} - [{cid}]")
        d_service = self.data_service

        result = d_service.get_data_object(
            self.database, self.collection, key_field=self.key_field, key_value=key
        )
        if result:
            result = User(**result)
        return result

    def get_spotify_by_token(self, token: str, cid: str) -> SpotifyToken:
        logger.info(f"Getting spotify token by token: {token} - [{cid}]")
        d_service = self.data_service

        result = d_service.get_data_object(
            self.database, self.token_collection, key_field=self.key_field, key_value=token
        )

        result = SpotifyToken(**result)
        return result
    
    def update_spotify_token(self, token: SpotifyToken, cid: str):
        logger.info(f"Updating user's spotify token: {token} - [{cid}]")
        d_service = self.data_service
        try:
            token = token.model_dump()
            user_update_result = d_service.update_data_object(
                self.database, self.token_collection, key_field=self.key_field, user_data=token
            )
            logger.info(f"Updated user's spotify token: {user_update_result}")
            return user_update_result

        except Exception as e:
            logger.error(f"Error updating user or token: {e} - [{cid}]")
            return None

    def add_user(self, user: User, cid: str):
        logger.info(f"Adding user: {user} - [{cid}]")
        d_service = self.data_service

        # Generate JWT for new user
        token = create_user_jwt(user, cid)
        user.jwt = token
        logger.info(f"Generated JWT: {token} - [{cid}]")

        result = d_service.add_user_data_object(
            self.database, self.collection, user.model_dump()
        )
        logger.info(f"Added user: {result} - [{cid}]")
        return result

    def add_spotify_token(self, user: User, token: SpotifyToken, cid: str):
        logger.info(f"Adding spotify token: {token} - [{cid}]")
        d_service = self.data_service

        info = token.model_dump()
        info[self.key_field] = user.id

        result = d_service.add_spotify_data_object(
            self.database, self.token_collection, info
        )
        logger.info(f"Added token: {result} - [{cid}]")
        return result

    def update_user(self, user: User, cid: str):
        logger.info(f"Updating user: {user} - [{cid}]")
        d_service = self.data_service
        try:
            user_data = user.model_dump()
            user_update_result = d_service.update_data_object(
                self.database, self.collection, key_field=self.key_field, user_data=user_data
            )
            logger.info(f"Updated user: {user_update_result}")
            return user_update_result

        except Exception as e:
            logger.error(f"Error updating user or token: {e} - [{cid}]")
            return None
