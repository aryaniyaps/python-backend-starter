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
 * @interface InvalidInputErrorResult
 */
export interface InvalidInputErrorResult {
    /**
     * A human readable message describing the error.
     * @type {string}
     * @memberof InvalidInputErrorResult
     */
    message: string;
}

/**
 * Check if a given object implements the InvalidInputErrorResult interface.
 */
export function instanceOfInvalidInputErrorResult(value: object): boolean {
    let isInstance = true;
    isInstance = isInstance && "message" in value;

    return isInstance;
}

export function InvalidInputErrorResultFromJSON(json: any): InvalidInputErrorResult {
    return InvalidInputErrorResultFromJSONTyped(json, false);
}

export function InvalidInputErrorResultFromJSONTyped(json: any, ignoreDiscriminator: boolean): InvalidInputErrorResult {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'message': json['message'],
    };
}

export function InvalidInputErrorResultToJSON(value?: InvalidInputErrorResult | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'message': value.message,
    };
}
