'use client';
import { useRegisterFlow } from '@/components/register-flow-provider';
import { client } from '@/lib/client';
import { KeyIcon } from '@heroicons/react/24/outline';
import {
  Button,
  Card,
  CardBody,
  CardFooter,
  CardHeader,
  Link,
} from '@nextui-org/react';
import { startRegistration } from '@simplewebauthn/browser';
import { useRouter } from 'next/navigation';
import { SubmitHandler, useForm } from 'react-hook-form';

export default function RegisterWebAuthnPage() {
  const { handleSubmit, formState, setError } = useForm({});

  const router = useRouter();
  const { flowId, setFlowId, setCurrentStep, setEmail } = useRegisterFlow();
  if (!flowId) {
    // redirect to register page
    return router.push('/register');
  }

  const onSubmit: SubmitHandler<{}> = async () => {
    // start webauthn registration
    const { data } = await client.POST('/auth/register/flow/webauthn-start', {
      body: { flowId: flowId },
    });

    if (data) {
      let attResp;
      try {
        attResp = await startRegistration(data.options);
        console.log('ATTESTATION RESPONSE: ', attResp);
      } catch (err) {
        setError('root', {
          message: `Couldn't create passkey. Please try again`,
        });
        return;
      }

      // FIXME ugly hack: we are renaming the `clientDataJSON` key to `clientDataJson`
      const { data: verificationData } = await client.POST(
        '/auth/register/flow/webauthn-finish',
        {
          body: {
            flowId: flowId,
            credential: JSON.stringify({
              ...attResp,
              response: {
                ...attResp.response,
                clientDataJson: attResp.response.clientDataJSON,
              },
            }),
          },
        }
      );

      if (verificationData) {
        const authToken = verificationData.authenticationToken;
        // TODO: store authentication token
        console.log('AUTHENTICATED!! auth token:', authToken);
      }
    }
  };

  return (
    <Card isFooterBlurred fullWidth className='px-unit-2'>
      <CardHeader className='flex flex-col items-start gap-unit-2'>
        <h1 className='text-md font-semibold'>Create a passkey</h1>
        <h3 className='text-xs font-light'>
          Passkeys are a secure alternative to passwords.{' '}
          <Link
            size='sm'
            href='https://developers.google.com/identity/passkeys'
            isExternal
            showAnchorIcon
          >
            learn more
          </Link>
        </h3>
      </CardHeader>
      <CardBody className='flex flex-col gap-unit-6'>
        {/* TODO: use a nested card for errors until we get an alert component */}
        {formState.errors.root ? (
          <Card isFooterBlurred fullWidth className='bg-danger-50 px-unit-2'>
            <CardBody className='text-center text-danger'>
              {formState.errors.root.message}
            </CardBody>
          </Card>
        ) : null}
        <form
          onSubmit={handleSubmit(onSubmit)}
          className='flex flex-col gap-unit-4'
        >
          <Button color='primary' type='submit'>
            <KeyIcon className='h-unit-6 w-unit-6' /> Create passkey
          </Button>
        </form>
      </CardBody>
      <CardFooter>
        <Button
          variant='ghost'
          fullWidth
          onClick={async () => {
            await client.POST('/auth/register/flow/cancel', {
              body: { flowId: flowId },
            });
            setFlowId(null);
            setCurrentStep(null);
            setEmail(null);
          }}
        >
          Cancel
        </Button>
      </CardFooter>
    </Card>
  );
}
