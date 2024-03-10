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
 * @interface HealthCheckResult
 */
export interface HealthCheckResult {
    /**
     * 
     * @type {any}
     * @memberof HealthCheckResult
     */
    status: any | null;
}

/**
 * Check if a given object implements the HealthCheckResult interface.
 */
export function instanceOfHealthCheckResult(value: object): boolean {
    let isInstance = true;
    isInstance = isInstance && "status" in value;

    return isInstance;
}

export function HealthCheckResultFromJSON(json: any): HealthCheckResult {
    return HealthCheckResultFromJSONTyped(json, false);
}

export function HealthCheckResultFromJSONTyped(json: any, ignoreDiscriminator: boolean): HealthCheckResult {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'status': json['status'],
    };
}

export function HealthCheckResultToJSON(value?: HealthCheckResult | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'status': value.status,
    };
}

