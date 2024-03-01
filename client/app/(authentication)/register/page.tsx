'use client';
import { APP_NAME } from '@/lib/constants';
import {
  Button,
  Card,
  CardBody,
  CardFooter,
  CardHeader,
  Input,
  Link,
} from '@nextui-org/react';
import { startRegistration } from '@simplewebauthn/browser';
import { SubmitHandler, useForm } from 'react-hook-form';

type RegisterInput = {
  email: string;
};

export default function RegisterPage() {
  const { register, handleSubmit } = useForm<RegisterInput>({});

  const onSubmit: SubmitHandler<RegisterInput> = async (data) => {
    const resp = await fetch('/api/v1/auth/register/start', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email: data.email }),
    });

    // TODO: catch and display errors here
    const attResp = await startRegistration(await resp.json());

    const verificationResp = await fetch('/api/v1/auth/register/finish', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(attResp),
    });

    const verificationJSON = await verificationResp.json();

    if (verificationJSON && verificationJSON.verified) {
      console.log('user is verified!');
    } else {
      console.log('user is not verified!');
    }
  };

  return (
    <Card isFooterBlurred fullWidth className='px-unit-2'>
      <CardHeader>
        <h1 className='text-md font-semibold'>Create a {APP_NAME} account</h1>
      </CardHeader>
      <CardBody>
        <form onSubmit={handleSubmit(onSubmit)} className='flex flex-col gap-4'>
          <Input
            {...register('email')}
            type='email'
            isRequired
            label='Email address'
            description="You'll need to verify that you own this email."
          />
          <Button color='primary' type='submit'>
            Continue
          </Button>
        </form>
      </CardBody>
      <CardFooter className='text-sm'>
        Have an account?&nbsp;<Link href='/login'>sign in</Link>
      </CardFooter>
    </Card>
  );
}
