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


/**
 * The Relying Party's preference for the authenticator to create a dedicated "client-side" credential for it. Requiring an authenticator to store a dedicated credential should not be done lightly due to the limited storage capacity of some types of authenticators.
 * 
 * Members:
 *     `DISCOURAGED`: The authenticator should not create a dedicated credential
 *     `PREFERRED`: The authenticator can create and store a dedicated credential, but if it doesn't that's alright too
 *     `REQUIRED`: The authenticator MUST create a dedicated credential. If it cannot, the RP is prepared for an error to occur.
 * 
 * https://www.w3.org/TR/webauthn-2/#enum-residentKeyRequirement
 * @export
 */
export const ResidentKeyRequirement = {
    Discouraged: 'discouraged',
    Preferred: 'preferred',
    Required: 'required'
} as const;
export type ResidentKeyRequirement = typeof ResidentKeyRequirement[keyof typeof ResidentKeyRequirement];


export function ResidentKeyRequirementFromJSON(json: any): ResidentKeyRequirement {
    return ResidentKeyRequirementFromJSONTyped(json, false);
}

export function ResidentKeyRequirementFromJSONTyped(json: any, ignoreDiscriminator: boolean): ResidentKeyRequirement {
    return json as ResidentKeyRequirement;
}

export function ResidentKeyRequirementToJSON(value?: ResidentKeyRequirement | null): any {
    return value as any;
}

