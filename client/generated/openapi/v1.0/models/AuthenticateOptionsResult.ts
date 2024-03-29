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
import type { PublicKeyCredentialRequestOptions } from './PublicKeyCredentialRequestOptions';
import {
    PublicKeyCredentialRequestOptionsFromJSON,
    PublicKeyCredentialRequestOptionsFromJSONTyped,
    PublicKeyCredentialRequestOptionsToJSON,
} from './PublicKeyCredentialRequestOptions';

/**
 * 
 * @export
 * @interface AuthenticateOptionsResult
 */
export interface AuthenticateOptionsResult {
    /**
     * 
     * @type {PublicKeyCredentialRequestOptions}
     * @memberof AuthenticateOptionsResult
     */
    options: PublicKeyCredentialRequestOptions;
}

/**
 * Check if a given object implements the AuthenticateOptionsResult interface.
 */
export function instanceOfAuthenticateOptionsResult(value: object): boolean {
    let isInstance = true;
    isInstance = isInstance && "options" in value;

    return isInstance;
}

export function AuthenticateOptionsResultFromJSON(json: any): AuthenticateOptionsResult {
    return AuthenticateOptionsResultFromJSONTyped(json, false);
}

export function AuthenticateOptionsResultFromJSONTyped(json: any, ignoreDiscriminator: boolean): AuthenticateOptionsResult {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'options': PublicKeyCredentialRequestOptionsFromJSON(json['options']),
    };
}

export function AuthenticateOptionsResultToJSON(value?: AuthenticateOptionsResult | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'options': PublicKeyCredentialRequestOptionsToJSON(value.options),
    };
}

