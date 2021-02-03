from fastapi import APIRouter, Response, Depends, status
from fastapi.responses import JSONResponse
from models.user import *
from utils.security import *
from utils.email import *
from schemas.token import Token
from schemas.utils import *
from schemas.user import *
from database import engine
from pydantic import EmailStr
from typing import Dict
from jose import JWTError
import codecs

router = APIRouter()


@router.post('/register', status_code=status.HTTP_200_OK)
async def register_user(user_data: User, response: Response):
    # Get user from database
    user = await user_crud.get(user_data.email)
    # If user was not found
    if user is not None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Email is already registered."}
    # Hash password
    user = user_data
    user.password = hash_password(user.password)
    # Create a new Email Validation Token
    user.email_validation = EmailValidation()
    """ARREGLAR ERROR DE LOGICA"""
    """TODO: Add email sender for validation"""
    html = get_html('activate_account.html',
                    replacements={"{{NAME}}": user.name, "{{URL}}": settings.API_BASE_URL + f'/auth/email-validation?email={user.email}&token={user.email_validation.token}'})
    send_email(user.email, "Welcome Aboard!", html)
    # Insert new user on database
    insert_response = await user_crud.create_or_update(user)
    # If user was not inserted
    if insert_response is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "There was a problem registering user."}
    # Return success message :D
    return {"message": "User was succesfully registered."}


@router.post('/login', status_code=status.HTTP_200_OK)
async def login_user(user_data: UserLogin, response: Response):
    # Get user from database
    user = await user_crud.get(user_data.email)
    # If user was not found
    if user is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Email not registered for any user."}
    # Verify password against hashed database password
    if not verify_password(user_data.password, user.password):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Password does not match our database."}
    # JWT payload
    data = {"email": user.email}
    # Create JWT
    try:
        jwt = create_acess_token(data)
        return Token(access_token=jwt, token_type="bearer")
    # If failed inform about error
    except JWTError as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "There was an error creating JWT."}


@router.post('/forgot-password', status_code=status.HTTP_200_OK)
async def forgot_password(email: EmailStr):
    # Find user
    user = await user_crud.get(email)
    # If user is None
    if user is None:
        raise MessageException(status_code=status.HTTP_400_BAD_REQUEST, content={
                               "message": "User was not found."})
    # Generate new password token
    user.forgot_password = ForgotPassword()
    # Update user document on database
    update_response = await user_crud.create_or_update(user)
    # If update fail
    if update_response is None:
        raise MessageException(status_code=status.HTTP_400_BAD_REQUEST, content={
                               "message": "We had a problem recovering your password."})
    """TODO: Add email sender for password recovering"""
    return {"message": "Recover password token succesfully created."}


@router.post('/email-validation-apply')
async def ask_email_validation(email: UserEmail, user=Depends(email_delay_check)):
    # If user is already verified
    if user.is_verified:
        raise MessageException(status_code=status.HTTP_400_BAD_REQUEST, content={
                               "message": "User is already verified."})
    if user.email_validation is not None:
        # If current token hasnt expired yet
        if datetime.utcnow() < user.email_validation.expires_at:
            raise MessageException(status_code=status.HTTP_400_BAD_REQUEST, content={
                                   "message": "You already have an active request. Check your email to activate your account."})
    # Create new email validation
    user.email_validation = EmailValidation()
    # Update record on database
    insert_response = await user_crud.create_or_update(user)
    # If there was a problem inserting on database
    if insert_response is None:
        raise MessageException(status_code=status.HTTP_400_BAD_REQUEST, content={
                               "message": "We had a problem processing your request."})
    """TODO: Add email sender for validation"""
    html = get_html('activate_account.html',
                    replacements={"{{NAME}}": user.name, "{{URL}}": settings.API_BASE_URL + f'/auth/email-validation?email={user.email}&token={user.email_validation.token}'})
    send_email(user.email, "Welcome Aboard!", html)
    return {"message": "Email validation sent"}

@router.get('/email-validation', status_code=status.HTTP_200_OK)
async def validate_email(email: EmailStr, token: str):
    # Find user by provided id on URL
    user = await user_crud.get(email)
    # If user is none
    if user is None:
        raise MessageException(status_code=status.HTTP_400_BAD_REQUEST, content={
                               "message": "User was not found."})
    # If user is already verified
    if user.is_verified:
        raise MessageException(status_code=status.HTTP_400_BAD_REQUEST, content={
                               "message": "User is already verified."})
    # If user has no email_validation field on database
    if user.email_validation is None:
        raise MessageException(status_code=status.HTTP_400_BAD_REQUEST, content={
                               "message": "User has no email_validation record."})
    # If token has already expired
    if user.email_validation.expires_at < datetime.utcnow():
        raise MessageException(status_code=status.HTTP_400_BAD_REQUEST, content={
                               "message": "Token has already expired."})
    # If provided token does not match database token
    if token != user.email_validation.token:
        raise MessageException(status_code=status.HTTP_400_BAD_REQUEST, content={
                               "message": "Token provided does not match with database."})
    # Destroy email_validation object on database
    user.email_validation = None
    # Verify user on database
    user.is_verified = True
    # Update user document on database
    insert_response = await user_crud.create_or_update(user)
    # If update failed
    if insert_response is None:
        raise MessageException(status_code=status.HTTP_400_BAD_REQUEST, content={
                               "message": "We had a problem activating your account."})
    return {"message": "User was succesfully verified."}
