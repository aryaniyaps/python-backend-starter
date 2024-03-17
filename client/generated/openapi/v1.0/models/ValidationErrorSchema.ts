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
import type { Loc } from './Loc';
import {
    LocFromJSON,
    LocFromJSONTyped,
    LocToJSON,
} from './Loc';

/**
 * 
 * @export
 * @interface ValidationErrorSchema
 */
export interface ValidationErrorSchema {
    /**
     * 
     * @type {Loc}
     * @memberof ValidationErrorSchema
     */
    loc?: Loc;
    /**
     * A message describing the validation error.
     * @type {string}
     * @memberof ValidationErrorSchema
     */
    msg: string;
    /**
     * The type of the validation error.
     * @type {string}
     * @memberof ValidationErrorSchema
     */
    type: string;
}

/**
 * Check if a given object implements the ValidationErrorSchema interface.
 */
export function instanceOfValidationErrorSchema(value: object): boolean {
    let isInstance = true;
    isInstance = isInstance && "msg" in value;
    isInstance = isInstance && "type" in value;

    return isInstance;
}

export function ValidationErrorSchemaFromJSON(json: any): ValidationErrorSchema {
    return ValidationErrorSchemaFromJSONTyped(json, false);
}

export function ValidationErrorSchemaFromJSONTyped(json: any, ignoreDiscriminator: boolean): ValidationErrorSchema {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'loc': !exists(json, 'loc') ? undefined : LocFromJSON(json['loc']),
        'msg': json['msg'],
        'type': json['type'],
    };
}

export function ValidationErrorSchemaToJSON(value?: ValidationErrorSchema | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'loc': LocToJSON(value.loc),
        'msg': value.msg,
        'type': value.type,
    };
}
