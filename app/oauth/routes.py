from json import dumps, loads
from typing import Annotated

from fastapi import APIRouter, Depends, Header, Query, Request
from fastapi.responses import RedirectResponse
from fastapi_sso.sso.google import GoogleSSO
from user_agents import parse

from app.core.constants import OpenAPITag
from app.core.dependencies import get_ip_address
from app.oauth.dependencies import get_google_sso, get_oauth_service
from app.oauth.services import OAuthService

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
    # TODO: pass the request ip_address and useragent also in the state
    # after signing it with itsdangerous. This will be needed for user creation/ login
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
        Depends(dependency=get_ip_address),
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
    openid_user = await google_sso.verify_and_process(request)

    if openid_user is None:
        # TODO: raise error here
        raise Exception

    # TODO: We should probably have a SocialConnection/ Identity model that allows
    # users to connect to multiple social accounts
    # TODO: check if the ip address and user agent are that of google's servers or
    # of the client that initiated the oauth workflow
    authentication_token, user = await oauth_service.login_or_register_user(
        openid_user=openid_user,
        request_ip=request_ip,
        user_agent=parse(user_agent),
    )

    # TODO: get user info with access token and login/ signup user here
    # create user session and return authentication token here via query params
    # if any error occurs, pass the error via query params
    if google_sso.state is not None:
        state = loads(google_sso.state)
        redirect_to = state.get("redirect_to", "")
    else:
        redirect_to = ""

    return RedirectResponse(
        url=redirect_to,
    )
