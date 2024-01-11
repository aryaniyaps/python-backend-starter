from redmail.email.sender import EmailSender

from app.config import settings

if settings.email_username and settings.email_password:
    email_sender = EmailSender(
        host=settings.email_host,
        port=settings.email_port,
        username=settings.email_username,
        password=settings.email_password,
    )
else:
    email_sender = EmailSender(
        host=settings.email_host,
        port=settings.email_port,
    )
