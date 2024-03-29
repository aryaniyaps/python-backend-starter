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
import type { PageInfoUUID } from './PageInfoUUID';
import {
    PageInfoUUIDFromJSON,
    PageInfoUUIDFromJSONTyped,
    PageInfoUUIDToJSON,
} from './PageInfoUUID';
import type { UserSessionSchema } from './UserSessionSchema';
import {
    UserSessionSchemaFromJSON,
    UserSessionSchemaFromJSONTyped,
    UserSessionSchemaToJSON,
} from './UserSessionSchema';

/**
 * 
 * @export
 * @interface PaginatedResultUserSessionSchemaUUID
 */
export interface PaginatedResultUserSessionSchemaUUID {
    /**
     * A list of entities.
     * @type {Array<UserSessionSchema>}
     * @memberof PaginatedResultUserSessionSchemaUUID
     */
    entities: Array<UserSessionSchema>;
    /**
     * 
     * @type {PageInfoUUID}
     * @memberof PaginatedResultUserSessionSchemaUUID
     */
    pageInfo: PageInfoUUID;
}

/**
 * Check if a given object implements the PaginatedResultUserSessionSchemaUUID interface.
 */
export function instanceOfPaginatedResultUserSessionSchemaUUID(value: object): boolean {
    let isInstance = true;
    isInstance = isInstance && "entities" in value;
    isInstance = isInstance && "pageInfo" in value;

    return isInstance;
}

export function PaginatedResultUserSessionSchemaUUIDFromJSON(json: any): PaginatedResultUserSessionSchemaUUID {
    return PaginatedResultUserSessionSchemaUUIDFromJSONTyped(json, false);
}

export function PaginatedResultUserSessionSchemaUUIDFromJSONTyped(json: any, ignoreDiscriminator: boolean): PaginatedResultUserSessionSchemaUUID {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'entities': ((json['entities'] as Array<any>).map(UserSessionSchemaFromJSON)),
        'pageInfo': PageInfoUUIDFromJSON(json['pageInfo']),
    };
}

export function PaginatedResultUserSessionSchemaUUIDToJSON(value?: PaginatedResultUserSessionSchemaUUID | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'entities': ((value.entities as Array<any>).map(UserSessionSchemaToJSON)),
        'pageInfo': PageInfoUUIDToJSON(value.pageInfo),
    };
}

