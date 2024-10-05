from typing import Any

from framework.resources.base_resource import BaseResource

from app.models.user import User
from app.services.service_factory import ServiceFactory


class UserResource(BaseResource):  # CourseResource

    def __init__(self, config):
        super().__init__(config)

        # TODO -- Replace with dependency injection.
        #
        self.data_service = ServiceFactory.get_service("UserResourceDataService")
        self.database = "user_db"
        self.collection = "user_info"  # "course_sections"
        self.key_field = "id"  # "sis_course_id"

    def get_by_key(self, key: str) -> User:

        d_service = self.data_service

        result = d_service.get_data_object(
            self.database, self.collection, key_field=self.key_field, key_value=key
        )

        result = User(**result)
        return result
