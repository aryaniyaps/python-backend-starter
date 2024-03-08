TODO: REPLACE openapi-fetch with some other client library, as the data being undefined causes an undesirable DX with TS

TODO:

generate a flow ID during registration and save it server side.
this flow ID is taken by the client and stored client side in local storage.

during each step, the client retrieves flow info/ state (whether it is valid, what stage it is in)
if the flow ID is invalid, the client redirects to initial register form and deletes it from local storage

if it is valid, it redirects to the relevant flow stage

flow stages:

- step 1: user enters email and a verification code is sent. if email already exists, error is returned. otherwise, the flow ID is returned from the server
- step 2: the verification code is entered by the client along with the flow ID. If the code is correct, the server marks the flow as verified server-side and proceeds to the next stage.
- step 3: the user initiates the webauthn registration process with the email as username
- step 4: the user finishes the webauthn registration process and the user is created along with their webauthn credential

the flowID is best stored in clientStorage, instead of the query param.

but if it is stored in query param, maybe we can validate the flow ID server-side using next js itself, before rendering the page
and redirect to the required state.
