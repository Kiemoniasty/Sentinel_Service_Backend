"""Postgres tools that can be used in none specific tasks"""

import os
import psycopg
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv(override=True)


class PostgresTools:
    """Universal Postgresql tools"""

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

    def userdb_connector(self=None):
        """Establish connection with user database"""
        return psycopg.connect(
            host=os.getenv("POSTGRES"),
            hostaddr=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            dbname=os.getenv("USER_DB_NAME"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
        )

    def db_connector(self=None, dbname=None):
        """Establish a connection with the database."""

        user = os.getenv("POSTGRES_USER")
        password = os.getenv("POSTGRES_PASSWORD")
        host = os.getenv("POSTGRES_HOST")
        port = os.getenv("POSTGRES_PORT")

        return create_engine(f"postgresql://{user}:{password}@{host}:{port}/{dbname}")
