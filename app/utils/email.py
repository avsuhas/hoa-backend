import os
from email.message import EmailMessage
from aiosmtplib import SMTP
from dotenv import load_dotenv

load_dotenv()

EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_FROM = os.getenv("EMAIL_FROM", EMAIL_USER)

async def send_email_async(to_email: str, subject: str, body: str):
    message = EmailMessage()
    message["From"] = EMAIL_FROM
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(body)

    smtp = SMTP(hostname=EMAIL_HOST, port=EMAIL_PORT, start_tls=True)
    await smtp.connect()
    await smtp.login(EMAIL_USER, EMAIL_PASSWORD)
    await smtp.send_message(message)
    await smtp.quit() 