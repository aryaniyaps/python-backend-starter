from enum import StrEnum


class RegisterFlowStep(StrEnum):
    EMAIL_VERIFICATION = "email_verification"
    WEBAUTHN_START = "webauthn_start"
    WEBAUTHN_FINISH = "webauthn_finish"
