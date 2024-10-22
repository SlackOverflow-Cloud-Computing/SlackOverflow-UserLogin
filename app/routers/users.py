import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.models.user import User
from app.models.token import Token
from app.resources.user_resource import UserResource
from app.services.service_factory import ServiceFactory

router = APIRouter()


class UpdateRequest(BaseModel):
    user: User
    token: Token


@router.get("/user_info/{user_id}", tags=["users"])
async def get_users(id: str) -> User:

    res = ServiceFactory.get_service("UserResource")
    result = res.get_by_key(id)
    return result

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
