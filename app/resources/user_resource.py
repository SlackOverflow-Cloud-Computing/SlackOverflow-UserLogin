from typing import Any

from framework.resources.base_resource import BaseResource

from app.models.user import User
from app.services.service_factory import ServiceFactory
import dotenv, os

dotenv.load_dotenv()
db = os.getenv('DB_NAME')
collection = os.getenv('DB_COLLECTION')


class UserResource(BaseResource):

    def __init__(self, config):
        super().__init__(config)

        self.data_service = ServiceFactory.get_service("UserResourceDataService")
        self.database = db
        self.collection = collection
        self.key_field = "id"

    def get_by_key(self, key: str) -> User:

        d_service = self.data_service

        result = d_service.get_data_object(
            self.database, self.collection, key_field=self.key_field, key_value=key
        )

        result = User(**result)
        return result
