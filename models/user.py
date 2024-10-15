"""Model for user instance"""

import uuid

from sqlalchemy import Enum
from app.flask import db
from enums.user_enums import AccountType


class User(db.Model):
    """Model for user instance"""

    __bind_key__ = "usersdb"
    __tablename__ = "users"

    guid = db.Column(
        db.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    login = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=True, unique=True)
    password = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(255), nullable=True, unique=True)
    account_type = db.Column(
        Enum(AccountType), nullable=False, default=AccountType.USER
    )
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return f"<User {self.login}>"
