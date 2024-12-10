import pymysql
from datetime import datetime
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

    def add_user_data_object(self, database_name: str, collection_name: str, data_object: dict):
        connection = None
        result = None

        try:
            data_object["created_at"] = datetime.now()
            data_object["last_login"] = datetime.now()
            sql_statement = f"INSERT INTO {database_name}.{collection_name} " + \
                f"({', '.join(data_object.keys())}) " + \
                f"VALUES ({', '.join(['%s'] * len(data_object))})"
            connection = self._get_connection()
            cursor = connection.cursor()
            cursor.execute(sql_statement, list(data_object.values()))
            result = cursor.fetchone()
        except Exception as e:
            if connection:
                connection.close()
            return e

        return result

    def add_spotify_data_object(self, database_name: str, collection_name: str, data_object: dict):
        connection = None
        result = None

        try:
            sql_statement = f"INSERT INTO {database_name}.{collection_name} " + \
                f"({', '.join(data_object.keys())}) " + \
                f"VALUES ({', '.join(['%s'] * len(data_object))})"
            connection = self._get_connection()
            cursor = connection.cursor()
            cursor.execute(sql_statement, list(data_object.values()))
            result = cursor.fetchone()
        except Exception as e:
            if connection:
                connection.close()
            return e

        return result

    def update_data_object(self, database_name: str, collection_name: str, key_field: str, user_data: dict):
        connection = None
        result = None

        try:
            key_value = user_data.pop(key_field)

            set_clause = ", ".join([f"{field} = %s" for field in user_data.keys()])
            sql_statement = f"UPDATE {database_name}.{collection_name} SET {set_clause} WHERE {key_field} = %s"

            connection = self._get_connection()
            cursor = connection.cursor()
            cursor.execute(sql_statement, list(user_data.values()) + [key_value])
            connection.commit()

            result = cursor.rowcount
            print(f"Updated {result} row(s).")

        except Exception as e:
            print(f"Error updating data object: {e}")
            if connection:
                connection.rollback()
        finally:
            if connection:
                connection.close()

        return result


