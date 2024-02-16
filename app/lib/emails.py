from redmail.email.sender import EmailSender

from app.config import settings

if settings.email_username and settings.email_password:
    email_sender = EmailSender(
        host=settings.email_host,
        port=settings.email_port,
        password=settings.email_password.get_secret_value(),
        username=settings.email_username,
    )
else:
    email_sender = EmailSender(
        host=settings.email_host,
        port=settings.email_port,
    )
