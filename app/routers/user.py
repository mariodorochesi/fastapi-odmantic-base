from fastapi import APIRouter, Depends
from models.user import *
from utils.security import *
from schemas.user import UserOut
from database import engine
from odmantic import ObjectId

router = APIRouter()


@router.get('/me', response_model=UserOut)
async def ping(current_user: User = Depends(get_current_active_user)):
    return UserOut(name=current_user.name, email=current_user.email, created_at=current_user.created_at)
