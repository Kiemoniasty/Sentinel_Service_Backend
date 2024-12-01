import uuid

from sqlalchemy import Enum
from app.flask import db
from enums.sentinel_enums import Status


class Settings(db.Model):

    __bind_key__ = "sentineldb"
    __tablename__ = "settings"

    guid = db.Column(
        db.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        unique=True,
    )
    status = db.Column(Enum(Status), nullable=False, default=Status.ACTIVE.name)
    address = db.Column(db.String(255), nullable=False)
    frequency = db.Column(db.Integer, nullable=False, default=60)
    response_time = db.Column(db.Integer, nullable=False, default=1)
    number_of_samples = db.Column(db.Integer, nullable=False, default=5)

    def __repr__(self):
        return f"""
            guid: {self.guid},
            status: {self.status},
            address: {self.address},
            frequency: {self.frequency},
            response_time: {self.response_time},
            number_of_samples: {self.number_of_samples}
            """
