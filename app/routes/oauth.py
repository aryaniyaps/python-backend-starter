from json import dumps, loads
from typing import Annotated

from fastapi import APIRouter, Depends, Header, Query, Request
from fastapi.responses import RedirectResponse
from fastapi_sso.sso.base import SSOLoginError
from fastapi_sso.sso.google import GoogleSSO
from user_agents import parse

from app.config import settings
from app.dependencies.ip_address import get_ip_address
from app.dependencies.oauth import get_google_sso, get_oauth_service
from app.lib.constants import OpenAPITag
from app.lib.enums import AuthProviderType
from app.lib.errors import OauthAccountCreateError, OauthAccountLinkingError
from app.services.oauth import OAuthService
from app.utils.query_params import append_query_param

oauth_router = APIRouter(
    prefix="/oauth",
    tags=[OpenAPITag.INTERNAL],
)


@oauth_router.post("/google/login")
async def google_login(
    request: Request,
    redirect_to: Annotated[
        str,
        Query(
            description="The URL to redirect to after authentication.",
        ),
    ],
    google_sso: Annotated[
        GoogleSSO,
        Depends(
            dependency=get_google_sso,
        ),
    ],
) -> RedirectResponse:
    """Redirect the user to the Google sign in URL."""
    return await google_sso.get_login_redirect(
        state=dumps({"redirect_to": redirect_to}),
        redirect_uri=str(
            request.url_for(
                "google_callback",
            )
        ),
    )


@oauth_router.post("/google/callback")
async def google_callback(
    request: Request,
    user_agent: Annotated[str, Header()],
    request_ip: Annotated[
        str,
        Depends(
            dependency=get_ip_address,
        ),
    ],
    google_sso: Annotated[
        GoogleSSO,
        Depends(
            dependency=get_google_sso,
        ),
    ],
    oauth_service: Annotated[
        OAuthService,
        Depends(
            dependency=get_oauth_service,
        ),
    ],
) -> RedirectResponse:
    """Login or register the user with the access token received."""
    try:
        redirect_to = settings.default_oauth2_redirect_to

        if google_sso.state is not None:
            state = loads(google_sso.state)
            redirect_to = state.get(
                "redirect_to",
                settings.default_oauth2_redirect_to,
            )

        openid_user = await google_sso.verify_and_process(request)

        authentication_token = await oauth_service.login_or_register_user(
            openid_user=openid_user,
            provider=AuthProviderType.google,
            request_ip=request_ip,
            user_agent=parse(user_agent),
        )

        # Construct the redirect URL with the authentication token
        redirect_url = append_query_param(
            redirect_to, "authentication_token", authentication_token
        )

        return RedirectResponse(url=redirect_url)

    except (SSOLoginError, OauthAccountCreateError):
        redirect_url = append_query_param(redirect_to, "error_code", "login")
        return RedirectResponse(url=redirect_url)

    except OauthAccountLinkingError:
        redirect_url = append_query_param(
            redirect_to, "error_code", "account_not_linked"
        )
        return RedirectResponse(url=redirect_url)

    except Exception:  # noqa: BLE001
        redirect_url = append_query_param(redirect_to, "error_code", "unexpected")
        return RedirectResponse(url=redirect_url)
