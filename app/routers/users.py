from fastapi import APIRouter

from app.models.user import User  # CourseSection
from app.resources.user_resource import UserResource  # CourseResource
from app.services.service_factory import ServiceFactory

router = APIRouter()


@router.get("/user_info/{user_id}", tags=["users"])
async def get_users(id: str) -> User:

    # TODO Do lifecycle management for singleton resource
    res = ServiceFactory.get_service("UserResource")
    result = res.get_by_key(id)
    return result


@router.get("/login/{authorization_code}", tags=["users"])
async def login(auth_code: str):
    """Uses Spotify Auth Code to Login User

    Gets login service and sends authorization code to Spotify service
    The service returns a user model, and this should save it to the database
    """

    print(f"Trying to login with {auth_code}")
    spotify = ServiceFactory.get_service("Login")
    database = ServiceFactory.get_service("UserResourceDataService")
    user = spotify.get_user_info(auth_code)
    print(f"Got info: {user}")

    # if user and user not in database: # Eventually add ability to save to database
    #     database.add(user)


""" @router.get("/courses_sections/{course_id}", tags=["users"])
async def get_courses(course_id: str) -> CourseSection:

    # TODO Do lifecycle management for singleton resource
    res = ServiceFactory.get_service("CourseResource")
    result = res.get_by_key(course_id)
    return result"""
