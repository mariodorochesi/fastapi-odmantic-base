from fastapi import APIRouter, Response, Depends
from fastapi.responses import JSONResponse
from models.user import *
from utils.security import *
from schemas.token import Token
from database import engine
from pydantic import EmailStr
from typing import Dict
from jose import JWTError

router = APIRouter()


@router.post('/register', status_code=200)
async def register_user(user_data: User, response: Response):
    # Get user from database
    user = await user_crud.get(user_data.email)
    # If user was not found
    if user is not None:
        response.status_code = 400
        return {"message": "Email is already registered."}
    # Hash password
    user = user_data
    user.password = hash_password(user.password)
    # Insert new user on database
    insert_response = await user_crud.create_or_update(user)
    # If user was not inserted
    if insert_response is None:
        response.status_code = 400
        return {"message": "There was a problem registering user."}
    # Return success message :D
    return {"message": "User was succesfully registered."}


@router.post('/login', status_code=200)
async def login_user(user_data: UserLogin, response: Response):
    # Get user from database
    user = await user_crud.get(user_data.email)
    # If user was not found
    if user is None:
        response.status_code = 400
        return {"message": "Email not registered for any user."}
    # Verify password against hashed database password
    if not verify_password(user_data.password, user.password):
        response.status_code = 400
        return {"message": "Password does not match our database."}
    # JWT payload
    data = {"email": user.email}
    # Create JWT
    try:
        jwt = create_acess_token(data)
        return Token(access_token=jwt, token_type="bearer")
    # If failed inform about error
    except JWTError as e:
        response.status_code = 400
        return {"message": "There was an error creating JWT."}
