import base64
from typing import Annotated

from fastapi import APIRouter, Depends, Header, Query, Request
from fastapi.responses import RedirectResponse
from fastapi_sso.sso.base import SSOBase, SSOLoginError
from fastapi_sso.sso.facebook import FacebookSSO
from fastapi_sso.sso.google import GoogleSSO
from orjson import dumps, loads
from user_agents import parse

from app.config import settings
from app.dependencies.ip_address import get_ip_address
from app.dependencies.oauth import get_facebook_sso, get_google_sso, get_oauth_service
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
    state_data = dumps({"redirect_to": redirect_to})
    return await google_sso.get_login_redirect(
        state=base64.b64encode(state_data).decode(),
        redirect_uri=str(
            request.url_for(
                "google_callback",
            )
        ),
    )


@oauth_router.post("/facebook/login")
async def facebook_login(
    request: Request,
    redirect_to: Annotated[
        str,
        Query(
            description="The URL to redirect to after authentication.",
        ),
    ],
    facebook_sso: Annotated[
        FacebookSSO,
        Depends(
            dependency=get_facebook_sso,
        ),
    ],
) -> RedirectResponse:
    """Redirect the user to the Facebook sign in URL."""
    state_data = dumps({"redirect_to": redirect_to})
    return await facebook_sso.get_login_redirect(
        state=base64.b64encode(state_data).decode(),
        redirect_uri=str(
            request.url_for(
                "facebook_callback",
            )
        ),
    )


async def handle_oauth_callback(
    request: Request,
    user_agent: str,
    request_ip: str,
    sso_provider: SSOBase,
    auth_provider: AuthProviderType,
    oauth_service: OAuthService,
) -> RedirectResponse:
    """Login or register the user with the given SSO provider."""
    try:
        redirect_to = settings.default_oauth2_redirect_to

        if sso_provider.state is not None:
            decoded_state = base64.b64decode(sso_provider.state)
            state = loads(decoded_state)
            redirect_to = state.get(
                "redirect_to",
                settings.default_oauth2_redirect_to,
            )

        openid_user = await sso_provider.verify_and_process(request)

        authentication_token = await oauth_service.login_or_register_user(
            openid_user=openid_user,
            provider=auth_provider,
            request_ip=request_ip,
            user_agent=parse(user_agent),
        )

        # Construct the redirect URL with the authentication token
        redirect_url = append_query_param(
            redirect_to, "authentication_token", authentication_token
        )

        return RedirectResponse(url=redirect_url)

    except SSOLoginError:
        redirect_url = append_query_param(redirect_to, "error_code", "oauth_callback")
        return RedirectResponse(url=redirect_url)

    except OauthAccountCreateError:
        redirect_url = append_query_param(
            redirect_to, "error_code", "oauth_account_create"
        )
        return RedirectResponse(url=redirect_url)

    except OauthAccountLinkingError:
        redirect_url = append_query_param(
            redirect_to, "error_code", "oauth_account_not_linked"
        )
        return RedirectResponse(url=redirect_url)


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
    return await handle_oauth_callback(
        request=request,
        user_agent=user_agent,
        request_ip=request_ip,
        sso_provider=google_sso,
        auth_provider=AuthProviderType.google,
        oauth_service=oauth_service,
    )


@oauth_router.post("/facebook/callback")
async def facebook_callback(
    request: Request,
    user_agent: Annotated[str, Header()],
    request_ip: Annotated[
        str,
        Depends(
            dependency=get_ip_address,
        ),
    ],
    facebook_sso: Annotated[
        FacebookSSO,
        Depends(
            dependency=get_facebook_sso,
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
    return await handle_oauth_callback(
        request=request,
        user_agent=user_agent,
        request_ip=request_ip,
        sso_provider=facebook_sso,
        auth_provider=AuthProviderType.facebook,
        oauth_service=oauth_service,
    )
