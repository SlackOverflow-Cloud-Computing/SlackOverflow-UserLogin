import logging
from typing_extensions import Optional

import jwt
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from app.models.user import User
from app.models.spotify_token import SpotifyToken
from app.resources.user_resource import JWT_SECRET, UserResource
from app.services.service_factory import ServiceFactory
from datetime import datetime

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class UpdateRequest(BaseModel):
    user: User
    token: SpotifyToken


@router.get("/users/{user_id}", tags=["users"])
async def get_user(user_id: str, token: str = Depends(oauth2_scheme)) -> User:
    res = ServiceFactory.get_service("UserResource")

    if not res.validate_token(token, scope=("/users/{user_id}", "GET")):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    result = res.get_by_key(user_id)

    # Block out private information - probably a better way to do this
    if user_id != res.get_user_id(token):
        result.jwt = None
        result.email = ""
        result.country = ""
        result.created_at = None
        result.last_login = None

    return result


@router.put("/users/{user_id}", tags=["users"], status_code=status.HTTP_202_ACCEPTED)
async def update_user(user_id: str, request: UpdateRequest, token:str = Depends(oauth2_scheme)):
    print(f"Updating user: {request}")
    user_db = ServiceFactory.get_service("UserResource")

    if not user_db.validate_token(token, user_id, scope=("/users/{user_id}", "PUT")):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    try:
        existing_user = user_db.get_by_key(request.user.id)
        if existing_user:
            print(f"User already exists: {existing_user}")
            request.user.last_login = datetime.now()
            user_db.update_user(request.user)
        else:
            print(f"User does not exist, adding user: {request.user}")
            return user_db.add_user(request.user)

        updated_user = user_db.get_by_key(request.user.id)
        return updated_user

    except Exception as e:
        # raise nested exception instead of generic 500
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/users/{user_id}/spotify_token", tags=["users"])
async def get_spotify_token(user_id: str, token: str = Depends(oauth2_scheme)) -> SpotifyToken:
    """Use a User ID to get a user's Spotify token."""
    res = ServiceFactory.get_service("UserResource")

    if not res.validate_token(token, scope=("/users/{user_id}/spotify_token", "GET")):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    result = res.get_spotify_by_token(user_id)
    return result


@router.post("/users", tags=["users"], status_code=status.HTTP_201_CREATED)
def create_user(request: UpdateRequest):
    user_db = ServiceFactory.get_service("UserResource")
    try:
        result = user_db.get_by_key(request.user.id)
        if result:
            print(f"User already exists: {result}")
            # raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists.")
            # I commented this out because the composite expects the up to date user object
            return {"message": "User already exists", "user": result.dict()}
        else:
            if request.user.created_at is None:
                request.user.created_at = datetime.now()
            print(f"User does not exist, adding user: {request.user}")
            user_db.add_user(request.user)
            user_db.add_spotify_token(request.user, request.token)
            return {"message": "User created successfully", "user": request.user.dict()}
    except Exception as e:
        # raise nested exception instead of generic 500
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))
