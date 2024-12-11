import logging
from typing_extensions import Optional

import jwt
from fastapi import APIRouter, HTTPException, status, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import logging

from app.models.user import User
from app.models.spotify_token import SpotifyToken
from app.resources.user_resource import JWT_SECRET, UserResource
from app.services.service_factory import ServiceFactory
from datetime import datetime

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

logger = logging.getLogger("uvicorn")


class UpdateRequest(BaseModel):
    user: User
    token: SpotifyToken


@router.get("/users/{user_id}", tags=["users"])
async def get_user(user_id: str, request: Request, token: str = Depends(oauth2_scheme)) -> User:
    """Get a user by their user id."""
    cid = request.headers.get("X-Correlation-ID")
    res = ServiceFactory.get_service("UserResource")

    if not res.validate_token(token, scope=("/users/{user_id}", "GET")):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    result = res.get_by_key(user_id, cid)

    # Block out private information - probably a better way to do this
    if user_id != res.get_user_id(token, cid):
        result.jwt = None
        result.email = ""
        result.country = ""
        result.created_at = None
        result.last_login = None

    return result


@router.put("/users/{user_id}", tags=["users"], status_code=status.HTTP_202_ACCEPTED)
async def update_user(user_id: str, update_request: UpdateRequest, request: Request, token:str = Depends(oauth2_scheme)):
    """Updates a user."""
    cid = request.headers.get("X-Correlation-ID")
    logger.info(f"Updating user: {update_request} - [{cid}]")
    user_db = ServiceFactory.get_service("UserResource")

    if not user_db.validate_token(token, user_id, scope=("/users/{user_id}", "PUT")):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    try:
        existing_user = user_db.get_by_key(update_request.user.id, cid)
        if existing_user:
            logger.info(f"User already exists: {existing_user} - [{cid}]")
            update_request.user.last_login = datetime.now()
            user_db.update_user(update_request.user, cid)
        else:
            logger.info(f"User does not exist, adding user: {update_request.user} - [{cid}]")
            return user_db.add_user(update_request.user, cid)

        updated_user = user_db.get_by_key(update_request.user.id, cid)
        return updated_user

    except Exception as e:
        # raise nested exception instead of generic 500
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/users/{user_id}/spotify_token", tags=["users"])
async def get_spotify_token(user_id: str, request: Request, token: str = Depends(oauth2_scheme)) -> SpotifyToken:
    """Use a User ID to get a user's Spotify token."""
    cid = request.headers.get("X-Correlation-ID")
    res = ServiceFactory.get_service("UserResource")

    if not res.validate_token(token, scope=("/users/{user_id}/spotify_token", "GET")):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    result = res.get_spotify_by_token(user_id, cid)
    return result

@router.put("/users/{user_id}/spotify_token", tags=["users"])
async def update_spotify_token(user_id: str, spotify_token: SpotifyToken, request: Request, token: str = Depends(oauth2_scheme)):
    """Update user's Spotify token."""
    cid = request.headers.get("X-Correlation-ID")
    res = ServiceFactory.get_service("UserResource")

    if not res.validate_token(token, scope=("/users/{user_id}/spotify_token", "PUT")):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    result = res.update_spotify_token(spotify_token, cid)
    return result


@router.post("/users", tags=["users"], status_code=status.HTTP_201_CREATED)
def create_user(update_request: UpdateRequest, request: Request):
    """Creates a user."""
    cid = request.headers.get("X-Correlation-ID")
    user_db = ServiceFactory.get_service("UserResource")
    try:
        result = user_db.get_by_key(update_request.user.id, cid)
        if result:
            logger.info(f"User already exists: {result} - [{cid}]")
            # raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists.")
            # I commented this out because the composite expects the up to date user object
            return {"message": "User already exists", "user": result.dict()}
        else:
            if update_request.user.created_at is None:
                update_request.user.created_at = datetime.now()
            logger.info(f"User does not exist, adding user: {update_request.user} - [{cid}]")
            user_db.add_user(update_request.user, cid)
            user_db.add_spotify_token(update_request.user, update_request.token, cid)
            return {"message": "User created successfully", "user": update_request.user.dict()}
    except Exception as e:
        # raise nested exception instead of generic 500
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))
