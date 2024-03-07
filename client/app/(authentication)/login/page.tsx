'use client';
import { client } from '@/lib/client';
import {
  APP_NAME,
  DEFAULT_REDIRECT_TO,
  MAX_EMAIL_LENGTH,
} from '@/lib/constants';
import { zodResolver } from '@hookform/resolvers/zod';
import {
  Button,
  Card,
  CardBody,
  CardFooter,
  CardHeader,
  Input,
  Link,
} from '@nextui-org/react';
import { startAuthentication } from '@simplewebauthn/browser';
import { useRouter, useSearchParams } from 'next/navigation';
import { Controller, SubmitHandler, useForm } from 'react-hook-form';
import * as z from 'zod';

const loginSchema = z.object({
  email: z
    .string()
    .min(1, { message: 'Email address is required' })
    .email({ message: 'Email address is invalid' })
    .max(MAX_EMAIL_LENGTH, { message: 'Email address is too long' }),
});

export default function LoginPage() {
  const { control, handleSubmit, formState, setError } = useForm({
    resolver: zodResolver(loginSchema),
    defaultValues: { email: '' },
    mode: 'onTouched',
  });

  const searchParams = useSearchParams();

  const returnTo = searchParams.get('returnTo') || DEFAULT_REDIRECT_TO;

  const router = useRouter();

  const onSubmit: SubmitHandler<z.infer<typeof loginSchema>> = async (
    input
  ) => {
    console.log(input);

    let asseResp;
    try {
      // start webauthn authentication
      const { data } = await client.POST('/auth/authenticate/start', {
        body: { email: input.email },
      });

      // Pass the options to the authenticator and wait for a response
      asseResp = await startAuthentication(data.options);
    } catch (err) {
      // TODO: handle errors better
      return setError('email', {
        message:
          "User with that email doesn't exist or couldn't login with passkey.",
        type: 'server',
      });
    }

    await client.POST('/auth/authenticate/finish', {
      params: { header: { 'user-agent': navigator.userAgent } },
      body: {
        credential: JSON.stringify(asseResp),
      },
    });

    router.replace(returnTo);
  };

  return (
    <Card isFooterBlurred fullWidth className='px-unit-2'>
      <CardHeader>
        <h1 className='text-md font-semibold'>Sign in with {APP_NAME}</h1>
      </CardHeader>
      <CardBody>
        <form onSubmit={handleSubmit(onSubmit)} className='flex flex-col gap-4'>
          <Controller
            name='email'
            control={control}
            render={({ field, fieldState }) => (
              <Input
                {...field}
                variant='faded'
                type='email'
                label='Email address'
                errorMessage={fieldState.error?.message}
                isInvalid={!!fieldState.error}
              />
            )}
          />
          <Button
            color='primary'
            type='submit'
            isLoading={formState.isSubmitting}
          >
            Login with passkeys
          </Button>
        </form>
      </CardBody>
      <CardFooter className='text-sm'>
        Don&apos;t have an account?&nbsp;<Link href='/register'>sign up</Link>
      </CardFooter>
    </Card>
  );
}
