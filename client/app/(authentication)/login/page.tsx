'use client';
import {
  APP_NAME,
  DEFAULT_REDIRECT_TO,
  MAX_EMAIL_LENGTH,
} from '@/lib/constants';
import useAuthenticateFinish from '@/lib/hooks/useAuthenticateFinish';
import useAuthenticateStart from '@/lib/hooks/useAuthenticateStart';
import { KeyIcon } from '@heroicons/react/24/outline';
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
  const authenticateFinish = useAuthenticateFinish();
  const authenticateStart = useAuthenticateStart();

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
    let data;

    try {
      // start webauthn authentication
      data = await authenticateStart.mutateAsync({ email: input.email });
    } catch (err) {
      // TODO: handle errors better
      return setError('email', {
        message: "User with that email doesn't exist",
        type: 'server',
      });
    }

    if (data) {
      try {
        // Pass the options to the authenticator and wait for a response
        const authenticatorResponse = await startAuthentication(data.options);
        await authenticateFinish.mutateAsync({
          credential: JSON.stringify(authenticatorResponse),
        });
      } catch (err) {
        // TODO: handle errors better
        return setError('root', {
          message: "Couldn't login with passkey. Please try again",
          type: 'server',
        });
      }

      router.replace(returnTo);
    }
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
          {/* TODO: use a nested card for errors until we get an alert component */}
          {formState.errors.root ? (
            <Card isFooterBlurred fullWidth className='bg-danger-50 px-unit-2'>
              <CardBody className='text-center text-sm text-danger'>
                {formState.errors.root.message}
              </CardBody>
            </Card>
          ) : null}
          <Button
            color='primary'
            type='submit'
            isLoading={formState.isSubmitting}
          >
            {!formState.isSubmitting ? (
              <KeyIcon className='h-unit-6 w-unit-6' />
            ) : null}{' '}
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
