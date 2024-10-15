"""Starts the Flask app."""

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config
from app.routes import api as api_bp

load_dotenv(override=True)

app = Flask(__name__)

app.config.from_object(config)
db = SQLAlchemy(app)

app.register_blueprint(api_bp)
