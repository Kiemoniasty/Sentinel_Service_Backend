"""Collection of instruction to build database structure in Postgresql"""

import os
from dotenv import load_dotenv
from psycopg import sql

# from databases.init_sentineldb import create_sentineldb_tables
# from databases.init_userdb import create_userdb_tables
from databases.postgres_tools import PostgresTools


load_dotenv()


class InitPostgresDBs:
    """Initialize the databases and tables using SQLAlchemy."""

    def create_dbs(self=None):
        """Create the databases and tables."""
        print("Starting initialization")
        conn = PostgresTools.psycopg_connector(dbname=os.getenv("POSTGRES_DB_NAME"))
        conn.autocommit = True
        cursor = conn.cursor()
        print("Connected to Postgres")

        cursor.execute("SELECT datname FROM pg_database;")
        db_list = cursor.fetchall()
        cleaned_db_list = [db[0] for db in db_list]

        print("Fetched databases")
        if os.getenv("SENTINEL_DB_NAME") not in cleaned_db_list:
            cursor.execute(sql.SQL(f"CREATE DATABASE {os.getenv('SENTINEL_DB_NAME')};"))
            print(f"{os.getenv('SENTINEL_DB_NAME')} created")
            # create_sentineldb_tables()
        else:
            print("Sentinel database already exists")
        if os.getenv("USER_DB_NAME") not in cleaned_db_list:
            cursor.execute(sql.SQL(f"CREATE DATABASE {os.getenv('USER_DB_NAME')};"))
            print(f"{os.getenv('USER_DB_NAME')} created")
            # create_userdb_tables()
        else:
            print("User database already exists")

        cursor.close()
        conn.close()
        print("Connection closed")
