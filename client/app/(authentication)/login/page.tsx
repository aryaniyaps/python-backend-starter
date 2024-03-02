'use client';
import { APP_NAME } from '@/lib/constants';
import { yupResolver } from '@hookform/resolvers/yup';
import {
  Button,
  Card,
  CardBody,
  CardFooter,
  CardHeader,
  Input,
  Link,
  Spinner,
} from '@nextui-org/react';
import { Controller, SubmitHandler, useForm } from 'react-hook-form';
import * as yup from 'yup';

const loginSchema = yup
  .object({
    email: yup
      .string()
      .required('Please enter an email')
      .email('Please enter a valid email')
      .max(255),
  })
  .required();

export default function LoginPage() {
  const { control, handleSubmit, formState } = useForm({
    resolver: yupResolver(loginSchema),
    defaultValues: { email: '' },
    mode: 'onTouched',
  });

  const onSubmit: SubmitHandler<yup.InferType<typeof loginSchema>> = (data) => {
    console.log(data);
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
            rules={{
              required: true,
              maxLength: 255,
              pattern: {
                value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                message: 'invalid email address',
              },
            }}
            render={({ field, fieldState }) => (
              <Input
                {...field}
                variant='faded'
                type='email'
                isRequired
                label='Email address'
                errorMessage={fieldState.error?.message}
                isInvalid={!!fieldState.error}
              />
            )}
          />
          <Button
            color='primary'
            type='submit'
            disabled={formState.isSubmitting}
          >
            {formState.isSubmitting ? (
              <Spinner size='sm' color='white' />
            ) : (
              <>Login with passkeys</>
            )}
          </Button>
        </form>
      </CardBody>
      <CardFooter className='text-sm'>
        Don&apos;t have an account?&nbsp;<Link href='/register'>sign up</Link>
      </CardFooter>
    </Card>
  );
}
