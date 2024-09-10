"""Collection of the instruction to prepare and start api"""

# import os
from flask import Flask

# from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from databases.influxdb_tools import InfluxTools
from databases.init_postgres_db import InitPostgresDBs

# Load environment variables from .env file
load_dotenv(override=True)

# Start creation of database structure in postgres
InitPostgresDBs.create_dbs()
InfluxTools.influxdb_connector()

app = Flask(__name__)

# Set the SQLALCHEMY_DATABASE_URI from the environment variable
# app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the SQLAlchemy object
# db = SQLAlchemy(app)


# Define the User model
# class User(db.Model):
#     __tablename__ = "users"

#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)

#     def __repr__(self):
#         return f"<User {self.username}>"


# if __name__ == "__main__":
#     app.run(debug=True)
