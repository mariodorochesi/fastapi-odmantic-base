import codecs
from pydantic import EmailStr, SecretStr
from typing import Dict
from config import settings
from utils.exceptions import MessageException


def get_html(filename: str, replacements: Dict = {}):
    """
        Returns raw HTML given a filename

    Args:
        filename (str): Name of HTML file
        replacements (Dict): Dict with Key-Value for replacing template tags
    """
    # Open HTML File
    file = codecs.open(settings.BASE_DIRECTORY +
                       settings.HTML_DIRECTORY + filename, 'r')
    # Get raw HTML
    html = file.read()
    # Replace template tags
    for original, replacement in replacements.items():
        html = html.replace(original, replacement)
    # Close file
    file.close()
    # Return raw HTML
    return html


def send_email(to_email: EmailStr, subject: str, body: str):
    if settings.EMAIL_SENDER_OPTION == 'sendgrid':
        try:
            settings.SENDGRID_INSTANCE.send_email(to_email, subject, body)
        except Exception as e:
            print(e)
            raise MessageException(status_code=400, content={
                                   "message": "SendGridEmail not properly configured."})
    elif settings.EMAIL_SENDER_OPTION == 'smtp':
        try:
            settings.EMAIL_SENDER_INSTANCE.send_email(to_email, subject, body)
        except Exception as e:
            print(e)
            raise MessageException(status_code=400, content={
                                   "message": "SMTPEmailSender not properly configured."})
    else:
        raise MessageException(status_code=400, content={
                               "message": "No proper mail sender configured."})
