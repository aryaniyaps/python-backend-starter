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

type RegisterInput = {
  email: string;
  displayName: string;
};

export default function RegisterPage() {
  const { register, handleSubmit } = useForm<RegisterInput>({});

  const onSubmit: SubmitHandler<RegisterInput> = (data) => console.log(data);

  return (
    <Card isFooterBlurred fullWidth className='px-unit-2'>
      <CardHeader>
        <h1 className='text-md font-semibold'>Create a {APP_NAME} account</h1>
      </CardHeader>
      <CardBody>
        <form onSubmit={handleSubmit(onSubmit)} className='flex flex-col gap-4'>
          <Input type='email' label='Email address' {...register('email')} />
          <Input
            type='text'
            label='Display name'
            {...register('displayName')}
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
