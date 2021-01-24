from pydantic import BaseSettings
import os


class Settings(BaseSettings):
    # Mongo DB Credentials
    MONGO_USERNAME: str = os.environ.get("MONGO_INITDB_ROOT_USERNAME")
    MONGO_PASSWORD: str = os.environ.get("MONGO_INITDB_ROOT_PASSWORD")
    MONGO_HOST: str = os.environ.get("MONGO_HOST")
    MONGO_DATABASE: str = "base_project"


settings = Settings()
