from datetime import timedelta
import os

from dotenv import load_dotenv

load_dotenv(override=True)

SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_BINDS = {
    "usersdb": os.getenv("USER_URL"),
    "sentineldb": os.getenv("SENTINEL_URL"),
}
JWT_SECRET_KEY = os.getenv("JWT_SECRET")
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=10)
JWT_TOKEN_LOCATION = ["headers"]
JWT_HEADER_NAME = "Authorization"
JWT_HEADER_TYPE = "Bearer"
JWT_HASH_ALGORITHM = "HS256"
# JWT_REFERSH_TOKEN_EXPIRES = 36000
