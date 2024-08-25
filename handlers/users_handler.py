"""Users handler module."""

import psycopg  # type: ignore
from db_config.postgres import Postgres


class UsersHandler:
    """Users handler class."""

    def query_usersdb(self, query):
        """Get all users."""
        try:
            connection = Postgres().userdb_connector()
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    results = cursor.fetchall()
                    return results

        except psycopg.OperationalError as e:
            error_message = f"<p>Error: {e}</p>"
            return error_message

        finally:
            connection.close()
