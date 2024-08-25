"""Postgres Database Connection Handlers"""

import os
import psycopg  # type: ignore
from dotenv import load_dotenv  # type: ignore

load_dotenv()


class Postgres:
    """Postgres connection handlers"""

    def sentineldb_connector(self=None):
        """Establish connection with sentinel database"""

        return psycopg.connect(
            host=os.getenv("POSTGRES"),
            hostaddr=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            dbname=os.getenv("SENTINEL_DB_NAME"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
        )

    def userdb_connector(self):
        """Establish connection with user database"""
        return psycopg.connect(
            host=os.getenv("POSTGRES"),
            hostaddr=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            dbname=os.getenv("USER_DB_NAME"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
        )
