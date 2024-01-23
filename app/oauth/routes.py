from typing import Annotated

from fastapi import APIRouter, Depends, Request, status
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
async def google_login(request: Request) -> RedirectResponse:
    authorization_url = await google_oauth_client.get_authorization_url(
        redirect_uri=str(request.url_for("google_callback")),
        # probably pass the redirect url in the state
        state={},
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
) -> None:
    # TODO: login user or sign them up with the userinfo information here
    # then redirect to the frontend?
    pass
