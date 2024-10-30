import logging

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.models.user import User
from app.models.token import Token
from app.resources.user_resource import UserResource
from app.services.service_factory import ServiceFactory
from datetime import datetime

router = APIRouter()


class UpdateRequest(BaseModel):
    user: User
    token: Token


@router.get("/user_info/{user_id}", tags=["users"])
async def get_users(user_id: str) -> User:
    res = ServiceFactory.get_service("UserResource")
    result = res.get_by_key(user_id)
    return result

@router.get("/user_info/{token}", tags=["users"])
async def get_token(token: str) -> Token:
    res = ServiceFactory.get_service("TokenResource")
    result = res.get_by_key(token)
    return result


@router.post("/create_user", tags=["users"], status_code=status.HTTP_201_CREATED)
def create_user(request: UpdateRequest):
    user_db = ServiceFactory.get_service("UserResource")
    try:
        result = user_db.get_by_key(request.user.id)
        if result:
            print(f"User already exists: {result}")
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists.")
        else:
            print(f"User does not exist, adding user: {request.user}")
            user_db.add_user(request.user)
            return {"message": "User created successfully", "user": request.user.dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/update_user", tags=["users"], status_code=status.HTTP_202_ACCEPTED)
async def update_user(request: UpdateRequest):
    print(f"Updating user: {request}")
    user_db = ServiceFactory.get_service("UserResource")

    try:
        existing_user = user_db.get_by_key(request.user.id)
        if existing_user:
            print(f"User already exists: {existing_user}")
            request.user.created_at = existing_user.created_at
            request.user.last_login = datetime.now()
            user_db.update_user(request.user)
        else:
            print(f"User does not exist, adding user: {request.user}")
            user_db.add_user(request.user)

        updated_user = user_db.get_by_key(request.user.id)
        return updated_user

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
