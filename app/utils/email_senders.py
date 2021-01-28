from pydantic import EmailStr, SecretStr
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Header
from utils.exceptions import MessageException
import random


class SMTPEmailSender:

    def __init__(self, sender_email: EmailStr, sender_password: SecretStr, sender_host: str, sender_port: int):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.sender_host = sender_host
        self.sender_port = sender_port

    def send_email(self, to_email: EmailStr, subject: str, body: str):
        message = MIMEMultipart()
        message['From'] = self.sender_email
        message['To'] = to_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'html'))
        context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        with smtplib.SMTP_SSL(self.sender_host, self.sender_port, context=context) as server:
            server.login(self.sender_email, self.sender_password)
            server.sendmail(self.sender_email, to_email, message.as_string())


class SendGridEmailSender:

    def __init__(self, sender_email: EmailStr, api_key: str):
        self.api_key = api_key
        self.sender_email = sender_email

    def send_email(self, to_email: EmailStr, subject: str, body: str):
        message = Mail(from_email=self.sender_email,
                       to_emails=to_email, subject=subject, html_content=body)
        message.add_header(
            Header('X-Entity-Ref-ID', str(random.randint(1, 15000000))))
        sg = SendGridAPIClient(self.api_key)
        response = sg.send(message)
