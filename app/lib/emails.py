from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from aiosmtplib import SMTP

from app.config import settings

if settings.email_username and settings.email_password:
    smtp_client = SMTP(
        hostname=settings.email_host,
        port=settings.email_port,
        password=settings.email_password.get_secret_value(),
        username=settings.email_username,
    )
else:
    smtp_client = SMTP(
        hostname=settings.email_host,
        port=settings.email_port,
    )


async def send_email(
    sender: str,
    receiver: str,
    subject: str,
    text: str,
    html: str,
) -> None:
    """Send an email."""
    message = MIMEMultipart("alternative")
    message["From"] = sender
    message["To"] = receiver
    message["Subject"] = subject
    message.attach(MIMEText(text, "plain"))
    message.attach(MIMEText(html, "html"))

    async with smtp_client:
        await smtp_client.send_message(message)
