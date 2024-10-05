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

# class User(db.Model):
#     """Model for user instance"""

#     __bind_key__ = "usersdb"
#     __tablename__ = "users"

#     guid = db.Column(
#         db.UUID(as_uuid=True),
#         primary_key=True,
#         default=uuid.uuid4,
#         unique=True,
#         nullable=False,
#     )
#     login = db.Column(db.String(255), nullable=False, unique=True)
#     email = db.Column(db.String(255), nullable=True, unique=True)
#     password = db.Column(db.String(255), nullable=False)
#     phone_number = db.Column(db.String(255), nullable=True, unique=True)
#     account_type = db.Column(db.String(255), nullable=False, default="user")
#     is_active = db.Column(db.Boolean, nullable=False, default=True)

#     def __repr__(self):
#         return f"<User {self.login}>"

# class UserController(Resource):
#     def get(self=None, guid=None, login=None, email=None, phone_number=None, account_type=None, is_active=None):

#         query = User.query.all()
#         result = []
#         for item in query:
#             result.append({ "guid": item.guid,
#                       "login": item.login,
#                       "email": item.email,
#                       "phone_number": item.phone_number,
#                       "account_type": item.account_type,
#                       "is_active": item.is_active })
#         return jsonify(result)

api.add_resource(UserController, BASE_URL + "/users", "/users/<string:guid>")
