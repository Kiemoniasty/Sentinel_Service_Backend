"""Made for dropping databases in Postgres"""

import os
from uuid import UUID
from dotenv import load_dotenv
from influxdb_client import InfluxDBClient
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


def infux_connector():
    """Establish connection with InfluxDB"""
    influxdb_url = os.getenv("INFLUXDB_URL")
    influxdb_token = os.getenv("INFLUXDB_TOKEN")
    influxdb_org = os.getenv("INFLUXDB_ORG")

    return InfluxDBClient(url=influxdb_url, token=influxdb_token, org=influxdb_org)


def is_uuid4(value):
    """
    Validate if the given string is a valid UUID4.
    """
    try:
        uuid_obj = UUID(value, version=4)
        return str(uuid_obj) == value
    except ValueError:
        return False


def delete_uuid_buckets():
    """
    Query all buckets and delete those whose names are valid UUID4.
    """
    client = infux_connector()
    buckets_api = client.buckets_api()
    all_buckets = buckets_api.find_buckets().buckets

    for bucket in all_buckets:
        bucket_name = bucket.name
        if is_uuid4(bucket_name) | (bucket_name == "app_logs"):
            print(f"Deleting bucket: {bucket_name}")
            buckets_api.delete_bucket(bucket)
        else:
            print(f"Skipping bucket: {bucket_name} (not UUID4)")


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


delete_uuid_buckets()
drop_databases()
