from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
from email.utils import formataddr
from sqlalchemy.orm import Session
from app.models import Contact
from datetime import datetime
from utils import get_unique_verification_token
import os

class EmailService:
    def __init__(self):
        self.conf = ConnectionConfig(
            MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
            MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
            MAIL_FROM=os.getenv("MAIL_FROM"),
            MAIL_PORT=int(os.getenv("MAIL_PORT")),
            MAIL_SERVER=os.getenv("MAIL_SERVER"),
            MAIL_TLS=True,
            MAIL_SSL=False,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True
        )
        self.mail = FastMail(self.conf)

    async def send_verification_email(self, contact: Contact, db: Session):
        verification_token = get_unique_verification_token(contact.email)
        verification_url = f"http://your-frontend.com/verify-email?token={verification_token}"

        message = MessageSchema(
            subject="Email Verification",
            recipients=[contact.email],
            body=f"Please verify your email by clicking the link: {verification_url}",
            subtype="html"
        )

        try:
            await self.mail.send_message(message)
            contact.verification_token = verification_token
            contact.token_sent_at = datetime.utcnow()
            db.commit()
            db.refresh(contact)
        except Exception as e:
            print(f"Error sending email: {e}")
            return False

        return True

    async def send_password_reset_email(self, contact: Contact, db: Session):
        reset_token = get_unique_verification_token(contact.email)
        reset_url = f"http://your-frontend.com/reset-password?token={reset_token}"

        message = MessageSchema(
            subject="Password Reset",
            recipients=[contact.email],
            body=f"Please reset your password by clicking the link: {reset_url}",
            subtype="html"
        )

        try:
            await self.mail.send_message(message)
            contact.reset_token = reset_token
            contact.token_sent_at = datetime.utcnow()
            db.commit()
            db.refresh(contact)
        except Exception as e:
            print(f"Error sending email: {e}")
            return False

        return True
