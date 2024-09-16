"""Made for dropping databases in Postgres"""

import os
from dotenv import load_dotenv
from psycopg import sql
import psycopg


load_dotenv()


def psycopg_connector():
    """Establish connection with database with Psycopg"""
    return psycopg.connect(
        host=os.getenv("POSTGRES"),
        hostaddr=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        dbname=os.getenv("POSTGRES_DB_NAME"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )


def drop_databases():
    """drops the databases"""

    conn = psycopg_connector()
    print("Connected to Postgres")

    conn.autocommit = True
    cursor = conn.cursor()
    print("Fetching databases")

    cursor.execute("SELECT datname FROM pg_database;")
    db_list = cursor.fetchall()
    cleaned_db_list = [db[0] for db in db_list]
    print("Fetched databases")

    if os.getenv("SENTINEL_DB_NAME") in cleaned_db_list:
        cursor.execute(
            sql.SQL(f"DROP DATABASE {os.getenv('SENTINEL_DB_NAME')} WITH (FORCE);")
        )
        print(f"{os.getenv('SENTINEL_DB_NAME')} dropped")
    if os.getenv("USER_DB_NAME") in cleaned_db_list:
        cursor.execute(
            sql.SQL(f"DROP DATABASE {os.getenv('USER_DB_NAME')} WITH (FORCE);")
        )
        print(f"{os.getenv('USER_DB_NAME')} dropped")

    cursor.close()
    conn.close()

    print("Done")


drop_databases()
