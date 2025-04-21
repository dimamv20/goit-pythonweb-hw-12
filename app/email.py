import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import HTTPException

def send_verification_email(to_email: str, token: str):
    subject = "Email Verification"
    body = f"Click on the link to verify your email: http://localhost:8000/verify/{token}"

    msg = MIMEMultipart()
    msg['From'] = "your_email@example.com"
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.example.com', 587)
        server.starttls()
        server.login("your_email@example.com", "password")
        text = msg.as_string()
        server.sendmail("your_email@example.com", to_email, text)
        server.quit()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to send email")
