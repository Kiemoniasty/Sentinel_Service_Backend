"""Postgres tools that can be used in none specific tasks"""

import os
import psycopg
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv(override=True)


class PostgresTools:
    """Universal Postgresql tools"""

    def psycopg_connector(self=None, dbname=None):
        """Establish connection with database with Psycopg"""
        return psycopg.connect(
            host=os.getenv("POSTGRES"),
            hostaddr=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            dbname=dbname,
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
        )

    def sqlalchemy_connector(self=None, dbname=None):
        """Establish a connection with the database via SQLAlchemy."""

        user = os.getenv("POSTGRES_USER")
        password = os.getenv("POSTGRES_PASSWORD")
        host = os.getenv("POSTGRES_HOST")
        port = os.getenv("POSTGRES_PORT")

        return create_engine(f"postgresql://{user}:{password}@{host}:{port}/{dbname}")
