"""Model for user instance"""

import uuid
from app.flask import db


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
    phone_number = db.Column(db.String(255), nullable=True)
    account_type = db.Column(db.String(255), nullable=False, default="user")
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return f"<User {self.login}>"
