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
import type { Displayname } from './Displayname';
import {
    DisplaynameFromJSON,
    DisplaynameFromJSONTyped,
    DisplaynameToJSON,
} from './Displayname';

/**
 * 
 * @export
 * @interface UpdateUserInput
 */
export interface UpdateUserInput {
    /**
     * 
     * @type {Displayname}
     * @memberof UpdateUserInput
     */
    displayName?: Displayname;
}

/**
 * Check if a given object implements the UpdateUserInput interface.
 */
export function instanceOfUpdateUserInput(value: object): boolean {
    let isInstance = true;

    return isInstance;
}

export function UpdateUserInputFromJSON(json: any): UpdateUserInput {
    return UpdateUserInputFromJSONTyped(json, false);
}

export function UpdateUserInputFromJSONTyped(json: any, ignoreDiscriminator: boolean): UpdateUserInput {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'displayName': !exists(json, 'displayName') ? undefined : DisplaynameFromJSON(json['displayName']),
    };
}

export function UpdateUserInputToJSON(value?: UpdateUserInput | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'displayName': DisplaynameToJSON(value.displayName),
    };
}
