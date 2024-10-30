import logging

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic.json import pydantic_encoder
import json
from pydantic import BaseModel

from app.models.user import User
from app.models.token import Token
from app.resources.user_resource import UserResource
from app.services.service_factory import ServiceFactory

router = APIRouter()


class UpdateRequest(BaseModel):
    user: User
    token: Token


@router.get("/user_info/{id}", tags=["users"])
async def get_users(id: str) -> User:

    user_db = ServiceFactory.get_service("UserResource")
    result = user_db.get_by_key(id)
    return result

@router.post("/create_user", tags=["users"], status_code=status.HTTP_201_CREATED)
def create_user(request):
    # Get request
    user_data = request.dict()
    # Connect to DB
    user_db = ServiceFactory.get_service("UserResource")
    # Submit to DB
    result = user_db.create_user(user_data)
    # Return response code + JSON(user)
    if result:
        return result
    else:
        raise HTTPException(status_code=400, detail="User creation failed")


@router.post("/update_user", tags=["users"])
async def update_user(request: UpdateRequest):
    """Update User Information in the Database

    Currently only called by the composite service with the user and token
    it gets from the login service. This just has the information from
    Spotify, so we need to respond with the rest of the information
    """

    # TODO: Add logic here to update the database
    print(f"Updating user: {request}")
    # user = request.user
    # token = request.token
    # res = ServiceFactory.get_service("UserResource")
    # If the user is already in the database, update the user
    # If the user is not in the database, add the user
    # Return user with completed fields

    # TODO: res.update(user, token)
    return request.user


# TODO: update_app_user
# @router.post("/update_app_user", tags=["users"])
# def update_app_user(request) -> User:
#     # TODO: Get request
#     user_data = request.dict()
#     # Connect to DB
#     user_db = ServiceFactory.get_service("UserResource")
#     # Submit to DB
#     result = user_db.update_user(user_data)
#     # Return response code + JSON(user)
#     if result:
#         # TODO: 201
#     else:
#         raise HTTPException()