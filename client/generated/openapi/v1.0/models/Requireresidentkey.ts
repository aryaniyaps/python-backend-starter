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
 * @interface Requireresidentkey
 */
export interface Requireresidentkey {
}

/**
 * Check if a given object implements the Requireresidentkey interface.
 */
export function instanceOfRequireresidentkey(value: object): boolean {
    let isInstance = true;

    return isInstance;
}

export function RequireresidentkeyFromJSON(json: any): Requireresidentkey {
    return RequireresidentkeyFromJSONTyped(json, false);
}

export function RequireresidentkeyFromJSONTyped(json: any, ignoreDiscriminator: boolean): Requireresidentkey {
    return json;
}

export function RequireresidentkeyToJSON(value?: Requireresidentkey | null): any {
    return value;
}
