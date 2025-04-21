from fastapi import Request
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import dotenv_values

config = dotenv_values(".env")

conf = ConnectionConfig(
    MAIL_USERNAME=config["MAIL_USERNAME"],
    MAIL_PASSWORD=config["MAIL_PASSWORD"],
    MAIL_FROM=config["MAIL_FROM"],
    MAIL_PORT=int(config["MAIL_PORT"]),
    MAIL_SERVER=config["MAIL_SERVER"],
    MAIL_FROM_NAME="Your App",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
)

async def send_verification_email(email: str, username: str, token: str, request: Request):
    verification_link = f"{request.base_url}auth/verify-email?token={token}"
    message = MessageSchema(
        subject="Verify your email",
        recipients=[email],
        body=f"Hi {username},\nPlease verify your email by clicking the link: {verification_link}",
        subtype="plain"
    )
    fm = FastMail(conf)
    await fm.send_message(message)
