from json import dumps, loads
from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import RedirectResponse
from fastapi_sso.sso.google import GoogleSSO

from app.auth.dependencies import get_auth_service
from app.auth.services import AuthService
from app.core.constants import OpenAPITag
from app.oauth.dependencies import get_google_sso

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
    google_sso: Annotated[
        GoogleSSO,
        Depends(
            dependency=get_google_sso,
        ),
    ],
    auth_service: Annotated[
        AuthService,
        Depends(
            dependency=get_auth_service,
        ),
    ],
) -> RedirectResponse:
    user = await google_sso.verify_and_process(request)

    if user is None:
        # TODO: raise error here
        raise Exception

    # TODO: create new service method to login or signup
    # Username must be created from display name, with max char limitations
    # in mind.
    # We should probably have a SocialConnection/ Identity model that allows
    # users to connect to multiple social accounts
    # authentication_token, user = await auth_service.register_user(
    #     email=user.email,
    #     username=data.username,
    #     password=data.password,
    #     request_ip=request_ip,
    #     user_agent=parse(user_agent),
    # )

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
