import smtplib
from email.mime.text import MIMEText
from app.core.config import settings

def send_reset_email(to_email: str, reset_token: str):
    reset_link = f"http://localhost:8000/auth/reset-password?token={reset_token}"
    subject = "Password Reset Request"
    body = f"Click the link below to reset your password:\n{reset_link}"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = settings.MAIL_FROM
    msg["To"] = to_email

    with smtplib.SMTP(settings.MAIL_SERVER, settings.MAIL_PORT) as server:
        server.starttls()
        server.login(settings.MAIL_USERNAME, settings.MAIL_PASSWORD)
        server.sendmail(settings.MAIL_FROM, to_email, msg.as_string())
