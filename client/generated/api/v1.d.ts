/**
 * This file was auto-generated by openapi-typescript.
 * Do not make direct changes to the file.
 */

export interface paths {
  '/health/': {
    /**
     * Check the health status of the application.
     * @description Provides information about the health status of the application.
     */
    get: operations['Tag.HEALTH-check_health'];
  };
  '/users/@me': {
    /**
     * Get the current user.
     * @description Get the current user.
     */
    get: operations['ITag.USERS-get_current_user'];
    /**
     * Update the current user.
     * @description Update the current user.
     */
    patch: operations['ITag.USERS-update_current_user'];
  };
  '/users/@me/email-change-request': {
    /**
     * Send an email change request.
     * @description Send an email change request.
     */
    post: operations['ITag.USERS-request_current_user_email_change'];
  };
  '/users/@me/email': {
    /**
     * Change the current user's email.
     * @description Change the current user's email.
     */
    patch: operations['ITag.USERS-change_current_user_email'];
  };
  '/users/{user_id}': {
    /**
     * Get the user with the given ID.
     * @description Get the user with the given ID.
     */
    get: operations['ITag.USERS-get_user'];
  };
  '/auth/register/flow/start': {
    /**
     * Start a register flow.
     * @description Start a register flow.
     */
    post: operations['ENTICATION-start_register_flow'];
  };
  '/auth/register/flow/verify': {
    /**
     * Verify a register flow.
     * @description Verify a register flow.
     */
    post: operations['ENTICATION-verify_register_flow'];
  };
  '/auth/register/flow/webauthn-start': {
    /**
     * Start the webauthn registration in the register flow.
     * @description Start the webauthn registration in the register flow.
     */
    post: operations['ENTICATION-start_webauthn_register_flow'];
  };
  '/auth/register/flow/webauthn-finish': {
    /**
     * Finish the webauthn registration in the register flow.
     * @description Finish the webauthn registration in the register flow.
     */
    post: operations['ENTICATION-finish_webauthn_register_flow'];
  };
  '/auth/login/start': {
    /**
     * Login Options
     * @description Generate options for retrieving a credential.
     */
    post: operations['ENTICATION-login_options'];
  };
  '/auth/login/finish': {
    /**
     * Login Verification
     * @description Verify the authenticator's response for login.
     */
    post: operations['ENTICATION-login_verification'];
  };
  '/auth/webauthn-credentials': {
    /**
     * Create Webauthn Credential
     * @description Create a new webauthn credential.
     */
    post: operations['ENTICATION-create_webauthn_credential'];
  };
  '/auth/logout': {
    /**
     * Logout the current user.
     * @description Logout the current user.
     */
    post: operations['ENTICATION-delete_current_user_session'];
  };
  '/auth/sessions': {
    /**
     * Get the current user's sessions.
     * @description Get the current user's user sessions.
     */
    get: operations['ENTICATION-get_user_sessions'];
  };
}

export type webhooks = Record<string, never>;

export interface components {
  schemas: {
    /**
     * AttestationConveyancePreference
     * @description The Relying Party's interest in receiving an attestation statement.
     *
     * Members:
     *     `NONE`: The Relying Party isn't interested in receiving an attestation statement
     *     `INDIRECT`: The Relying Party is interested in an attestation statement, but the client is free to generate it as it sees fit
     *     `DIRECT`: The Relying Party is interested in an attestation statement generated directly by the authenticator
     *     `ENTERPRISE`: The Relying Party is interested in a statement with identifying information. Typically used within organizations
     *
     * https://www.w3.org/TR/webauthn-2/#enum-attestation-convey
     * @enum {string}
     */
    AttestationConveyancePreference:
      | 'none'
      | 'indirect'
      | 'direct'
      | 'enterprise';
    /** AuthenticateUserResult */
    AuthenticateUserResult: {
      /**
       * Authentication Token
       * @description The authentication token generated upon successful login.
       */
      authenticationToken: string;
      /** @description The logged in user. */
      user: components['schemas']['UserSchema'];
    };
    /** AuthenticationCredential */
    AuthenticationCredential: {
      /** Id */
      id: string;
      /**
       * Rawid
       * Format: binary
       */
      rawId: string;
      response: components['schemas']['AuthenticatorAssertionResponse'];
      authenticatorAttachment?:
        | components['schemas']['AuthenticatorAttachment']
        | null;
      /**
       * Type
       * @default public-key
       * @constant
       */
      type?: 'public-key';
    };
    /** AuthenticatorAssertionResponse */
    AuthenticatorAssertionResponse: {
      /**
       * Clientdatajson
       * Format: binary
       */
      clientDataJson: string;
      /**
       * Authenticatordata
       * Format: binary
       */
      authenticatorData: string;
      /**
       * Signature
       * Format: binary
       */
      signature: string;
      /** Userhandle */
      userHandle?: string | null;
    };
    /**
     * AuthenticatorAttachment
     * @description How an authenticator is connected to the client/browser.
     *
     * Members:
     *     `PLATFORM`: A non-removable authenticator, like TouchID or Windows Hello
     *     `CROSS_PLATFORM`: A "roaming" authenticator, like a YubiKey
     *
     * https://www.w3.org/TR/webauthn-2/#enumdef-authenticatorattachment
     * @enum {string}
     */
    AuthenticatorAttachment: 'platform' | 'cross-platform';
    /** AuthenticatorAttestationResponse */
    AuthenticatorAttestationResponse: {
      /**
       * Clientdatajson
       * Format: binary
       */
      clientDataJson: string;
      /**
       * Attestationobject
       * Format: binary
       */
      attestationObject: string;
      /** Transports */
      transports?: components['schemas']['AuthenticatorTransport'][] | null;
    };
    /** AuthenticatorSelectionCriteria */
    AuthenticatorSelectionCriteria: {
      authenticator_attachment?:
        | components['schemas']['AuthenticatorAttachment']
        | null;
      resident_key?: components['schemas']['ResidentKeyRequirement'] | null;
      /**
       * Require Resident Key
       * @default false
       */
      require_resident_key?: boolean | null;
      /** @default preferred */
      user_verification?:
        | components['schemas']['UserVerificationRequirement']
        | null;
    };
    /**
     * AuthenticatorTransport
     * @description How an authenticator communicates to the client/browser.
     *
     * Members:
     *     `USB`: USB wired connection
     *     `NFC`: Near Field Communication
     *     `BLE`: Bluetooth Low Energy
     *     `INTERNAL`: Direct connection (read: a platform authenticator)
     *     `CABLE`: Cloud Assisted Bluetooth Low Energy
     *     `HYBRID`: A combination of (often separate) data-transport and proximity mechanisms
     *
     * https://www.w3.org/TR/webauthn-2/#enum-transport
     * @enum {string}
     */
    AuthenticatorTransport:
      | 'usb'
      | 'nfc'
      | 'ble'
      | 'internal'
      | 'cable'
      | 'hybrid';
    /**
     * COSEAlgorithmIdentifier
     * @description Various registered values indicating cryptographic algorithms that may be used in credential responses
     *
     * Members:
     *     `ECDSA_SHA_256`
     *     `EDDSA`
     *     `ECDSA_SHA_512`
     *     `RSASSA_PSS_SHA_256`
     *     `RSASSA_PSS_SHA_384`
     *     `RSASSA_PSS_SHA_512`
     *     `RSASSA_PKCS1_v1_5_SHA_256`
     *     `RSASSA_PKCS1_v1_5_SHA_384`
     *     `RSASSA_PKCS1_v1_5_SHA_512`
     *     `RSASSA_PKCS1_v1_5_SHA_1`
     *
     * https://www.w3.org/TR/webauthn-2/#sctn-alg-identifier
     * https://www.iana.org/assignments/cose/cose.xhtml#algorithms
     * @enum {integer}
     */
    COSEAlgorithmIdentifier:
      | -7
      | -8
      | -36
      | -37
      | -38
      | -39
      | -257
      | -258
      | -259
      | -65535;
    /** ChangeUserEmailInput */
    ChangeUserEmailInput: {
      /**
       * Email
       * Format: email
       * @description The new email address for the user.
       */
      email: string;
      /**
       * Verification Code
       * Format: password
       * @description The verification code for the email.
       */
      verificationCode: string;
    };
    /** ChangeUserEmailRequestInput */
    ChangeUserEmailRequestInput: {
      /**
       * Email
       * Format: email
       * @description The new email address for the user.
       */
      email: string;
      /**
       * Currentpassword
       * Format: password
       * @description The password associated with the user.
       */
      currentPassword: string;
    };
    /** CreateWebAuthnCredentialInput */
    CreateWebAuthnCredentialInput: Record<string, never>;
    /** HealthCheckResult */
    HealthCheckResult: {
      /**
       * Status
       * @description The status of the application.
       * @constant
       */
      status: 'OK';
    };
    /** InvalidInputErrorResult */
    InvalidInputErrorResult: {
      /**
       * Message
       * @description A human readable message describing the error.
       */
      message: string;
    };
    /** LoginOptionsInput */
    LoginOptionsInput: {
      /**
       * Email
       * Format: email
       */
      email: string;
    };
    /** LoginVerificationInput */
    LoginVerificationInput: {
      /** Credential */
      credential: string;
    };
    /** LogoutInput */
    LogoutInput: {
      /**
       * Remember Session
       * @description Whether the current user's session should be remembered.
       * @default true
       */
      rememberSession?: boolean;
    };
    /** PartialUserSchema */
    PartialUserSchema: {
      /**
       * Id
       * Format: uuid
       * @description The ID of the user.
       */
      id: string;
      /**
       * Username
       * @description The username of the user.
       */
      username: string;
      /**
       * Created At
       * Format: date-time
       * @description When the user was created.
       */
      createdAt: string;
      /**
       * Updated At
       * @description When the user was last updated.
       */
      updatedAt: string | null;
    };
    /** PublicKeyCredentialCreationOptions */
    PublicKeyCredentialCreationOptions: {
      rp: components['schemas']['PublicKeyCredentialRpEntity'];
      user: components['schemas']['PublicKeyCredentialUserEntity'];
      /**
       * Challenge
       * Format: binary
       */
      challenge: string;
      /** Pub Key Cred Params */
      pub_key_cred_params: components['schemas']['PublicKeyCredentialParameters'][];
      /** Timeout */
      timeout?: number | null;
      /** Exclude Credentials */
      exclude_credentials?:
        | components['schemas']['PublicKeyCredentialDescriptor'][]
        | null;
      authenticator_selection?:
        | components['schemas']['AuthenticatorSelectionCriteria']
        | null;
      /** @default none */
      attestation?: components['schemas']['AttestationConveyancePreference'];
    };
    /** PublicKeyCredentialDescriptor */
    PublicKeyCredentialDescriptor: {
      /**
       * Id
       * Format: binary
       */
      id: string;
      /**
       * Type
       * @default public-key
       * @constant
       */
      type?: 'public-key';
      /** Transports */
      transports?: components['schemas']['AuthenticatorTransport'][] | null;
    };
    /** PublicKeyCredentialParameters */
    PublicKeyCredentialParameters: {
      /**
       * Type
       * @constant
       */
      type: 'public-key';
      alg: components['schemas']['COSEAlgorithmIdentifier'];
    };
    /** PublicKeyCredentialRequestOptions */
    PublicKeyCredentialRequestOptions: {
      /**
       * Challenge
       * Format: binary
       */
      challenge: string;
      /** Timeout */
      timeout?: number | null;
      /** Rp Id */
      rp_id?: string | null;
      /** Allow Credentials */
      allow_credentials?:
        | components['schemas']['PublicKeyCredentialDescriptor'][]
        | null;
      /** @default preferred */
      user_verification?:
        | components['schemas']['UserVerificationRequirement']
        | null;
    };
    /** PublicKeyCredentialRpEntity */
    PublicKeyCredentialRpEntity: {
      /** Name */
      name: string;
      /** Id */
      id?: string | null;
    };
    /** PublicKeyCredentialUserEntity */
    PublicKeyCredentialUserEntity: {
      /**
       * Id
       * Format: binary
       */
      id: string;
      /** Name */
      name: string;
      /** Display Name */
      display_name: string;
    };
    /** RateLimitExceededErrorResult */
    RateLimitExceededErrorResult: {
      /**
       * Message
       * @description A human readable message describing the error.
       */
      message: string;
      /**
       * Is Primary
       * @description Whether the primary rate limiter was exceeded.
       */
      isPrimary: boolean;
    };
    /** RegisterFlowStartInput */
    RegisterFlowStartInput: {
      /**
       * Email
       * Format: email
       */
      email: string;
    };
    /** RegisterFlowStartResult */
    RegisterFlowStartResult: {
      /**
       * Flowid
       * Format: uuid
       */
      flowId: string;
    };
    /** RegisterFlowVerifyInput */
    RegisterFlowVerifyInput: {
      /**
       * Flowid
       * Format: uuid
       */
      flowId: string;
      /** Verificationcode */
      verificationCode: string;
    };
    /** RegisterFlowVerifyResult */
    RegisterFlowVerifyResult: {
      /**
       * Flowid
       * Format: uuid
       */
      flowId: string;
    };
    /** RegisterFlowWebAuthnFinishInput */
    RegisterFlowWebAuthnFinishInput: {
      /**
       * Flowid
       * Format: uuid
       */
      flowId: string;
      /** Displayname */
      displayName: string;
      /** Credential */
      credential: string;
    };
    /** RegisterFlowWebAuthnFinishResult */
    RegisterFlowWebAuthnFinishResult: {
      user: components['schemas']['UserSchema'];
      /**
       * Authentication Token
       * @description The authentication token generated upon successful registration.
       */
      authenticationToken: string;
    };
    /** RegisterFlowWebAuthnStartInput */
    RegisterFlowWebAuthnStartInput: {
      /**
       * Flowid
       * Format: uuid
       */
      flowId: string;
      /** Displayname */
      displayName: string;
    };
    /** RegistrationCredential */
    RegistrationCredential: {
      /** Id */
      id: string;
      /**
       * Rawid
       * Format: binary
       */
      rawId: string;
      response: components['schemas']['AuthenticatorAttestationResponse'];
      authenticatorAttachment?:
        | components['schemas']['AuthenticatorAttachment']
        | null;
      /**
       * Type
       * @default public-key
       * @constant
       */
      type?: 'public-key';
    };
    /**
     * ResidentKeyRequirement
     * @description The Relying Party's preference for the authenticator to create a dedicated "client-side" credential for it. Requiring an authenticator to store a dedicated credential should not be done lightly due to the limited storage capacity of some types of authenticators.
     *
     * Members:
     *     `DISCOURAGED`: The authenticator should not create a dedicated credential
     *     `PREFERRED`: The authenticator can create and store a dedicated credential, but if it doesn't that's alright too
     *     `REQUIRED`: The authenticator MUST create a dedicated credential. If it cannot, the RP is prepared for an error to occur.
     *
     * https://www.w3.org/TR/webauthn-2/#enum-residentKeyRequirement
     * @enum {string}
     */
    ResidentKeyRequirement: 'discouraged' | 'preferred' | 'required';
    /** ResourceNotFoundErrorResult */
    ResourceNotFoundErrorResult: {
      /**
       * Message
       * @description A human readable message describing the error.
       */
      message: string;
    };
    /** UnexpectedErrorResult */
    UnexpectedErrorResult: {
      /**
       * Message
       * @description A human readable message describing the error.
       */
      message: string;
    };
    /** UpdateUserInput */
    UpdateUserInput: {
      /**
       * Displayname
       * @description The new username for the user.
       */
      displayName?: string | null;
    };
    /** UserSchema */
    UserSchema: {
      /**
       * Id
       * Format: uuid
       * @description The ID of the user.
       */
      id: string;
      /**
       * Username
       * @description The username of the user.
       */
      username: string;
      /**
       * Created At
       * Format: date-time
       * @description When the user was created.
       */
      createdAt: string;
      /**
       * Updated At
       * @description When the user was last updated.
       */
      updatedAt: string | null;
      /**
       * Email
       * @description The email of the user.
       */
      email: string;
      /**
       * Haspassword
       * @description Whether the user has their password set.
       */
      hasPassword: boolean;
    };
    /** UserSessionSchema */
    UserSessionSchema: {
      /**
       * Id
       * Format: uuid
       * @description The ID of the user session.
       */
      id: string;
      /**
       * IP Address
       * Format: ipvanyaddress
       * @description The IP address of the user session.
       */
      ipAddress: string;
      /**
       * Location
       * @description The location of the user session.
       */
      location: string;
      /**
       * User Agent
       * @description The device of the user session.
       */
      device: string;
      /**
       * Logged Out At
       * @description When the user logged out of the session.
       */
      loggedOutAt: string | null;
      /**
       * Created At
       * Format: date-time
       * @description When the user session was created.
       */
      createdAt: string;
    };
    /**
     * UserVerificationRequirement
     * @description The degree to which the Relying Party wishes to verify a user's identity.
     *
     * Members:
     *     `REQUIRED`: User verification must occur
     *     `PREFERRED`: User verification would be great, but if not that's okay too
     *     `DISCOURAGED`: User verification should not occur, but it's okay if it does
     *
     * https://www.w3.org/TR/webauthn-2/#enumdef-userverificationrequirement
     * @enum {string}
     */
    UserVerificationRequirement: 'required' | 'preferred' | 'discouraged';
    /** ValidationErrorResult */
    ValidationErrorResult: {
      /**
       * Message
       * @description A human readable message describing the error.
       */
      message: string;
      /**
       * Errors
       * @description A list of validation errors.
       */
      errors: components['schemas']['ValidationErrorSchema'][];
    };
    /** ValidationErrorSchema */
    ValidationErrorSchema: {
      /**
       * Loc
       * @description The location of the validation error.
       */
      loc?: string[] | null;
      /**
       * Msg
       * @description A message describing the validation error.
       */
      msg: string;
      /**
       * Type
       * @description The type of the validation error.
       */
      type: string;
    };
  };
  responses: never;
  parameters: never;
  requestBodies: never;
  headers: never;
  pathItems: never;
}

export type $defs = Record<string, never>;

export type external = Record<string, never>;

export interface operations {
  /**
   * Check the health status of the application.
   * @description Provides information about the health status of the application.
   */
  'Tag.HEALTH-check_health': {
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          'application/json': components['schemas']['HealthCheckResult'];
        };
      };
      /** @description Validation Error */
      422: {
        content: {
          'application/json': components['schemas']['ValidationErrorResult'];
        };
      };
      /** @description Rate Limit Exceeded Error */
      429: {
        content: {
          'application/json': components['schemas']['RateLimitExceededErrorResult'];
        };
      };
      /** @description Internal Server Error */
      500: {
        content: {
          'application/json': components['schemas']['UnexpectedErrorResult'];
        };
      };
    };
  };
  /**
   * Get the current user.
   * @description Get the current user.
   */
  'ITag.USERS-get_current_user': {
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          'application/json': components['schemas']['UserSchema'];
        };
      };
      /** @description Validation Error */
      422: {
        content: {
          'application/json': components['schemas']['ValidationErrorResult'];
        };
      };
      /** @description Rate Limit Exceeded Error */
      429: {
        content: {
          'application/json': components['schemas']['RateLimitExceededErrorResult'];
        };
      };
      /** @description Internal Server Error */
      500: {
        content: {
          'application/json': components['schemas']['UnexpectedErrorResult'];
        };
      };
    };
  };
  /**
   * Update the current user.
   * @description Update the current user.
   */
  'ITag.USERS-update_current_user': {
    requestBody: {
      content: {
        'application/json': components['schemas']['UpdateUserInput'];
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          'application/json': components['schemas']['UserSchema'];
        };
      };
      /** @description Invalid Input Error */
      400: {
        content: {
          'application/json': components['schemas']['InvalidInputErrorResult'];
        };
      };
      /** @description Validation Error */
      422: {
        content: {
          'application/json': components['schemas']['ValidationErrorResult'];
        };
      };
      /** @description Rate Limit Exceeded Error */
      429: {
        content: {
          'application/json': components['schemas']['RateLimitExceededErrorResult'];
        };
      };
      /** @description Internal Server Error */
      500: {
        content: {
          'application/json': components['schemas']['UnexpectedErrorResult'];
        };
      };
    };
  };
  /**
   * Send an email change request.
   * @description Send an email change request.
   */
  'ITag.USERS-request_current_user_email_change': {
    parameters: {
      header: {
        'user-agent': string;
      };
    };
    requestBody: {
      content: {
        'application/json': components['schemas']['ChangeUserEmailRequestInput'];
      };
    };
    responses: {
      /** @description Successful Response */
      202: {
        content: {
          'application/json': unknown;
        };
      };
      /** @description Invalid Input Error */
      400: {
        content: {
          'application/json': components['schemas']['InvalidInputErrorResult'];
        };
      };
      /** @description Validation Error */
      422: {
        content: {
          'application/json': components['schemas']['ValidationErrorResult'];
        };
      };
      /** @description Rate Limit Exceeded Error */
      429: {
        content: {
          'application/json': components['schemas']['RateLimitExceededErrorResult'];
        };
      };
      /** @description Internal Server Error */
      500: {
        content: {
          'application/json': components['schemas']['UnexpectedErrorResult'];
        };
      };
    };
  };
  /**
   * Change the current user's email.
   * @description Change the current user's email.
   */
  'ITag.USERS-change_current_user_email': {
    requestBody: {
      content: {
        'application/json': components['schemas']['ChangeUserEmailInput'];
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          'application/json': components['schemas']['UserSchema'];
        };
      };
      /** @description Invalid Input Error */
      400: {
        content: {
          'application/json': components['schemas']['InvalidInputErrorResult'];
        };
      };
      /** @description Validation Error */
      422: {
        content: {
          'application/json': components['schemas']['ValidationErrorResult'];
        };
      };
      /** @description Rate Limit Exceeded Error */
      429: {
        content: {
          'application/json': components['schemas']['RateLimitExceededErrorResult'];
        };
      };
      /** @description Internal Server Error */
      500: {
        content: {
          'application/json': components['schemas']['UnexpectedErrorResult'];
        };
      };
    };
  };
  /**
   * Get the user with the given ID.
   * @description Get the user with the given ID.
   */
  'ITag.USERS-get_user': {
    parameters: {
      path: {
        user_id: string;
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          'application/json': components['schemas']['PartialUserSchema'];
        };
      };
      /** @description Resource Not Found Error */
      404: {
        content: {
          'application/json': components['schemas']['ResourceNotFoundErrorResult'];
        };
      };
      /** @description Validation Error */
      422: {
        content: {
          'application/json': components['schemas']['ValidationErrorResult'];
        };
      };
      /** @description Rate Limit Exceeded Error */
      429: {
        content: {
          'application/json': components['schemas']['RateLimitExceededErrorResult'];
        };
      };
      /** @description Internal Server Error */
      500: {
        content: {
          'application/json': components['schemas']['UnexpectedErrorResult'];
        };
      };
    };
  };
  /**
   * Start a register flow.
   * @description Start a register flow.
   */
  'ENTICATION-start_register_flow': {
    parameters: {
      header: {
        'user-agent': string;
      };
    };
    requestBody: {
      content: {
        'application/json': components['schemas']['RegisterFlowStartInput'];
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          'application/json': components['schemas']['RegisterFlowStartResult'];
        };
      };
      /** @description Invalid Input Error */
      400: {
        content: {
          'application/json': components['schemas']['InvalidInputErrorResult'];
        };
      };
      /** @description Validation Error */
      422: {
        content: {
          'application/json': components['schemas']['ValidationErrorResult'];
        };
      };
      /** @description Rate Limit Exceeded Error */
      429: {
        content: {
          'application/json': components['schemas']['RateLimitExceededErrorResult'];
        };
      };
      /** @description Internal Server Error */
      500: {
        content: {
          'application/json': components['schemas']['UnexpectedErrorResult'];
        };
      };
    };
  };
  /**
   * Verify a register flow.
   * @description Verify a register flow.
   */
  'ENTICATION-verify_register_flow': {
    requestBody: {
      content: {
        'application/json': components['schemas']['RegisterFlowVerifyInput'];
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          'application/json': components['schemas']['RegisterFlowVerifyResult'];
        };
      };
      /** @description Invalid Input Error */
      400: {
        content: {
          'application/json': components['schemas']['InvalidInputErrorResult'];
        };
      };
      /** @description Validation Error */
      422: {
        content: {
          'application/json': components['schemas']['ValidationErrorResult'];
        };
      };
      /** @description Rate Limit Exceeded Error */
      429: {
        content: {
          'application/json': components['schemas']['RateLimitExceededErrorResult'];
        };
      };
      /** @description Internal Server Error */
      500: {
        content: {
          'application/json': components['schemas']['UnexpectedErrorResult'];
        };
      };
    };
  };
  /**
   * Start the webauthn registration in the register flow.
   * @description Start the webauthn registration in the register flow.
   */
  'ENTICATION-start_webauthn_register_flow': {
    requestBody: {
      content: {
        'application/json': components['schemas']['RegisterFlowWebAuthnStartInput'];
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          'application/json': components['schemas']['PublicKeyCredentialCreationOptions'];
        };
      };
      /** @description Invalid Input Error */
      400: {
        content: {
          'application/json': components['schemas']['InvalidInputErrorResult'];
        };
      };
      /** @description Validation Error */
      422: {
        content: {
          'application/json': components['schemas']['ValidationErrorResult'];
        };
      };
      /** @description Rate Limit Exceeded Error */
      429: {
        content: {
          'application/json': components['schemas']['RateLimitExceededErrorResult'];
        };
      };
      /** @description Internal Server Error */
      500: {
        content: {
          'application/json': components['schemas']['UnexpectedErrorResult'];
        };
      };
    };
  };
  /**
   * Finish the webauthn registration in the register flow.
   * @description Finish the webauthn registration in the register flow.
   */
  'ENTICATION-finish_webauthn_register_flow': {
    requestBody: {
      content: {
        'application/json': components['schemas']['RegisterFlowWebAuthnFinishInput'];
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          'application/json': components['schemas']['RegisterFlowWebAuthnFinishResult'];
        };
      };
      /** @description Invalid Input Error */
      400: {
        content: {
          'application/json': components['schemas']['InvalidInputErrorResult'];
        };
      };
      /** @description Validation Error */
      422: {
        content: {
          'application/json': components['schemas']['ValidationErrorResult'];
        };
      };
      /** @description Rate Limit Exceeded Error */
      429: {
        content: {
          'application/json': components['schemas']['RateLimitExceededErrorResult'];
        };
      };
      /** @description Internal Server Error */
      500: {
        content: {
          'application/json': components['schemas']['UnexpectedErrorResult'];
        };
      };
    };
  };
  /**
   * Login Options
   * @description Generate options for retrieving a credential.
   */
  'ENTICATION-login_options': {
    requestBody: {
      content: {
        'application/json': components['schemas']['LoginOptionsInput'];
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          'application/json': components['schemas']['PublicKeyCredentialRequestOptions'];
        };
      };
      /** @description Validation Error */
      422: {
        content: {
          'application/json': components['schemas']['ValidationErrorResult'];
        };
      };
      /** @description Rate Limit Exceeded Error */
      429: {
        content: {
          'application/json': components['schemas']['RateLimitExceededErrorResult'];
        };
      };
      /** @description Internal Server Error */
      500: {
        content: {
          'application/json': components['schemas']['UnexpectedErrorResult'];
        };
      };
    };
  };
  /**
   * Login Verification
   * @description Verify the authenticator's response for login.
   */
  'ENTICATION-login_verification': {
    parameters: {
      header: {
        'user-agent': string;
      };
    };
    requestBody: {
      content: {
        'application/json': components['schemas']['LoginVerificationInput'];
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          'application/json': components['schemas']['AuthenticateUserResult'];
        };
      };
      /** @description Validation Error */
      422: {
        content: {
          'application/json': components['schemas']['ValidationErrorResult'];
        };
      };
      /** @description Rate Limit Exceeded Error */
      429: {
        content: {
          'application/json': components['schemas']['RateLimitExceededErrorResult'];
        };
      };
      /** @description Internal Server Error */
      500: {
        content: {
          'application/json': components['schemas']['UnexpectedErrorResult'];
        };
      };
    };
  };
  /**
   * Create Webauthn Credential
   * @description Create a new webauthn credential.
   */
  'ENTICATION-create_webauthn_credential': {
    requestBody: {
      content: {
        'application/json': components['schemas']['CreateWebAuthnCredentialInput'];
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          'application/json': unknown;
        };
      };
      /** @description Validation Error */
      422: {
        content: {
          'application/json': components['schemas']['ValidationErrorResult'];
        };
      };
      /** @description Rate Limit Exceeded Error */
      429: {
        content: {
          'application/json': components['schemas']['RateLimitExceededErrorResult'];
        };
      };
      /** @description Internal Server Error */
      500: {
        content: {
          'application/json': components['schemas']['UnexpectedErrorResult'];
        };
      };
    };
  };
  /**
   * Logout the current user.
   * @description Logout the current user.
   */
  'ENTICATION-delete_current_user_session': {
    requestBody: {
      content: {
        'application/json': components['schemas']['LogoutInput'];
      };
    };
    responses: {
      /** @description Successful Response */
      204: {
        content: never;
      };
      /** @description Validation Error */
      422: {
        content: {
          'application/json': components['schemas']['ValidationErrorResult'];
        };
      };
      /** @description Rate Limit Exceeded Error */
      429: {
        content: {
          'application/json': components['schemas']['RateLimitExceededErrorResult'];
        };
      };
      /** @description Internal Server Error */
      500: {
        content: {
          'application/json': components['schemas']['UnexpectedErrorResult'];
        };
      };
    };
  };
  /**
   * Get the current user's sessions.
   * @description Get the current user's user sessions.
   */
  'ENTICATION-get_user_sessions': {
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          'application/json': components['schemas']['UserSessionSchema'][];
        };
      };
      /** @description Validation Error */
      422: {
        content: {
          'application/json': components['schemas']['ValidationErrorResult'];
        };
      };
      /** @description Rate Limit Exceeded Error */
      429: {
        content: {
          'application/json': components['schemas']['RateLimitExceededErrorResult'];
        };
      };
      /** @description Internal Server Error */
      500: {
        content: {
          'application/json': components['schemas']['UnexpectedErrorResult'];
        };
      };
    };
  };
}
