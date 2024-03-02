'use client';
import {
  Button,
  Card,
  CardBody,
  CardFooter,
  CardHeader,
} from '@nextui-org/react';
import { SubmitHandler, useForm } from 'react-hook-form';

type RegisterInput = {
  email: string;
};

export default function RegisterPage() {
  const { register, handleSubmit, formState } = useForm<RegisterInput>({});

  const onSubmit: SubmitHandler<RegisterInput> = async (data) => {};

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
