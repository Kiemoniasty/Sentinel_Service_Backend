"""Collection of classes and methods to create userdb"""

import os
import uuid
from dotenv import load_dotenv
from sqlalchemy import UUID, Boolean, Column, String
from sqlalchemy.ext.declarative import declarative_base
from databases.postgres_tools import PostgresTools

load_dotenv()
Base = declarative_base()


class User(Base):
    """Model for user instance"""

    __tablename__ = "users"

    guid = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    login = Column(String(255), nullable=False, unique=True)
    email = Column(String(255), nullable=True, unique=True)
    password = Column(String(255), nullable=False)
    phone_number = Column(String(255), nullable=True)
    account_type = Column(String(255), nullable=False, default="user")
    is_active = Column(Boolean, nullable=False, default=True)


def create_userdb_tables():
    """Create the tables for the user database."""

    engine = PostgresTools.sqlalchemy_connector(dbname=os.getenv("USER_DB_NAME"))
    Base.metadata.create_all(engine)
