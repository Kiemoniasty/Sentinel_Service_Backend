import os

from dotenv import load_dotenv

load_dotenv(override=True)

SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_BINDS = {
    "usersdb": os.getenv("USER_URL"),
    "sentineldb": os.getenv("SENTINEL_URL"),
}
