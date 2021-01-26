from pydantic import BaseModel, Field
from datetime import datetime
from config import settings
import secrets


class EmailValidation(BaseModel):
    token: str = Field(default=secrets.token_urlsafe(32))
    expires_at: datetime = Field(
        default=datetime.utcnow() + settings.EMAIL_VALIDATION_EXPIRES_DELTA)


class ForgotPassword(BaseModel):
    token: str = Field(default=secrets.token_urlsafe(32))
    expires_at: datetime = Field(
        default=datetime.utcnow() + settings.PASSWORD_RECOVERY_EXPIRES_DELTA)
