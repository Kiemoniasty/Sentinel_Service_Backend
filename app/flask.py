"""Starts the Flask app."""

# import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import config
import constants
from databases.influxdb_tools import InfluxTools
from databases.init_influxdb import InitInfluxDB
from databases.init_postgres_db import InitPostgresDBs

# import config
from app.routes import api as api_bp

load_dotenv(override=True)

# init logs table in influxdb
InitInfluxDB.create_logs_bucket()
InfluxTools.write_log(constants.INIT_APP)

app = Flask(__name__)
app.config.from_object(config)
CORS(app)

# init Postgres databases
InitPostgresDBs.create_dbs()

db = SQLAlchemy(app)

with app.app_context():

    from models.user import User

    db.create_all(bind_key="usersdb")

    from models.service import Service
    from models.settings import Settings

    db.create_all(bind_key="sentineldb")

    from monitor.check_scheduler import StateChecker

    InfluxTools.write_log(constants.INIT_SCHEDULER)

    # init scheduler
    state_checker = StateChecker()
    state_checker.schedule_list()

state_checker.run_continuously()

# InfluxTools.write_log(constants.SCHD_RETRIVED)
# all_tasks = state_checker.get_task_list()
# for i, task in enumerate(all_tasks):
#     print(i, " - ", task)
# print("retrieved")


app.register_blueprint(api_bp)

InfluxTools.write_log(constants.API_RDY)
InfluxTools.write_log(constants.APP_RDY)
