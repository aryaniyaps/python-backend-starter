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
 * @interface Id
 */
export interface Id {
}

/**
 * Check if a given object implements the Id interface.
 */
export function instanceOfId(value: object): boolean {
    let isInstance = true;

    return isInstance;
}

export function IdFromJSON(json: any): Id {
    return IdFromJSONTyped(json, false);
}

export function IdFromJSONTyped(json: any, ignoreDiscriminator: boolean): Id {
    return json;
}

export function IdToJSON(value?: Id | null): any {
    return value;
}

