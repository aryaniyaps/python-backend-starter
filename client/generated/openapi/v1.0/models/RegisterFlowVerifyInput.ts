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
 * @interface RegisterFlowVerifyInput
 */
export interface RegisterFlowVerifyInput {
    /**
     * 
     * @type {string}
     * @memberof RegisterFlowVerifyInput
     */
    verificationCode: string;
}

/**
 * Check if a given object implements the RegisterFlowVerifyInput interface.
 */
export function instanceOfRegisterFlowVerifyInput(value: object): boolean {
    let isInstance = true;
    isInstance = isInstance && "verificationCode" in value;

    return isInstance;
}

export function RegisterFlowVerifyInputFromJSON(json: any): RegisterFlowVerifyInput {
    return RegisterFlowVerifyInputFromJSONTyped(json, false);
}

export function RegisterFlowVerifyInputFromJSONTyped(json: any, ignoreDiscriminator: boolean): RegisterFlowVerifyInput {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'verificationCode': json['verificationCode'],
    };
}

export function RegisterFlowVerifyInputToJSON(value?: RegisterFlowVerifyInput | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'verificationCode': value.verificationCode,
    };
}

