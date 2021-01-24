from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
from config import settings
import os

MONGO_USERNAME = settings.MONGO_USERNAME
MONGO_PASSWORD = settings.MONGO_PASSWORD
MONGO_HOST = settings.MONGO_HOST
MONGO_DATABASE = settings.MONGO_DATABASE

# Cliente Motor que se conecta con la base de datos Mongo
client = AsyncIOMotorClient(
    f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:27017/")

# Engine de Odmantic que sirve como ODM conectado a la base de datos
engine = AIOEngine(motor_client=client, database=settings.MONGO_DATABASE)
