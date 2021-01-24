from fastapi import APIRouter
from models.user import *
from models.correo import Correo
from database import engine
from odmantic import ObjectId

router = APIRouter()


@router.get('/create')
async def create_user():
    user = User(name="Mario Dorochesi")
    response = await user_crud.create_or_update(user)
    if response is None:
        return {"message": "User could not be created for strange reasons."}
    return {"message": "User created succesfully", "payload": user}


@router.get('/find')
async def find_user():
    user = await user_crud.get("600cb30bfcd404ed9941fba1")
    return {"message": user}


@router.get("/email")
async def email_user():
    user = await user_crud.get("600cb4abd1a17a48c84c6e0a")
    if user is None:
        return {"message": "User does not exists!"}
    user.correos.append(Correo(direccion="blablabla@google.com"))
    response = await user_crud.create_or_update(user)
    if response is None:
        return {"message": "User could not be updated"}
    return {"message": "User was succesfully updated", "payload": user}


@router.get("/delete")
async def delete_user():
    user = await user_crud.get("600cb6951a1677d1dc2f1d2a")
    if user is None:
        return {"message": "User does not exists!"}
    response = await user_crud.delete(user)
    print(response)
    if response is not None:
        return {"message": "User could not be deleted"}
    return {"message": "User was succesfully deleted"}
