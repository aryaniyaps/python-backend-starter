'use client';
import { APP_NAME, MAX_EMAIL_LENGTH } from '@/lib/constants';
import { zodResolver } from '@hookform/resolvers/zod';
import { SubmitHandler, useForm } from 'react-hook-form';
import * as z from 'zod';

import useStartRegisterFlow from '@/lib/hooks/useStartRegisterFlow';
import Link from 'next/link';
import { Button } from '../ui/button';
import { Card, CardContent, CardFooter, CardHeader } from '../ui/card';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '../ui/form';
import { Input } from '../ui/input';

// TODO: change resolver to zod as we are already using it for env management
const registerSchema = z.object({
  email: z
    .string()
    .min(1, { message: 'Email address is required' })
    .email({ message: 'Email address is invalid' })
    .max(MAX_EMAIL_LENGTH, { message: 'Email address is too long' }),
});

export default function RegisterFlowStart() {
  const startRegisterFlow = useStartRegisterFlow();

  const form = useForm({
    resolver: zodResolver(registerSchema),
    defaultValues: { email: '' },
    mode: 'onTouched',
  });

  const onSubmit: SubmitHandler<z.infer<typeof registerSchema>> = async (
    input
  ) => {
    try {
      // start register flow
      await startRegisterFlow.mutateAsync({ email: input.email });
    } catch (err) {
      // TODO: handle email already taken err
      form.setError('email', {
        message: 'That email is already in use',
        type: 'server',
      });
    }
  };

  return (
    <Card className='w-full'>
      <CardHeader>
        <h1 className='text-md font-semibold'>Create a {APP_NAME} account</h1>
      </CardHeader>
      <CardContent>
        <Form {...form}>
          <form
            onSubmit={form.handleSubmit(onSubmit)}
            className='flex flex-col gap-4'
          >
            <FormField
              name='email'
              control={form.control}
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Email address</FormLabel>
                  <FormControl>
                    <Input {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <Button
              className='w-full'
              type='submit'
              disabled={form.formState.isSubmitting}
            >
              Continue
            </Button>
          </form>
        </Form>
      </CardContent>
      <CardFooter className='text-sm'>
        Have an account?&nbsp;
        <Link href='/login' className='text-primary'>
          sign in
        </Link>
      </CardFooter>
    </Card>
  );
}
