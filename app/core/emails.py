from email.message import EmailMessage
from email.mime.text import MIMEText
from smtplib import SMTP
from urllib.parse import urlparse

from app.config import settings


class EmailSender:
    def __init__(self, email_server: str, email_from: str) -> None:
        # Parse the email_server string
        parsed_url = urlparse(email_server)
        self.smtp_host = parsed_url.hostname
        self.smtp_port = parsed_url.port
        self.username = parsed_url.username
        self.password = parsed_url.password

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


email_sender = EmailSender(
    email_server=str(settings.email_server),
    email_from=settings.email_from,
)
