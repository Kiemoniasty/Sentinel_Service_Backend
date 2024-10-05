"""Collection of classes and methods to create userdb"""

import os
from dotenv import load_dotenv
from databases.postgres_tools import PostgresTools
from models.user import Base

load_dotenv()


def create_userdb_tables():
    """Create the tables for the user database."""

    engine = PostgresTools.sqlalchemy_connector(dbname=os.getenv("USER_DB_NAME"))
    Base.metadata.create_all(engine)
