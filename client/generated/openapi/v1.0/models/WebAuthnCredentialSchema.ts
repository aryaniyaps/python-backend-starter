/* tslint:disable */
/* eslint-disable */
/**
 * Starter HTTP API
 * No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)
 *
 * The version of the OpenAPI document: 0.0.1
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */

import { exists, mapValues } from '../runtime';
/**
 * 
 * @export
 * @interface WebAuthnCredentialSchema
 */
export interface WebAuthnCredentialSchema {
    /**
     * The ID of the WebAuthn credential.
     * @type {string}
     * @memberof WebAuthnCredentialSchema
     */
    id: string;
    /**
     * The credential ID of the WebAuthn credential.
     * @type {string}
     * @memberof WebAuthnCredentialSchema
     */
    credentialId: string;
    /**
     * The public key of the WebAuthn credential.
     * @type {string}
     * @memberof WebAuthnCredentialSchema
     */
    publicKey: string;
    /**
     * The device type of the WebAuthn credential.
     * @type {string}
     * @memberof WebAuthnCredentialSchema
     */
    deviceType: string;
    /**
     * When the user session was created.
     * @type {Date}
     * @memberof WebAuthnCredentialSchema
     */
    createdAt: Date;
}

/**
 * Check if a given object implements the WebAuthnCredentialSchema interface.
 */
export function instanceOfWebAuthnCredentialSchema(value: object): boolean {
    let isInstance = true;
    isInstance = isInstance && "id" in value;
    isInstance = isInstance && "credentialId" in value;
    isInstance = isInstance && "publicKey" in value;
    isInstance = isInstance && "deviceType" in value;
    isInstance = isInstance && "createdAt" in value;

    return isInstance;
}

export function WebAuthnCredentialSchemaFromJSON(json: any): WebAuthnCredentialSchema {
    return WebAuthnCredentialSchemaFromJSONTyped(json, false);
}

export function WebAuthnCredentialSchemaFromJSONTyped(json: any, ignoreDiscriminator: boolean): WebAuthnCredentialSchema {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'id': json['id'],
        'credentialId': json['credentialId'],
        'publicKey': json['publicKey'],
        'deviceType': json['deviceType'],
        'createdAt': (new Date(json['createdAt'])),
    };
}

export function WebAuthnCredentialSchemaToJSON(value?: WebAuthnCredentialSchema | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'id': value.id,
        'credentialId': value.credentialId,
        'publicKey': value.publicKey,
        'deviceType': value.deviceType,
        'createdAt': (value.createdAt.toISOString()),
    };
}

