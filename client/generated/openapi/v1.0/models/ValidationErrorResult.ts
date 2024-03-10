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
import type { ValidationErrorSchema } from './ValidationErrorSchema';
import {
    ValidationErrorSchemaFromJSON,
    ValidationErrorSchemaFromJSONTyped,
    ValidationErrorSchemaToJSON,
} from './ValidationErrorSchema';

/**
 * 
 * @export
 * @interface ValidationErrorResult
 */
export interface ValidationErrorResult {
    /**
     * A human readable message describing the error.
     * @type {string}
     * @memberof ValidationErrorResult
     */
    message: string;
    /**
     * A list of validation errors.
     * @type {Array<ValidationErrorSchema>}
     * @memberof ValidationErrorResult
     */
    errors: Array<ValidationErrorSchema>;
}

/**
 * Check if a given object implements the ValidationErrorResult interface.
 */
export function instanceOfValidationErrorResult(value: object): boolean {
    let isInstance = true;
    isInstance = isInstance && "message" in value;
    isInstance = isInstance && "errors" in value;

    return isInstance;
}

export function ValidationErrorResultFromJSON(json: any): ValidationErrorResult {
    return ValidationErrorResultFromJSONTyped(json, false);
}

export function ValidationErrorResultFromJSONTyped(json: any, ignoreDiscriminator: boolean): ValidationErrorResult {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'message': json['message'],
        'errors': ((json['errors'] as Array<any>).map(ValidationErrorSchemaFromJSON)),
    };
}

export function ValidationErrorResultToJSON(value?: ValidationErrorResult | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'message': value.message,
        'errors': ((value.errors as Array<any>).map(ValidationErrorSchemaToJSON)),
    };
}

