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
 * @interface PublicKeyCredentialUserEntity
 */
export interface PublicKeyCredentialUserEntity {
    /**
     * 
     * @type {Blob}
     * @memberof PublicKeyCredentialUserEntity
     */
    id: Blob;
    /**
     * 
     * @type {string}
     * @memberof PublicKeyCredentialUserEntity
     */
    name: string;
    /**
     * 
     * @type {string}
     * @memberof PublicKeyCredentialUserEntity
     */
    displayName: string;
}

/**
 * Check if a given object implements the PublicKeyCredentialUserEntity interface.
 */
export function instanceOfPublicKeyCredentialUserEntity(value: object): boolean {
    let isInstance = true;
    isInstance = isInstance && "id" in value;
    isInstance = isInstance && "name" in value;
    isInstance = isInstance && "displayName" in value;

    return isInstance;
}

export function PublicKeyCredentialUserEntityFromJSON(json: any): PublicKeyCredentialUserEntity {
    return PublicKeyCredentialUserEntityFromJSONTyped(json, false);
}

export function PublicKeyCredentialUserEntityFromJSONTyped(json: any, ignoreDiscriminator: boolean): PublicKeyCredentialUserEntity {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'id': json['id'],
        'name': json['name'],
        'displayName': json['displayName'],
    };
}

export function PublicKeyCredentialUserEntityToJSON(value?: PublicKeyCredentialUserEntity | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'id': value.id,
        'name': value.name,
        'displayName': value.displayName,
    };
}

