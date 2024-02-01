from json import dumps, loads
from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request, status
from fastapi.responses import RedirectResponse
from httpx_oauth.integrations.fastapi import OAuth2AuthorizeCallback
from httpx_oauth.oauth2 import OAuth2Token

from app.core.constants import OpenAPITag

from .clients import google_oauth_client

oauth_router = APIRouter(
    prefix="/oauth",
    tags=[OpenAPITag.INTERNAL],
)

oauth2_authorize_callback = OAuth2AuthorizeCallback(
    google_oauth_client, route_name="google_callback"
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
) -> RedirectResponse:
    authorization_url = await google_oauth_client.get_authorization_url(
        redirect_uri=str(request.url_for("google_callback")),
        state=dumps({"redirect_to": redirect_to}),
    )
    return RedirectResponse(
        authorization_url,
        status.HTTP_303_SEE_OTHER,
    )


@oauth_router.post("/google/callback")
async def google_callback(
    access_token_state: Annotated[
        tuple[OAuth2Token, str | None],
        Depends(
            dependency=oauth2_authorize_callback,
        ),
    ]
) -> RedirectResponse:
    access_token, raw_state = access_token_state

    if raw_state is not None:
        state = loads(raw_state)
        redirect_to = state.get("redirect_to", "DEFAULT_REDIRECT_TO")
    else:
        redirect_to = "DEFAULT_REDIRECT_TO"

    # TODO: get user info with access token and login/ signup user here
    # create user session and return authentication token here via query params
    # if any error occurs, pass the error via query params
    return RedirectResponse(redirect_to)
