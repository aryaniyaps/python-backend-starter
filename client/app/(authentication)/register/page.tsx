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
} from '@nextui-org/react';
import { Controller, SubmitHandler, useForm } from 'react-hook-form';
import * as yup from 'yup';

const registerSchema = yup
  .object({
    email: yup
      .string()
      .required('Please enter an email')
      .email('Please enter a valid email')
      .max(255),
  })
  .required();

export default function RegisterPage() {
  const { handleSubmit, control, formState } = useForm({
    resolver: yupResolver(registerSchema),
    defaultValues: { email: '' },
    mode: 'onTouched',
  });

  const onSubmit: SubmitHandler<yup.InferType<typeof registerSchema>> = async (
    data
  ) => {
    console.log(data);
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
