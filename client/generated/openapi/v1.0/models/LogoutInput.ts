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
 * @interface LogoutInput
 */
export interface LogoutInput {
    /**
     * Whether the current user's session should be remembered.
     * @type {boolean}
     * @memberof LogoutInput
     */
    rememberSession?: boolean;
}

/**
 * Check if a given object implements the LogoutInput interface.
 */
export function instanceOfLogoutInput(value: object): boolean {
    let isInstance = true;

    return isInstance;
}

export function LogoutInputFromJSON(json: any): LogoutInput {
    return LogoutInputFromJSONTyped(json, false);
}

export function LogoutInputFromJSONTyped(json: any, ignoreDiscriminator: boolean): LogoutInput {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'rememberSession': !exists(json, 'rememberSession') ? undefined : json['rememberSession'],
    };
}

export function LogoutInputToJSON(value?: LogoutInput | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'rememberSession': value.rememberSession,
    };
}

