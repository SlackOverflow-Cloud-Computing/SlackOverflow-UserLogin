from framework.services.service_factory import BaseServiceFactory
import app.resources.user_resource as user_resource  # course_resource
from framework.services.data_access.MySQLRDBDataService import MySQLRDBDataService
from app.services.login import LoginService


# TODO -- Implement this class
class ServiceFactory(BaseServiceFactory):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_service(cls, service_name):
        #
        # TODO -- The terrible, hardcoding and hacking continues.
        #

        match service_name:
            case 'UserResource':
                result = user_resource.UserResource(config=None)
            case 'UserResourceDataService':
                context = dict(user="admin", password="slackOverflowDB",
                            host="database-1.ccjxezwbfect.us-east-1.rds.amazonaws.com", port=3306)
                data_service = MySQLRDBDataService(context=context)
                result = data_service
            case "Login":
                url = "http://127.0.0.1:8080"
                result = LoginService(url)

            case _:
                result = None

        return result
