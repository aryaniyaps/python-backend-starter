from fastapi import APIRouter, Request

from app.core.constants import OpenAPITag
from app.core.oauth import oauth_client

oauth_router = APIRouter(
    prefix="/oauth",
    tags=[OpenAPITag.INTERNAL],
)


@oauth_router.post("/google/login")
async def google_login(request: Request) -> None:
    callback_uri = request.url_for("google_callback")
    return await oauth_client.google.authorize_redirect(
        request,
        callback_uri,
    )


@oauth_router.post("/google/callback")
async def google_callback(request: Request) -> None:
    token = await oauth_client.google.authorize_access_token(request)
    user = token.get("userinfo")
    # TODO: login user or sign them up with the userinfo information here
    # then redirect to the frontend?
