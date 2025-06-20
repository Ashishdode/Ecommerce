import smtplib
from email.message import EmailMessage
from app.core.config import settings

def send_email(subject: str, recipient: str, body: str):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = settings.MAIL_FROM
    msg["To"] = recipient
    msg["X-PM-Message-Stream"] = "outbound"
    msg.set_content(body)

    with smtplib.SMTP(settings.MAIL_SERVER, settings.MAIL_PORT) as server:
        server.starttls()
        server.login(settings.MAIL_USERNAME, settings.MAIL_PASSWORD)
        server.send_message(msg)
