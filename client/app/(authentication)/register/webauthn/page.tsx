'use client';
import { useRegisterFlow } from '@/components/register-flow-provider';
import { client } from '@/lib/client';
import { yupResolver } from '@hookform/resolvers/yup';
import {
  Button,
  Card,
  CardBody,
  CardFooter,
  CardHeader,
  Input,
} from '@nextui-org/react';
import { startRegistration } from '@simplewebauthn/browser';
import { useRouter } from 'next/navigation';
import { Controller, SubmitHandler, useForm } from 'react-hook-form';
import * as yup from 'yup';

const createPasskeySchema = yup
  .object({
    displayName: yup.string().required().max(75),
  })
  .required();

export default function RegisterPage() {
  const { handleSubmit, formState, control } = useForm({
    resolver: yupResolver(createPasskeySchema),
  });
  const router = useRouter();
  const { flowId } = useRegisterFlow();
  if (!flowId) {
    // redirect to register page
    return router.push('/register');
  }

  const onSubmit: SubmitHandler<
    yup.InferType<typeof createPasskeySchema>
  > = async (input) => {
    console.log(input);

    // start webauthn registration
    const { data } = await client.POST('/auth/register/flow/webauthn-start', {
      body: { flowId: flowId, displayName: input.displayName },
    });

    if (data) {
      let attResp;
      try {
        attResp = await startRegistration(data.options);
      } catch (err) {
        alert("Couldn't register credential!");
        return;
      }

      const { data: verificationData } = await client.POST(
        '/auth/register/flow/webauthn-finish',
        { body: attResp }
      );

      if (verificationData) {
        const authToken = verificationData.authenticationToken;
        // TODO: store authentication token
      }
    }
  };

  return (
    <Card isFooterBlurred fullWidth className='px-unit-2'>
      <CardHeader>
        <h1 className='text-md font-semibold'>Create a passkey</h1>
      </CardHeader>
      <CardBody>
        <form onSubmit={handleSubmit(onSubmit)} className='flex flex-col gap-4'>
          <Controller
            name='displayName'
            control={control}
            render={({ field, fieldState }) => {
              return (
                <Input
                  {...field}
                  variant='faded'
                  type='text'
                  label='Display name'
                  placeholder='example passkey'
                  description='Enter the name of your passkey'
                  errorMessage={fieldState.error?.message}
                  isInvalid={!!fieldState.error}
                />
              );
            }}
          />
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
