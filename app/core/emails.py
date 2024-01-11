from marrow.mailer import Mailer

from app.config import settings

mailer = Mailer(
    {
        "manager.use": "futures",
        "transport.use": "smtp",
        "transport.max_messages_per_connection": 5,
        "transport.tls": "optional",
        "transport.host": settings.email_host,
        "transport.port": settings.email_port,
        "transport.debug": settings.debug,
        "transport.username": settings.email_username,
        "transport.password": settings.email_password,
        "message.author": settings.email_from,
    }
)
