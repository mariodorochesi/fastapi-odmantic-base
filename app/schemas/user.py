from pydantic import BaseModel, EmailStr
from odmantic import ObjectId, Model
from datetime import datetime


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    name: str
    email: EmailStr
    created_at: datetime
