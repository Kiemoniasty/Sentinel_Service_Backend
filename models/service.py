import uuid

from sqlalchemy import Enum
from app.flask import db
from enums.sentinel_enums import Response


class Service(db.Model):

    __bind_key__ = "sentineldb"
    __tablename__ = "services"

    guid = db.Column(
        db.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        unique=True,
    )
    name = db.Column(db.String(255), nullable=False)
    setting_guid = db.Column(db.UUID(as_uuid=True), db.ForeignKey("settings.guid"))
    actual_state = db.Column(Enum(Response), nullable=True, default=None)
    setting = db.relationship("Settings", uselist=False, backref="service")

    def __repr__(self):
        return f"""
            guid: {self.guid},
            name: {self.name},
            setting_guid: {self.setting_guid},
            actual_state: {self.actual_state}
            """
