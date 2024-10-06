"""Starts the Flask app."""

import os
from dotenv import load_dotenv
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from controllers.user_controller import UserController

# from handlers.user import UserHandler
BASE_URL = "/api/v1"
load_dotenv(override=True)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_BINDS"] = {
    "usersdb": os.getenv("USER_URL"),
    "sentineldb": os.getenv("SENTINEL_URL"),
}
api = Api(app)
db = SQLAlchemy(app)

api.add_resource(UserController, BASE_URL + "/users", "/users/<string:guid>")
