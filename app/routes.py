"""Routes for the main parts of the app."""

from flask import Flask, jsonify
from flask_restful import Api, Resource
import handlers.constants as constants

# import psycopg
# from db_config.postgres import Postgres
from handlers.users_handler import UsersHandler

app = Flask(__name__)
api = Api(app)


class Users(Resource):
    """Users class."""

    def get(self):
        """Get all users."""
        return jsonify(UsersHandler.query_usersdb(self, constants.GET_USERS))


api.add_resource(Users, "/users")
