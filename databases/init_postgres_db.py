"""Collection of instruction to build database structure in Postgresql"""

import os
from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base
from databases.init_sentineldb import create_sentineldb_tables
from databases.init_userdb import create_userdb_tables
from databases.postgres_tools import PostgresTools


load_dotenv()
Base = declarative_base()


class InitPostgresDBs:
    """Initialize the databases and tables using SQLAlchemy."""

    def create_dbs(self=None):
        """Create the databases and tables."""

        engine = PostgresTools.db_connector(dbname=os.getenv("POSTGRES_DB_NAME"))
        conn = engine.connect()

        conn.execute("commit")

        existing_dbs = [
            db[0] for db in conn.execute("SELECT datname FROM pg_database;")
        ]

        if os.getenv("SENTINEL_DB_NAME") not in existing_dbs:
            conn.execute(f"CREATE DATABASE {os.getenv('SENTINEL_DB_NAME')}")
        if os.getenv("USER_DB_NAME") not in existing_dbs:
            conn.execute(f"CREATE DATABASE {os.getenv('USER_DB_NAME')}")

        conn.close()

        create_userdb_tables()
        create_sentineldb_tables()
