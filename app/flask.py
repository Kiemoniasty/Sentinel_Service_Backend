"""Starts the Flask app."""

# import os
import config
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from databases.init_postgres_db import InitPostgresDBs

# import config
from app.routes import api as api_bp


load_dotenv(override=True)

app = Flask(__name__)

app.config.from_object(config)
InitPostgresDBs.create_dbs()
db = SQLAlchemy(app)

with app.app_context():

    from models.user import User

    db.create_all(bind_key="usersdb")

    from models.service import Service
    from models.settings import Settings

    db.create_all(bind_key="sentineldb")

    from monitor.check_scheduler import StateChecker

    state_checker = StateChecker()
    state_checker.schedule_list()

app.register_blueprint(api_bp)


print("retrive tasks list")
all_tasks = state_checker.get_task_list()
for i, task in enumerate(all_tasks):
    print(i, " - ", task)
print("retrieved")
# state_checker.run_continuously()

# InfluxTools.write_data()
