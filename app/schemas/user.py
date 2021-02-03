from pydantic import BaseModel, EmailStr
from odmantic import ObjectId, Model
from datetime import datetime


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserEmail(BaseModel):
    email: EmailStr


class UserOut(BaseModel):
    name: str
    email: EmailStr
    created_at: datetime
