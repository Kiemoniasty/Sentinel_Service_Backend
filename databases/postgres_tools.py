"""Postgres tools that can be used in none specific tasks"""

import os
import psycopg
from dotenv import load_dotenv
from sqlalchemy import create_engine
from controllers.service_tools import ServiceTools

load_dotenv(override=True)


class PostgresTools:
    """Universal Postgresql tools"""

    def psycopg_connector(self=None, dbname=None):
        """Establish connection with database with Psycopg"""

        return psycopg.connect(
            host=os.getenv("POSTGRES"),
            hostaddr=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            dbname=dbname,
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
        )

    def sqlalchemy_connector(self=None, dbname=None):
        """Establish a connection with the database via SQLAlchemy."""

        user = os.getenv("POSTGRES_USER")
        password = os.getenv("POSTGRES_PASSWORD")
        host = os.getenv("POSTGRES_HOST")
        port = os.getenv("POSTGRES_PORT")

        return create_engine(f"postgresql://{user}:{password}@{host}:{port}/{dbname}")

    def write_data(self=None, data=None):
        """Write data to the database."""
        from app.flask import db

        db.session.add(data)
        db.session.commit()

    def delete_data(self=None, data=None):
        """Delete data from the database."""
        from app.flask import db

        db.session.delete(data)
        db.session.commit()

    def update_service(self=None, guid=None, data=None):
        """Update service data in the database."""

        setting = data.get("setting", {})

        from models.settings import Settings
        from models.service import Service
        from app.flask import db, app

        with app.app_context():
            service = Service.query.filter_by(guid=guid).first()
            settings = Settings.query.filter_by(guid=service.setting_guid).first()

            if "name" in data:
                service.name = data["name"]
            if "actual_state" in data:
                service.actual_state = ServiceTools.valid_actual_state(
                    actual_state=data["actual_state"]
                )

            if "status" in setting:
                print(setting["status"])
                settings.status = ServiceTools.valid_status(status=setting["status"])
            if "address" in setting:
                settings.address = setting["address"]
            if "frequency" in setting:
                settings.frequency = ServiceTools.string_to_int(
                    data=setting["frequency"]
                )
            if "response_time" in setting:
                settings.response_time = setting["response_time"]
            if "number_of_samples" in setting:
                settings.number_of_samples = setting["number_of_samples"]

            db.session.commit()
