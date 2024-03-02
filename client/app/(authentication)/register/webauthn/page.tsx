'use client';
import { client } from '@/lib/client';
import {
  Button,
  Card,
  CardBody,
  CardFooter,
  CardHeader,
} from '@nextui-org/react';
import { SubmitHandler, useForm } from 'react-hook-form';

// TODO: remove form and only keep button?
type RegisterWebAuthnInput = {
  email: string;
};

export default function RegisterPage() {
  const { handleSubmit, formState } = useForm<RegisterWebAuthnInput>({});

  const onSubmit: SubmitHandler<RegisterWebAuthnInput> = async (data) => {
    console.log(data);

    // start webauthn registration
    await client.POST('/auth/register/flow/webauthn-start', {
      body: { flowId: '', displayName: '' },
    });
  };

  return (
    <Card isFooterBlurred fullWidth className='px-unit-2'>
      <CardHeader>
        <h1 className='text-md font-semibold'>Create a passkey</h1>
      </CardHeader>
      <CardBody>
        <form onSubmit={handleSubmit(onSubmit)} className='flex flex-col gap-4'>
          <Button color='primary' type='submit' isDisabled={!formState.isValid}>
            Create passkey
          </Button>
        </form>
      </CardBody>
      <CardFooter>
        <Button variant='ghost' fullWidth>
          Go back
        </Button>
      </CardFooter>
    </Card>
  );
}
