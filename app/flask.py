"""Starts the Flask app."""

# import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import config
import constants
from databases.influxdb_tools import InfluxTools
from databases.init_influxdb import InitInfluxDB
from databases.init_postgres_db import InitPostgresDBs
from app.routes import api as api_bp

load_dotenv(override=True)

# init logs table in influxdb
InitInfluxDB.create_logs_bucket()
# write init app log
InfluxTools.write_log(constants.INIT_APP)

# init Flask
app = Flask(__name__)

# load config
app.config.from_object(config)

# enable CORS
CORS(app, supports_credentials=True, expose_headers=["Authorization"])

# init JWT manager
jwt = JWTManager(app)

# init Postgres databases
InitPostgresDBs.create_dbs()

# init SQLAlchemy
db = SQLAlchemy(app)

# init Postgres databases
with app.app_context():

    # create users table
    from models.user import User

    db.create_all(bind_key="usersdb")

    # create services table
    from models.service import Service
    from models.settings import Settings

    db.create_all(bind_key="sentineldb")

    # init scheduler
    from monitor.check_scheduler import StateChecker

    # write init scheduler log
    InfluxTools.write_log(constants.INIT_SCHEDULER)

    # init scheduler
    state_checker = StateChecker()
    state_checker.schedule_list()

# run scheduler
state_checker.run_continuously()

# register routes
app.register_blueprint(api_bp)

# write ready logs
InfluxTools.write_log(constants.API_RDY)
InfluxTools.write_log(constants.APP_RDY)
