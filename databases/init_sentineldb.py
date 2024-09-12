import os
import uuid
from dotenv import load_dotenv
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases.postgres_tools import PostgresTools

load_dotenv()
Base = declarative_base()


class ServiceStatuses(Base):
    __tablename__ = "service_statuses"

    guid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)


class LoggerMessages(Base):
    __tablename__ = "logger_messages"

    guid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = Column(String(255), nullable=False)


class ErrorCodes(Base):
    __tablename__ = "error_codes"

    guid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(50), nullable=False)


class NotificationMessages(Base):
    __tablename__ = "notification_messages"

    guid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = Column(String(255), nullable=False)


class Statuses(Base):
    __tablename__ = "statuses"

    guid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)


class Settings(Base):
    __tablename__ = "settings"

    guid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    status_guid = Column(UUID(as_uuid=True), ForeignKey("statuses.guid"))
    address = Column(String(255), nullable=False)
    frequency = Column(Integer, nullable=False)
    response_time = Column(Integer, nullable=False)
    number_of_samples = Column(Integer, nullable=False)


class Services(Base):
    __tablename__ = "services"

    guid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    setting_guid = Column(UUID(as_uuid=True), ForeignKey("settings.guid"))
    actual_status = Column(UUID(as_uuid=True), ForeignKey("statuses.guid"))


def create_sentineldb_tables():
    """Create the tables for the sentinel database."""

    engine = PostgresTools.db_connector(os.getenv("SENTINEL_DB_NAME"))
    Base.metadata.create_all(engine)

    sessionmk = sessionmaker(bind=engine)
    session = sessionmk()

    # dummy data
    if not session.query(AccountType).count():
        session.add_all(
            [AccountType(account_type="admin"), AccountType(account_type="user")]
        )
