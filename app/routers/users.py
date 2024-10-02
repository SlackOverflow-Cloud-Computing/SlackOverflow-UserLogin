from fastapi import APIRouter

from app.models.user import UserLogin  # CourseSection
from app.resources.user_resource import UserLoginResource  # CourseResource
from app.services.service_factory import ServiceFactory

router = APIRouter()


@router.get("/user/{user_id}", tags=["users"])
async def get_users(user_id: str) -> UserLogin:

    # TODO Do lifecycle management for singleton resource
    res = ServiceFactory.get_service("UserLoginResource")
    result = res.get_by_key(user_id)
    return result

""" @router.get("/courses_sections/{course_id}", tags=["users"])
async def get_courses(course_id: str) -> CourseSection:

    # TODO Do lifecycle management for singleton resource
    res = ServiceFactory.get_service("CourseResource")
    result = res.get_by_key(course_id)
    return result"""


