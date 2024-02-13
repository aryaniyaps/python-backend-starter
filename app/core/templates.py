from datetime import timedelta

from humanize import naturaldelta
from jinja2 import Environment, FileSystemLoader, select_autoescape

from app.core.constants import (
    APP_NAME,
    APP_URL,
    EMAIL_VERIFICATION_TOKEN_EXPIRES_IN,
    PASSWORD_RESET_TOKEN_EXPIRES_IN,
    SUPPORT_EMAIL,
)


def register_globals(environment: Environment) -> None:
    """Register global variables for the environment."""
    environment.globals["app_name"] = APP_NAME
    environment.globals["app_url"] = APP_URL
    environment.globals["support_email"] = SUPPORT_EMAIL


def create_environment() -> Environment:
    """Initialize an environment for template rendering."""
    environment = Environment(
        loader=FileSystemLoader(
            "templates",
        ),
        autoescape=select_autoescape(),
    )
    register_globals(environment)
    return environment


environment = create_environment()

# email verification request templates

email_verification_request_subject = environment.get_template(
    name="emails/email-verification-request/subject.txt",
)

email_verification_request_html = environment.get_template(
    name="emails/email-verification-request/body.html",
    globals={
        "token_expires_in": naturaldelta(
            timedelta(
                seconds=EMAIL_VERIFICATION_TOKEN_EXPIRES_IN,
            ),
        ),
    },
)

email_verification_request_text = environment.get_template(
    name="emails/email-verification-request/body.txt",
    globals={
        "token_expires_in": naturaldelta(
            timedelta(
                seconds=EMAIL_VERIFICATION_TOKEN_EXPIRES_IN,
            ),
        ),
    },
)

# password reset request templates

reset_password_request_subject = environment.get_template(
    name="emails/reset-password-request/subject.txt",
)

reset_password_request_html = environment.get_template(
    name="emails/reset-password-request/body.html",
    globals={
        "token_expires_in": naturaldelta(
            timedelta(
                seconds=PASSWORD_RESET_TOKEN_EXPIRES_IN,
            ),
        ),
    },
)

reset_password_request_text = environment.get_template(
    name="emails/reset-password-request/body.txt",
    globals={
        "token_expires_in": naturaldelta(
            timedelta(
                seconds=PASSWORD_RESET_TOKEN_EXPIRES_IN,
            ),
        ),
    },
)

# password reset templates

reset_password_subject = environment.get_template(
    name="emails/reset-password/subject.txt",
)

reset_password_html = environment.get_template(
    name="emails/reset-password/body.html",
)

reset_password_text = environment.get_template(
    name="emails/reset-password/body.txt",
)

# onboarding templates

onboarding_subject = environment.get_template(
    name="emails/onboarding/subject.txt",
)

onboarding_html = environment.get_template(
    name="emails/onboarding/body.html",
)

onboarding_text = environment.get_template(
    name="emails/onboarding/body.txt",
)


# new login location detected templates

new_login_location_subject = environment.get_template(
    name="emails/new-login-location/subject.txt",
)

new_login_location_html = environment.get_template(
    name="emails/new-login-location/body.html",
)

new_login_location_text = environment.get_template(
    name="emails/new-login-location/body.txt",
)
