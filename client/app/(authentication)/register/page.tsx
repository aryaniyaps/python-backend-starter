'use client';
import { APP_NAME, MAX_EMAIL_LENGTH } from '@/lib/constants';
import { yupResolver } from '@hookform/resolvers/yup';
import {
  Button,
  Card,
  CardBody,
  CardFooter,
  CardHeader,
  Input,
  Link,
} from '@nextui-org/react';
import { Controller, SubmitHandler, useForm } from 'react-hook-form';
import * as yup from 'yup';

import { useRegisterFlow } from '@/components/register-flow-provider';
import { client } from '@/lib/client';

// TODO: change resolver to zod as we are already using it for env management
const registerSchema = yup
  .object({
    email: yup
      .string()
      .required('Please enter an email')
      .email('Please enter a valid email')
      .max(MAX_EMAIL_LENGTH),
  })
  .required();

export default function RegisterPage() {
  const { setCurrentStep, setFlowId } = useRegisterFlow();

  const { handleSubmit, control, formState, setError } = useForm({
    resolver: yupResolver(registerSchema),
    defaultValues: { email: '' },
    mode: 'onTouched',
  });

  const onSubmit: SubmitHandler<yup.InferType<typeof registerSchema>> = async (
    input
  ) => {
    console.log(input);
    try {
      // start register flow
      const { data } = await client.POST('/auth/register/flow/start', {
        body: { email: input.email },
        params: {
          header: { 'user-agent': window.navigator.userAgent },
        },
      });

      if (data) {
        setFlowId(data.registerFlow.id);
        setCurrentStep(data.registerFlow.currentStep);
      }
    } catch (err) {
      // TODO: handle email already taken err
      setError('email', {
        message: 'That email is already in use',
        type: 'server',
      });
    }
  };

  return (
    <Card isFooterBlurred fullWidth className='px-unit-2'>
      <CardHeader>
        <h1 className='text-md font-semibold'>Create a {APP_NAME} account</h1>
      </CardHeader>
      <CardBody>
        <form onSubmit={handleSubmit(onSubmit)} className='flex flex-col gap-4'>
          <Controller
            name='email'
            control={control}
            render={({ field, fieldState }) => {
              return (
                <Input
                  {...field}
                  variant='faded'
                  type='email'
                  label='Email address'
                  errorMessage={fieldState.error?.message}
                  isInvalid={!!fieldState.error}
                />
              );
            }}
          />

          <Button
            color='primary'
            type='submit'
            isLoading={formState.isSubmitting}
          >
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
