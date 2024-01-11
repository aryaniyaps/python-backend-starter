from email.message import EmailMessage


class MockSMTP:
    """Mock SMTP server used for testing."""

    messages: list[EmailMessage] = []

    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.username = None
        self.password = None

    def starttls(self) -> None:
        # Called only if use_startls is True
        return

    def login(self, username: str, password: str) -> None:
        # Log in to the server (if credentials passed)
        self.username = username
        self.password = password
        return

    def send_message(self, msg: EmailMessage) -> None:
        # Instead of sending, we just store the message
        self.messages.append(msg)

    def quit(self) -> None:
        # Closing the connection
        return
