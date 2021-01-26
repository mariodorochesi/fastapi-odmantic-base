from passlib.context import CryptContext
from typing import Optional
from schemas.token import *
from datetime import timedelta, datetime
from config import settings
from jose import JWTError, jwt
from fastapi import status, Depends
from utils.exceptions import MessageException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models.user import *


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password: str, hashed_password: str):
    """
        Verify if a plain_password matches with hashed password

    Returns:
        [bool] : True if password matches, otherwise return False
    """
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str):
    """
        Hash a given password

    Returns:
        [str]: String with password hashed
    """
    return pwd_context.hash(password)


def create_acess_token(data: TokenData, expires_delta: timedelta = settings.JWT_EXPIRES_DELTA):
    """
        Create an access token given an TokenData schema

    Returns:
        [str] : String with encoded jwt
    """
    # Calculate expire datetime based on settings
    expire = datetime.utcnow() + expires_delta
    # Add or replace expire field on dictionary
    data["expire_at"] = expire.strftime(settings.DATETIME_FORMAT)
    # Encode JWT
    encoded_jwt = jwt.encode(data, settings.SECRET_KEY,
                             algorithm=settings.ENCRYPTION_ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
        Get current user based on Token

    Raises:
        credentials_exceptions: If credentials doesnt match Token

    Returns:
        [User] : Model instance of corresponding User
    """
    credentials_exceptions = MessageException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"content" : "Could not validate credentials"},
        headers={"WWW-Authenticate": "Bearer"},
    )

    expired_token_exception = MessageException(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"message": "Token expired"},
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        # Decode JWT
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[
                             settings.ENCRYPTION_ALGORITHM])
        # Get email from JWT payload
        email: str = payload.get("email")
        # Validate email
        if email is None:
            raise credentials_exceptions
        # Get expire time from JWT payload
        expire: datetime = datetime.strptime(
            payload.get("expire_at"), settings.DATETIME_FORMAT)
        # Validate that JWT hasnt expired
        if expire < datetime.utcnow():
            raise expired_token_exception
        # Create TokenData schema
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exceptions
    # Get user instance from Database
    user = await user_crud.get(token_data.email)
    # Check user
    if user is None:
        raise credentials_exceptions
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """
        Validate that current user is active
    """
    if not current_user.is_verified:
        raise MessageException(status_code=400, content={"message" : "User is not verified."})
    if not current_user.is_active:
        raise MessageException(status_code=400, content={"message" : "User is not active."})
    return current_user
