from email.message import EmailMessage
from email.mime.text import MIMEText
from smtplib import SMTP

from app.config import settings


class EmailSender:
    def __init__(
        self,
        smtp_server: str,
        smtp_port: int,
        username: str,
        password: str,
    ) -> None:
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password

        # Connect to the SMTP server during initialization
        self.server = SMTP(self.smtp_server, self.smtp_port)
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
        message["From"] = self.username
        message["To"] = to
        message["Subject"] = subject
        # Attach the body as plain text
        message.attach(MIMEText(body, "plain"))
        if html_body:
            # Attach the HTML body
            message.attach(MIMEText(html_body, "html"))
        self.server.send_message(message)


email_sender = EmailSender(
    smtp_server=settings.smtp_server,
    smtp_port=settings.smtp_port,
    username=settings.email_username,
    password=settings.email_password.get_secret_value(),
)
