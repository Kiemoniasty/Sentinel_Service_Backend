"""Postgres Database Connection Handlers"""

import psycopg
import env.postgres_env as env


class Postgres:
    """Postgres connection handlers"""

    def sentineldb_connector(self=None):
        """Establish connection with sentinel database"""

        return psycopg.connect(
            host=env.POSTGRES,
            hostaddr=env.POSTGRES_HOST,
            port=env.POSTGRES_PORT,
            dbname=env.SENTINEL_DB_NAME,
            user=env.POSTGRES_USER,
            password=env.POSTGRES_PASSWORD,
        )

    def userdb_connector(self):
        """Establish connection with user database"""
        return psycopg.connect(
            host=env.POSTGRES,
            hostaddr=env.POSTGRES_HOST,
            port=env.POSTGRES_PORT,
            dbname=env.USER_DB_NAME,
            user=env.POSTGRES_USER,
            password=env.POSTGRES_PASSWORD,
        )
