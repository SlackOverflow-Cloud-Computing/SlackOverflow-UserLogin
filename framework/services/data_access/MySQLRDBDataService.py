import pymysql
from .BaseDataService import DataDataService


class MySQLRDBDataService(DataDataService):
    """
    A generic data service for MySQL databases. The class implement common
    methods from BaseDataService and other methods for MySQL. More complex use cases
    can subclass, reuse methods and extend.
    """

    def __init__(self, context):
        super().__init__(context)

    def _get_connection(self):
        connection = pymysql.connect(
            host=self.context["host"],
            port=self.context["port"],
            user=self.context["user"],
            passwd=self.context["password"],
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        return connection

    def get_data_object(self,
                        database_name: str,
                        collection_name: str,
                        key_field: str,
                        key_value: str):
        """
        See base class for comments.
        """

        connection = None
        result = None

        try:
            sql_statement = f"SELECT * FROM {database_name}.{collection_name} " + \
                        f"where {key_field}=%s"
            connection = self._get_connection()
            cursor = connection.cursor()
            cursor.execute(sql_statement, [key_value])
            result = cursor.fetchone()
        except Exception as e:
            if connection:
                connection.close()

        return result

    # TODO: Insert a new user into DB
    def create_data_object(self,
                        database_name: str,
                        collection_name: str,
                        key_field: str,
                        user_data: dict):
        """
        See base class for comments.
        """

        connection = None
        result = None

        try:
            # Parse user data
            columns = ", ".join(user_data.keys())
            placeholders = ", ".join(["%s"] * len(user_data))
            values = list(user_data.values())

            # Insert a user
            sql_statement = f"INSERT INTO {database_name}.{collection_name} ({columns}) VALUES ({placeholders})"

            connection = self._get_connection()
            cursor = connection.cursor()

            # Execute the insert operation
            cursor.execute(sql_statement, values)
            connection.commit()

            # Retrieve the inserted record to confirm creation
            cursor.execute(f"SELECT * FROM {database_name}.{collection_name} WHERE {key_field} = %s",
                           [user_data[key_field]])
            result = cursor.fetchone()

        except Exception as e:
            print(f"Error inserting data: {e}")
            if connection:
                connection.rollback()  # Rollback in case of error
        finally:
            if connection:
                connection.close()
        return result

    # TODO: Update the user into DB
    def update_data_object(self,
                        database_name: str,
                        collection_name: str,
                        key_field: str,
                        user_data: dict):
        """
        See base class for comments.
        """

        connection = None
        result = None

        try:
            # Optional:Parse user data
            key_value = user_data['id']

            # TODO: SQL - update a user
            sql_statement = f"SELECT * FROM {database_name}.{collection_name} " + \
                        f"where {key_field}=%s"

            connection = self._get_connection()
            cursor = connection.cursor()
            cursor.execute(sql_statement, [key_value])
            result = cursor.fetchone()
        except Exception as e:
            if connection:
                connection.close()

        return result







