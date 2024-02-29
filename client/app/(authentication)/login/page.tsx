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
import { SubmitHandler, useForm } from 'react-hook-form';

type LoginInput = {
  email: string;
};

export default function LoginPage() {
  const { register, handleSubmit } = useForm<LoginInput>({});

  const onSubmit: SubmitHandler<LoginInput> = (data) => console.log(data);
  return (
    <Card isFooterBlurred fullWidth className='px-unit-2'>
      <CardHeader>
        <h1 className='text-md font-semibold'>Sign in with {APP_NAME}</h1>
      </CardHeader>
      <CardBody>
        <form onSubmit={handleSubmit(onSubmit)} className='flex flex-col gap-4'>
          <Input type='email' label='Email address' {...register('email')} />
          <Button color='primary' type='submit'>
            login with passkeys
          </Button>
        </form>
      </CardBody>
      <CardFooter className='text-sm'>
        Don&apos;t have an account?&nbsp;<Link href='/register'>sign up</Link>
      </CardFooter>
    </Card>
  );
}
