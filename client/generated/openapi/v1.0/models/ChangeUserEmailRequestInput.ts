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
 * @interface ChangeUserEmailRequestInput
 */
export interface ChangeUserEmailRequestInput {
    /**
     * The new email address for the user.
     * @type {string}
     * @memberof ChangeUserEmailRequestInput
     */
    email: string;
    /**
     * The password associated with the user.
     * @type {string}
     * @memberof ChangeUserEmailRequestInput
     */
    currentPassword: string;
}

/**
 * Check if a given object implements the ChangeUserEmailRequestInput interface.
 */
export function instanceOfChangeUserEmailRequestInput(value: object): boolean {
    let isInstance = true;
    isInstance = isInstance && "email" in value;
    isInstance = isInstance && "currentPassword" in value;

    return isInstance;
}

export function ChangeUserEmailRequestInputFromJSON(json: any): ChangeUserEmailRequestInput {
    return ChangeUserEmailRequestInputFromJSONTyped(json, false);
}

export function ChangeUserEmailRequestInputFromJSONTyped(json: any, ignoreDiscriminator: boolean): ChangeUserEmailRequestInput {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'email': json['email'],
        'currentPassword': json['currentPassword'],
    };
}

export function ChangeUserEmailRequestInputToJSON(value?: ChangeUserEmailRequestInput | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'email': value.email,
        'currentPassword': value.currentPassword,
    };
}
