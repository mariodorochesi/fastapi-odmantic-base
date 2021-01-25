from fastapi import APIRouter, Depends
from models.user import *
from utils.security import *
from database import engine
from odmantic import ObjectId

router = APIRouter()


@router.get('/ping')
async def ping(current_user: User = Depends(get_current_active_user)):
    return {"message": "pong"}
