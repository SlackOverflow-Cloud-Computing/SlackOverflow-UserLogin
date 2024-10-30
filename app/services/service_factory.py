from framework.services.service_factory import BaseServiceFactory
import app.resources.user_resource as user_resource
from framework.services.data_access.MySQLRDBDataService import MySQLRDBDataService
import dotenv, os

dotenv.load_dotenv()
user = os.getenv('DB_USER')
password = os.getenv('DB_PASS')
host = os.getenv('DB_HOST')
port = int(os.getenv('DB_PORT'))

print(user)
print(host)

class ServiceFactory(BaseServiceFactory):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_service(cls, service_name):

        match service_name:
            case 'UserResource':
                result = user_resource.UserResource(config=None)
            case 'UserResourceDataService':
                context = dict(user=user, password=password, host=host, port=port)
                data_service = MySQLRDBDataService(context=context)
                result = data_service
            case 'TokenResource':
                context = dict(user=user, password=password, host=host, port=port)
                data_service = MySQLRDBDataService(context=context)
                result = data_service
            case _:
                result = None

        return result
