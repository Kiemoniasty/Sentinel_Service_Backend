import os
import uuid
from dotenv import load_dotenv
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases.postgres_tools import PostgresTools

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


def create_userdb_tables():
    """Create the tables for the user database."""

    engine = PostgresTools.db_connector(os.getenv("USER_DB_NAME"))
    Base.metadata.create_all(engine)

    sessionmk = sessionmaker(bind=engine)
    session = sessionmk()

    if not session.query(AccountType).count():
        session.add_all(
            [AccountType(account_type="admin"), AccountType(account_type="user")]
        )

    if not session.query(AccountStatus).count():
        session.add_all([AccountStatus(is_active=True), AccountStatus(is_active=False)])

    session.commit()
    session.close()
