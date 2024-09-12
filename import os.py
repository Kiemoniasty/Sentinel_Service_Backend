import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uuid

load_dotenv()

Base = declarative_base()


class AccountType(Base):
    __tablename__ = "account_type"

    guid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_type = Column(String(255), nullable=False)


class AccountStatus(Base):
    __tablename__ = "account_status"

    guid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    is_active = Column(Boolean, nullable=False)


class User(Base):
    __tablename__ = "users"

    guid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    login = Column(String(255), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    phone_number = Column(Integer)
    account_type = Column(UUID(as_uuid=True), ForeignKey("account_type.guid"))
    is_active = Column(UUID(as_uuid=True), ForeignKey("account_status.guid"))


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


class InitPostgresDBs:
    """Initialize the databases and tables using SQLAlchemy."""

    def db_connector(self, dbname):
        """Establish a connection with the database."""
        return create_engine(
            f'postgresql://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("POSTGRES_HOST")}:{os.getenv("POSTGRES_PORT")}/{dbname}'
        )

    def create_dbs(self=None):
        """Create the databases and tables."""

        # Connecting to the main database to create other databases
        engine = self.db_connector(os.getenv("POSTGRES_DB_NAME"))
        conn = engine.connect()

        conn.execute(
            "commit"
        )  # Required in psycopg2 to commit CREATE DATABASE commands

        existing_dbs = [
            db[0] for db in conn.execute("SELECT datname FROM pg_database;")
        ]

        if os.getenv("SENTINEL_DB_NAME") not in existing_dbs:
            conn.execute(f"CREATE DATABASE {os.getenv('SENTINEL_DB_NAME')}")
        if os.getenv("USER_DB_NAME") not in existing_dbs:
            conn.execute(f"CREATE DATABASE {os.getenv('USER_DB_NAME')}")

        conn.close()

        self.create_users_tables()
        self.create_sentinel_tables()

    def create_users_tables(self=None):
        """Create the tables for the user database."""

        # Connecting to the USER_DB_NAME
        engine = self.db_connector(os.getenv("USER_DB_NAME"))
        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        session = Session()

        # Check and insert default account types and statuses
        if not session.query(AccountType).count():
            session.add_all(
                [AccountType(account_type="admin"), AccountType(account_type="user")]
            )

        if not session.query(AccountStatus).count():
            session.add_all(
                [AccountStatus(is_active=True), AccountStatus(is_active=False)]
            )

        session.commit()
        session.close()

    def create_sentinel_tables(self=None):
        """Create the tables for the sentinel database."""

        # Connecting to the SENTINEL_DB_NAME
        engine = self.db_connector(os.getenv("SENTINEL_DB_NAME"))
        Base.metadata.create_all(engine)

        # No default data insertion required for sentinel tables


# Example of usage:
if __name__ == "__main__":
    InitPostgresDBs().create_dbs()
