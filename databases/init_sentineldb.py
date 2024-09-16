"""Collection of classes and methods to initialize the sentinel database."""

import os
import uuid
from dotenv import load_dotenv
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from databases.postgres_tools import PostgresTools

load_dotenv()
Base = declarative_base()


class Settings(Base):
    """Class model for settings table"""

    __tablename__ = "settings"

    guid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    status = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    frequency = Column(Integer, nullable=False)
    response_time = Column(Integer, nullable=False)
    number_of_samples = Column(Integer, nullable=False)


class Services(Base):
    """Class model for services table"""

    __tablename__ = "services"

    guid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    setting_guid = Column(UUID(as_uuid=True), ForeignKey("settings.guid"))
    actual_state = Column(String(255), nullable=False)


def create_sentineldb_tables():
    """Create the tables for the sentinel database."""

    engine = PostgresTools.sqlalchemy_connector(dbname=os.getenv("SENTINEL_DB_NAME"))
    Base.metadata.create_all(engine)
