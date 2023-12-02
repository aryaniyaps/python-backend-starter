from jinja2 import Environment, FileSystemLoader, select_autoescape

from app.core.constants import APP_NAME, APP_URL, SUPPORT_EMAIL


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

reset_password_html = environment.get_template(
    name="reset_password/content.html",
)

reset_password_text = environment.get_template(
    name="reset_password/content.txt",
)
