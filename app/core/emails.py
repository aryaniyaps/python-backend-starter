from email.message import EmailMessage
from email.mime.text import MIMEText
from functools import lru_cache
from smtplib import SMTP
from typing import Generator

from pydantic_core import Url

from app.config import settings


class EmailSender:
    def __init__(self, email_server: Url, email_from: str) -> None:
        self.smtp_host = email_server.host
        self.smtp_port = email_server.port
        self.username = email_server.username
        self.password = email_server.password

        self.email_from = email_from

        assert self.smtp_host and self.smtp_port, (
            "Invalid SMTP host or port provided.",
        )

        # Connect to the SMTP server during initialization
        self.server = SMTP(self.smtp_host, self.smtp_port)
        if self.username and self.password:
            self.server.starttls()
            self.server.login(self.username, self.password)

    def send_email(
        self,
        to: str,
        subject: str,
        body: str,
        html_body: str | None = None,
    ) -> None:
        """Send an Email to the specified address."""
        message = EmailMessage()
        message["From"] = self.email_from
        message["To"] = to
        message["Subject"] = subject
        # Attach the body as plain text
        message.attach(MIMEText(body, "plain"))
        if html_body:
            # Attach the HTML body
            message.attach(MIMEText(html_body, "html"))
        self.server.send_message(message)

    def close_connection(self) -> None:
        """Close the SMTP connection."""
        if self.server:
            self.server.quit()


@lru_cache
def get_email_sender() -> Generator[EmailSender, None, None]:
    """Get the email sender."""
    email_sender = EmailSender(
        email_server=settings.email_server,
        email_from=settings.email_from,
    )
    yield email_sender
    email_sender.close_connection()
