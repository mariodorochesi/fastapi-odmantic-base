import codecs
from pydantic import EmailStr, SecretStr
from typing import Dict
from config import settings


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


def send_email(to: EmailStr, body: str):
    pass
