import uuid
from app.flask import db


class Service(db.Model):

    __bind_key__ = "sentineldb"
    __tablename__ = "services"

    guid = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False)
    setting_guid = db.Column(db.UUID(as_uuid=True), db.ForeignKey("settings.guid"))
    actual_state = db.Column(db.String(255), nullable=False)
    setting = db.relationship("settings", uselist=False, backref="service")

    def __repr__(self):
        return f"<Service {self.name}>"
