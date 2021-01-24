from models.correo import Correo
from typing import Optional, List
from database import engine
from database.base import BaseCRUD
from odmantic import Field, Model, ObjectId


class User(Model):
    name: str
    correos: Optional[List[Correo]] = []


class UserCRUD(BaseCRUD):
    pass


user_crud = UserCRUD(User, engine)
