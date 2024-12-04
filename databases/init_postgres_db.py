"""Collection of instruction to build database structure in Postgresql"""

import os
from dotenv import load_dotenv
from psycopg import sql
import psycopg

# from databases.init_sentineldb import create_sentineldb_tables
# from databases.init_userdb import create_userdb_tables
import constants
from databases.influxdb_tools import InfluxTools
from databases.postgres_tools import PostgresTools


load_dotenv()


class InitPostgresDBs:
    """Initialize the databases and tables using SQLAlchemy."""

    def create_dbs(self=None):
        """Create the databases and tables."""
        InfluxTools.write_log(constants.INIT_PG)

        conn = PostgresTools.psycopg_connector(dbname=os.getenv("POSTGRES_DB_NAME"))
        conn.autocommit = True
        cursor = conn.cursor()

        InfluxTools.write_log(constants.PG_CONN)

        cursor.execute("SELECT datname FROM pg_database;")
        db_list = cursor.fetchall()
        cleaned_db_list = [db[0] for db in db_list]

        InfluxTools.write_log(constants.PG_FETCHED)

        if os.getenv("SENTINEL_DB_NAME") not in cleaned_db_list:
            cursor.execute(sql.SQL(f"CREATE DATABASE {os.getenv('SENTINEL_DB_NAME')};"))

            InfluxTools.write_log(constants.SENDB_CREATED)
        else:
            InfluxTools.write_log(constants.SENDB_EXISTS)

        if os.getenv("USER_DB_NAME") not in cleaned_db_list:
            cursor.execute(sql.SQL(f"CREATE DATABASE {os.getenv('USER_DB_NAME')};"))

            InfluxTools.write_log(constants.USRDB_CREATED)
        else:
            InfluxTools.write_log(constants.USRDB_EXISTS)

        cursor.close()
        conn.close()

        InfluxTools.write_log(constants.PG_CLOSED)
