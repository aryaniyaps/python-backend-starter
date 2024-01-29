from datetime import timedelta

from humanize import naturaldelta
from jinja2 import Environment, FileSystemLoader, select_autoescape

from app.core.constants import (
    APP_NAME,
    APP_URL,
    PASSWORD_RESET_TOKEN_EXPIRES_IN,
    SUPPORT_EMAIL,
)


def add_globals(environment: Environment) -> None:
    """Add global variables to the environment."""
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
    add_globals(environment)
    return environment


environment = create_environment()

# password reset templates

reset_password_subject = environment.get_template(
    name="emails/reset-password/subject.txt",
)

reset_password_html = environment.get_template(
    name="emails/reset-password/body.html",
    globals={
        "token_expires_in": naturaldelta(
            timedelta(
                seconds=PASSWORD_RESET_TOKEN_EXPIRES_IN,
            ),
        ),
    },
)

reset_password_text = environment.get_template(
    name="emails/reset-password/body.txt",
    globals={
        "token_expires_in": naturaldelta(
            timedelta(
                seconds=PASSWORD_RESET_TOKEN_EXPIRES_IN,
            ),
        ),
    },
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
