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
 * The location of the validation error.
 * @export
 * @interface Loc
 */
export interface Loc {
}

/**
 * Check if a given object implements the Loc interface.
 */
export function instanceOfLoc(value: object): boolean {
    let isInstance = true;

    return isInstance;
}

export function LocFromJSON(json: any): Loc {
    return LocFromJSONTyped(json, false);
}

export function LocFromJSONTyped(json: any, ignoreDiscriminator: boolean): Loc {
    return json;
}

export function LocToJSON(value?: Loc | null): any {
    return value;
}
