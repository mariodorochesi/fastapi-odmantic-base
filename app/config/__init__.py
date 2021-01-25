from pydantic import BaseSettings
from datetime import timedelta
import os


class Settings(BaseSettings):
    # Mongo DB Credentials
    MONGO_USERNAME: str = os.environ.get("MONGO_INITDB_ROOT_USERNAME")
    MONGO_PASSWORD: str = os.environ.get("MONGO_INITDB_ROOT_PASSWORD")
    MONGO_HOST: str = os.environ.get("MONGO_HOST")
    MONGO_DATABASE: str = "base_project"
    # JWT
    JWT_EXPIRES_DELTA: timedelta = timedelta(minutes=15)
    SECRET_KEY: str = os.environ.get("SECRET_KEY")
    ENCRYPTION_ALGORITHM: str = "HS256"
    # Date Format
    DATETIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"


settings = Settings()
