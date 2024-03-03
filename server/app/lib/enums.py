from enum import StrEnum


class RegisterFlowStep(StrEnum):
    EMAIL_VERIFICATION = "email_verification"
    WEBAUTHN_REGISTRATION = "webauthn_registration"
