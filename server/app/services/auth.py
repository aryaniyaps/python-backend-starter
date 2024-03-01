import base64
from datetime import UTC, datetime
from uuid import UUID, uuid4

import humanize
import orjson
from geoip2.database import Reader
from user_agents.parsers import UserAgent
from webauthn import (
    generate_authentication_options,
    generate_registration_options,
    verify_authentication_response,
    verify_registration_response,
)
from webauthn.helpers.structs import (
    AuthenticationCredential,
    AuthenticatorAttachment,
    AuthenticatorSelectionCriteria,
    PublicKeyCredentialCreationOptions,
    PublicKeyCredentialDescriptor,
    PublicKeyCredentialRequestOptions,
    PublicKeyCredentialType,
    RegistrationCredential,
    ResidentKeyRequirement,
    UserVerificationRequirement,
)

from app.config import settings
from app.lib.errors import InvalidInputError, UnauthenticatedError
from app.lib.geo_ip import get_city_location, get_geoip_city
from app.models.user_session import UserSession
from app.repositories.authentication_token import AuthenticationTokenRepo
from app.repositories.email_verification_code import EmailVerificationCodeRepo
from app.repositories.user import UserRepo
from app.repositories.user_session import UserSessionRepo
from app.repositories.webauthn_challenge import WebAuthnChallengeRepo
from app.repositories.webauthn_credential import WebAuthnCredentialRepo
from app.types.auth import AuthenticationResult, UserInfo
from app.worker import task_queue

# reference: https://github.com/maximousblk/passkeys-demo/blob/main/server.ts


class AuthService:
    def __init__(
        self,
        user_session_repo: UserSessionRepo,
        webauthn_credential_repo: WebAuthnCredentialRepo,
        webauthn_challenge_repo: WebAuthnChallengeRepo,
        authentication_token_repo: AuthenticationTokenRepo,
        user_repo: UserRepo,
        email_verification_code_repo: EmailVerificationCodeRepo,
        geoip_reader: Reader,
    ) -> None:
        self._user_session_repo = user_session_repo
        self._webauthn_credential_repo = webauthn_credential_repo
        self._webauthn_challenge_repo = webauthn_challenge_repo
        self._authentication_token_repo = authentication_token_repo
        self._user_repo = user_repo
        self._email_verification_code_repo = email_verification_code_repo
        self._geoip_reader = geoip_reader

    async def send_email_verification_request(
        self,
        *,
        email: str,
        user_agent: UserAgent,
        request_ip: str,
    ) -> None:
        """Send an email verification request to the given email."""
        if (
            await self._user_repo.get_by_email(
                email=email,
            )
            is not None
        ):
            raise InvalidInputError(
                message="User with that email already exists.",
            )

        verification_token = await self._email_verification_code_repo.create(
            email=email,
        )

        # send verification request email
        await task_queue.enqueue(
            "send_email_verification_request_email",
            receiver=email,
            verification_token=verification_token,
            device=user_agent.get_device(),
            browser_name=user_agent.get_browser(),
            location=get_city_location(
                city=get_geoip_city(
                    ip_address=request_ip,
                    geoip_reader=self._geoip_reader,
                ),
            ),
            ip_address=request_ip,
        )

    async def generate_registration_options(
        self,
        *,
        email: str,
        verification_code: str,
        display_name: str,
    ) -> PublicKeyCredentialCreationOptions:
        """Generate options for registering a credential."""
        email_verification_code = await self._email_verification_code_repo.get(
            verification_code=verification_code,
            email=email,
        )

        if email_verification_code is None or email_verification_code.email != email:
            raise InvalidInputError(
                message="Invalid email verification code passed.",
            )

        # delete existing email verification codes
        await self._email_verification_code_repo.delete_all(email=email)

        # generate user ID (UUID)
        user_id = uuid4()

        registration_options = generate_registration_options(
            rp_id=settings.rp_id,
            rp_name=settings.rp_name,
            user_id=user_id.bytes,
            user_name=email,
            user_display_name=display_name,
            authenticator_selection=AuthenticatorSelectionCriteria(
                authenticator_attachment=AuthenticatorAttachment.PLATFORM,
                user_verification=UserVerificationRequirement.REQUIRED,
                resident_key=ResidentKeyRequirement.PREFERRED,
                require_resident_key=False,
            ),
        )

        # store challenge server-side
        await self._webauthn_challenge_repo.create(
            challenge=registration_options.challenge.decode(),
            user_id=user_id,
        )

        return registration_options

    async def verify_registration_response(
        self,
        *,
        email: str,
        display_name: str,
        credential: RegistrationCredential,
        request_ip: str,
        user_agent: UserAgent,
    ) -> AuthenticationResult:
        """Verify the authenticator's response for registration."""
        client_data = orjson.loads(
            base64.b64decode(credential.response.client_data_json)
        )

        challenge = client_data["challenge"]

        user_id = await self._webauthn_challenge_repo.get(
            challenge=challenge,
        )

        if user_id is None:
            raise InvalidInputError(
                message="Challenge response doesn't match.",
            )

        verified_registration = verify_registration_response(
            credential=credential,
            expected_challenge=challenge,
            expected_rp_id=settings.rp_id,
            expected_origin=settings.rp_expected_origin,
        )

        if not verified_registration.user_verified:
            raise InvalidInputError(
                message="Couldn't verify user.",
            )

        user = await self._user_repo.create(
            user_id=user_id,
            email=email,
            display_name=display_name,
        )

        # delete challenge server-side
        await self._webauthn_challenge_repo.delete(challenge=challenge)

        await self._webauthn_credential_repo.create(
            user_id=user.id,
            credential_id=str(verified_registration.credential_id),
            public_key=str(verified_registration.credential_public_key),
            sign_count=verified_registration.sign_count,
            backed_up=verified_registration.credential_backed_up,
            device_type=verified_registration.credential_device_type,
            transports=credential.response.transports,
        )

        user_session = await self._user_session_repo.create(
            user_id=user.id,
            ip_address=request_ip,
            user_agent=user_agent,
        )

        authentication_token = await self._authentication_token_repo.create(
            user_id=user.id,
            user_session_id=user_session.id,
        )

        await task_queue.enqueue(
            "send_onboarding_email",
            receiver=user.email,
            email=user.email,
        )

        return {
            "authentication_token": authentication_token,
            "user": user,
        }

    async def generate_login_options(
        self, *, email: str
    ) -> PublicKeyCredentialRequestOptions:
        """Generate options for retrieving a credential."""
        existing_user = await self._user_repo.get_by_email(
            email=email,
        )

        if existing_user is None:
            raise InvalidInputError(
                message="User with that email doesn't exist.",
            )

        existing_credentials = await self._webauthn_credential_repo.get_all(
            user_id=existing_user.id,
        )

        authentication_options = generate_authentication_options(
            rp_id=settings.rp_id,
            user_verification=UserVerificationRequirement.DISCOURAGED,
            allow_credentials=[
                PublicKeyCredentialDescriptor(
                    id=credential.id.encode(),
                    type=PublicKeyCredentialType.PUBLIC_KEY,
                    transports=credential.transports,
                )
                for credential in existing_credentials
            ],
        )

        # store challenge server-side
        await self._webauthn_challenge_repo.create(
            challenge=authentication_options.challenge.decode(),
            user_id=existing_user.id,
        )

        return authentication_options

    async def verify_login_response(
        self,
        *,
        credential: AuthenticationCredential,
        request_ip: str,
        user_agent: UserAgent,
    ) -> AuthenticationResult:
        """Verify the authenticator's response for authentication."""
        # TODO: check if its okay if we don't use the user_handle here
        # user_id = credential.response.user_handle

        client_data = orjson.loads(
            base64.b64decode(credential.response.client_data_json)
        )

        challenge = client_data["challenge"]

        user_id = await self._webauthn_challenge_repo.get(challenge=challenge)

        if user_id is None:
            raise InvalidInputError(
                message="Challenge response doesn't match.",
            )

        existing_user = await self._user_repo.get(user_id=user_id)

        if existing_user is None:
            # TODO: handle error here
            raise Exception

        existing_credential = await self._webauthn_credential_repo.get(
            credential_id=credential.id,
            user_id=existing_user.id,
        )

        if existing_credential is None:
            raise InvalidInputError(
                message="Webauthn credential doesn't exist.",
            )

        verified_authentication = verify_authentication_response(
            credential=credential,
            expected_challenge=challenge.encode(),
            expected_rp_id=settings.rp_id,
            expected_origin=settings.rp_expected_origin,
            credential_current_sign_count=existing_credential.sign_count,
            credential_public_key=existing_credential.public_key.encode(),
        )

        # delete challenge server-side
        await self._webauthn_challenge_repo.delete(challenge=challenge)

        # update credential sign count
        await self._webauthn_credential_repo.update(
            webauthn_credential=existing_credential,
            sign_count=verified_authentication.new_sign_count,
        )

        if not await self._user_session_repo.check_if_device_exists(
            user_id=existing_user.id,
            device=user_agent.device,
        ):
            await task_queue.enqueue(
                "send_new_login_device_detected_email",
                receiver=existing_user.email,
                email=existing_user.email,
                login_timestamp=humanize.naturaldate(datetime.now(UTC)),
                device=user_agent.get_device(),
                browser_name=user_agent.get_browser(),
                location=get_city_location(
                    city=get_geoip_city(
                        ip_address=request_ip,
                        geoip_reader=self._geoip_reader,
                    ),
                ),
                ip_address=request_ip,
            )

        user_session = await self._user_session_repo.create(
            user_id=existing_user.id,
            ip_address=request_ip,
            user_agent=user_agent,
        )

        authentication_token = await self._authentication_token_repo.create(
            user_id=existing_user.id,
            user_session_id=user_session.id,
        )

        return {
            "authentication_token": authentication_token,
            "user": existing_user,
        }

    async def get_user_sessions(self, *, user_id: UUID) -> list[UserSession]:
        """Get user sessions for the given user ID."""
        return await self._user_session_repo.get_all(
            user_id=user_id,
        )

    async def logout_user(
        self,
        *,
        authentication_token: str,
        user_session_id: UUID,
        user_id: UUID,
        remember_session: bool,
    ) -> None:
        """Logout the user."""
        await self._authentication_token_repo.delete(
            authentication_token=authentication_token,
            user_id=user_id,
        )
        if remember_session:
            await self._user_session_repo.update(
                user_session_id=user_session_id,
                logged_out_at=datetime.now(UTC),
            )
        else:
            await self._user_session_repo.delete(
                user_session_id=user_session_id,
                user_id=user_id,
            )

    async def get_user_info_for_authentication_token(
        self, authentication_token: str
    ) -> UserInfo:
        """Verify the given authentication token and return the corresponding user info."""
        user_info = await self._authentication_token_repo.get_user_info(
            authentication_token=authentication_token,
        )

        if not user_info:
            raise UnauthenticatedError(
                message="Invalid authentication token provided.",
            )
        return user_info