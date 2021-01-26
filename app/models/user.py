from typing import Optional, List
from database import engine
from database.base import BaseCRUD
from pydantic import EmailStr, BaseModel
from schemas.utils import *
from datetime import datetime
from odmantic import Field, Model, ObjectId, AIOEngine



class User(Model):
    name: str
    password: str
    email: EmailStr
    is_active: Optional[bool] = Field(default=True)
    is_admin: Optional[bool] = Field(default=False)
    is_verified: Optional[bool] = Field(default=False)
    email_validation: Optional[EmailValidation] = None
    forgot_password : Optional[ForgotPassword] = None
    created_at: datetime = Field(default=datetime.utcnow())



class UserCRUD(BaseCRUD):

    async def get(self, email: str, engine: Optional[AIOEngine] = None) -> Optional[User]:
        query = self.model.email == email
        return await (engine.find_one(self.model, query) if engine is not None else self.engine.find_one(self.model, query))
    
    async def get_by_id(self, id: str, engine: Optional[AIOEngine] = None) -> Optional[User]:
        query = self.model.id == ObjectId(id)
        return await (engine.find_one(self.model, query) if engine is not None else self.engine.find_one(self.model, query))


user_crud = UserCRUD(User, engine)
