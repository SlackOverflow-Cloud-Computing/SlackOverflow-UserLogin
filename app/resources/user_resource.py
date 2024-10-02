from typing import Any

from framework.resources.base_resource import BaseResource

from app.models.user import UserLogin  # CourseSection
from app.services.service_factory import ServiceFactory


class UserLoginResource(BaseResource):  # CourseResource

    def __init__(self, config):
        super().__init__(config)

        # TODO -- Replace with dependency injection.
        #
        self.data_service = ServiceFactory.get_service("UserLoginResourceDataService")  # "CourseResourceDataService"
        self.database = "p1_database"
        self.collection = "user_login_tb"  # "course_sections"
        self.key_field = "user_id"  # "sis_course_id"

    def get_by_key(self, key: str) -> UserLogin:

        d_service = self.data_service

        result = d_service.get_data_object(
            self.database, self.collection, key_field=self.key_field, key_value=key
        )

        result = UserLogin(**result)
        return result


