"""Collection of instruction to build database structure in Postgresql"""

import os
from dotenv import load_dotenv
import psycopg
from psycopg import sql

load_dotenv()


class InitPostgresDBs:
    """Initialize the databases and tables."""

    def db_connector(self, dbname):
        """Establish connection with the database."""
        return psycopg.connect(
            host=os.getenv("POSTGRES"),
            hostaddr=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            dbname=dbname,
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
        )

    def create_dbs(self=None):
        """Create the databases."""

        conn = InitPostgresDBs.db_connector(self, os.getenv("POSTGRES_DB_NAME"))
        conn.autocommit = True
        cursor = conn.cursor()

        cursor.execute("SELECT datname FROM pg_database;")
        db_list = cursor.fetchall()
        cleaned_db_list = [db[0] for db in db_list]

        if os.getenv("SENTINEL_DB_NAME") not in cleaned_db_list:
            cursor.execute(sql.SQL(f"CREATE DATABASE {os.getenv('SENTINEL_DB_NAME')}"))
        if os.getenv("USER_DB_NAME") not in cleaned_db_list:
            cursor.execute(sql.SQL(f"CREATE DATABASE {os.getenv('USER_DB_NAME')}"))

        cursor.close()
        conn.close()
        InitPostgresDBs.create_users_tables()
        InitPostgresDBs.create_sentinel_tables()

    def create_users_tables(self=None):
        """Create the tables."""
        conn = InitPostgresDBs.db_connector(self, dbname=os.getenv("USER_DB_NAME"))
        conn.autocommit = True
        cursor = conn.cursor()

        cursor.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
        )
        table_list = cursor.fetchall()
        cleaned_table_list = [db[0] for db in table_list]

        if "account_type" not in cleaned_table_list:
            cursor.execute(
                """CREATE TABLE account_type (
                    guid UUID PRIMARY KEY,
                    account_type VARCHAR(255) NOT NULL
                    );"""
            )

        if "account_status" not in cleaned_table_list:
            cursor.execute(
                """CREATE TABLE account_status (
                    guid UUID PRIMARY KEY,
                    is_active BOOLEAN NOT NULL
                    );"""
            )

        if "users" not in cleaned_table_list:
            cursor.execute(
                """CREATE TABLE users (
                    guid UUID PRIMARY KEY,
                    login VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    phone_number INTEGER,
                    account_type UUID,
                    is_active UUID,
                    FOREIGN KEY (account_type) REFERENCES account_type(guid),
                    FOREIGN KEY (is_active) REFERENCES account_status(guid)
                );"""
            )

        cursor.close()
        conn.close()

    def create_sentinel_tables(self=None):
        """Create the tables."""
        conn = InitPostgresDBs.db_connector(self, dbname=os.getenv("SENTINEL_DB_NAME"))
        conn.autocommit = True
        cursor = conn.cursor()

        cursor.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
        )
        table_list = cursor.fetchall()
        cleaned_table_list = [db[0] for db in table_list]

        if "service_statuses" not in cleaned_table_list:
            cursor.execute(
                """CREATE TABLE service_statuses (
                    GUID UUID PRIMARY KEY,
                    Name VARCHAR(255) NOT NULL
                );"""
            )

        if "logger_messages" not in cleaned_table_list:
            cursor.execute(
                """CREATE TABLE logger_messages (
                    GUID UUID PRIMARY KEY,
                    Content VARCHAR(255) NOT NULL
                );"""
            )

        if "error_codes" not in cleaned_table_list:
            cursor.execute(
                """CREATE TABLE error_codes (
                    GUID UUID PRIMARY KEY,
                    code VARCHAR(50) NOT NULL
                );"""
            )

        if "notification_messages" not in cleaned_table_list:
            cursor.execute(
                """CREATE TABLE notification_messages (
                    GUID UUID PRIMARY KEY,
                    Content VARCHAR(255) NOT NULL
                );"""
            )

        if "statuses" not in cleaned_table_list:
            cursor.execute(
                """CREATE TABLE statuses (
                    GUID UUID PRIMARY KEY,
                    Name VARCHAR(255) NOT NULL
                );"""
            )

        if "settings" not in cleaned_table_list:
            cursor.execute(
                """CREATE TABLE settings (
                    GUID UUID PRIMARY KEY,
                    Status_guid UUID REFERENCES statuses(GUID),
                    Address VARCHAR(255) NOT NULL,
                    Frequency INT NOT NULL,
                    Response_time INT NOT NULL,
                    Number_of_samples INT NOT NULL
                );"""
            )

        if "services" not in cleaned_table_list:
            cursor.execute(
                """CREATE TABLE services (
                    GUID UUID PRIMARY KEY,
                    Name VARCHAR(255) NOT NULL,
                    Setting_guid UUID REFERENCES settings(GUID),
                    Actual_status UUID REFERENCES statuses(GUID)
                );"""
            )
        cursor.close()
        conn.close()
