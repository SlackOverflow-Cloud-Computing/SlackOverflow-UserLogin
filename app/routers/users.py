from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.models.user import User  # CourseSection
from app.resources.user_resource import UserResource  # CourseResource
from app.services.service_factory import ServiceFactory

router = APIRouter()


class LoginRequest(BaseModel):
    auth_code: str


@router.get("/user_info/{user_id}", tags=["users"])
async def get_users(id: str) -> User:

    # TODO Do lifecycle management for singleton resource
    res = ServiceFactory.get_service("UserResource")
    result = res.get_by_key(id)
    return result


@router.post("/login", tags=["users"])
async def login(request: LoginRequest):
    """Uses Spotify Auth Code to Login User

    Gets login service and sends authorization code to Spotify service
    The service returns a user model, and this should save it to the database
    """

    auth_code = request.auth_code
    spotify = ServiceFactory.get_service("Login")
    database = ServiceFactory.get_service("UserResourceDataService")

    try:
        user = spotify.get_user_info(auth_code)
        print(f"Got info: {user}")
        if not user:
            print(f"Error for request: {request}")
            raise HTTPException(status_code=400, detail="Spotify Login Failed")

        # if user and user not in database: # Eventually add ability to save to database
        #     database.add(user)

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error during login")


""" @router.get("/courses_sections/{course_id}", tags=["users"])
async def get_courses(course_id: str) -> CourseSection:

    # TODO Do lifecycle management for singleton resource
    res = ServiceFactory.get_service("CourseResource")
    result = res.get_by_key(course_id)
    return result"""
