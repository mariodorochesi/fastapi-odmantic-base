from typing import Optional, List
from database import engine
from database.base import BaseCRUD
from pydantic import EmailStr, BaseModel
from odmantic import Field, Model, ObjectId, AIOEngine



class User(Model):
    name: str
    password: str
    email: EmailStr
    is_active: Optional[bool] = Field(default=False)
    is_admin: Optional[bool] = Field(default=False)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserCRUD(BaseCRUD):

    async def get(self, email: str, engine: Optional[AIOEngine] = None) -> Optional[User]:
        query = self.model.email == email
        return await (engine.find_one(self.model, query) if engine is not None else self.engine.find_one(self.model, query))


user_crud = UserCRUD(User, engine)
