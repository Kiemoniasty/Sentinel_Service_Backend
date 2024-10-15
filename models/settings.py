import uuid

from sqlalchemy import Enum
from app.flask import db
from enums.sentinel_enums import Status


class Settings(db.Model):

    __bind_key__ = "sentineldb"
    __tablename__ = "settings"

    guid = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    status = db.Column(Enum(Status), nullable=False, default=Status.ACTIVE)
    address = db.Column(db.String(255), nullable=False)
    frequency = db.Column(db.Integer, nullable=False)
    response_time = db.Column(db.Integer, nullable=False)
    number_of_samples = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Settings {self.guid}>"
