from pydantic import BaseSettings, SecretStr
from enum import Enum
from typing import Optional
from datetime import timedelta
from utils.email_senders import SMTPEmailSender
import os


class EmailSenderOption(str, Enum):
    sendgrid = 'sendgrid'
    smtp = 'smtp'


class Settings(BaseSettings):
    # Mongo DB Credentials
    MONGO_USERNAME: str = os.environ.get("MONGO_INITDB_ROOT_USERNAME")
    MONGO_PASSWORD: str = os.environ.get("MONGO_INITDB_ROOT_PASSWORD")
    MONGO_HOST: str = os.environ.get("MONGO_HOST")
    MONGO_DATABASE: str = "base_project"
    # JWT
    JWT_EXPIRES_DELTA: timedelta = timedelta(hours=24)
    SECRET_KEY: str = os.environ.get("SECRET_KEY")
    ENCRYPTION_ALGORITHM: str = "HS256"
    # Date Format
    DATETIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"
    # Email Validation Token
    EMAIL_VALIDATION_EXPIRES_DELTA: timedelta = timedelta(hours=24)
    # Password Recovery Token
    PASSWORD_RECOVERY_EXPIRES_DELTA: timedelta = timedelta(minutes=15)
    # Base URL
    API_BASE_URL: str = 'localhost'
    # Base Directory
    BASE_DIRECTORY: str = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))
    # Html Files Directory
    HTML_DIRECTORY: str = '/static/html/'
    # Email Sender Settings
    EMAIL_SENDER_OPTION: EmailSenderOption = EmailSenderOption.smtp.value
    # Email SMTP Settings
    EMAIL_SENDER_ADDRESS: Optional[str] = os.environ.get(
        "EMAIL_SENDER_ADRESS") or None
    EMAIL_SENDER_PASSWORD: Optional[SecretStr] = os.environ.get(
        "EMAIL_SENDER_PASSWORD") or None
    EMAIL_SENDER_SMTP_HOST: Optional[str] = os.environ.get(
        "EMAIL_SENDER_SMTP_HOST") or "smtp.gmail.com"
    EMAIL_SENDER_SMTP_PORT: Optional[int] = os.environ.get(
        "EMAIL_SENDER_SMTP_PORT") or 465
    EMAIL_SENDER_INSTANCE: SMTPEmailSender = SMTPEmailSender(
        EMAIL_SENDER_ADDRESS, EMAIL_SENDER_PASSWORD, EMAIL_SENDER_SMTP_HOST, EMAIL_SENDER_SMTP_PORT)


settings = Settings()
print(settings.EMAIL_SENDER_PASSWORD)
