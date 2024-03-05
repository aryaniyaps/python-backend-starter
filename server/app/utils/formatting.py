def redact_email(email: str) -> str:
    """
    Redact the given email.

    Replaces the characters in the username with asterisks,
    except for the first and last character.
    """
    # Split the email address into username and domain
    username, domain = email.split("@")

    # Redact the username
    redacted_username = username[0] + "*" * (len(username) - 2) + username[-1]

    # Reconstruct the redacted email
    return redacted_username + "@" + domain
