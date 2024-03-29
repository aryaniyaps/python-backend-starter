'use client';
import { Icons } from '@/components/icons';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Button } from '@/components/ui/button';
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
} from '@/components/ui/card';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import {
  APP_NAME,
  DEFAULT_REDIRECT_TO,
  MAX_EMAIL_LENGTH,
} from '@/lib/constants';
import useAuthenticateFinish from '@/lib/hooks/useAuthenticateFinish';
import useAuthenticateStart from '@/lib/hooks/useAuthenticateStart';
import { zodResolver } from '@hookform/resolvers/zod';
import { startAuthentication } from '@simplewebauthn/browser';
import Link from 'next/link';
import { useRouter, useSearchParams } from 'next/navigation';
import { SubmitHandler, useForm } from 'react-hook-form';
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

  const form = useForm({
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
      return form.setError('email', {
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
        return form.setError('root', {
          message: "Couldn't login with passkey. Please try again",
          type: 'server',
        });
      }

      router.replace(returnTo);
    }
  };

  return (
    <Card className='w-full'>
      <CardHeader>
        <h1 className='text-md font-semibold'>Sign in with {APP_NAME}</h1>
      </CardHeader>
      <CardContent>
        <Form {...form}>
          <form
            onSubmit={form.handleSubmit(onSubmit)}
            className='flex flex-col gap-4'
          >
            {form.formState.errors.root ? (
              <Alert variant='destructive'>
                <AlertDescription>
                  {form.formState.errors.root.message}
                </AlertDescription>
              </Alert>
            ) : null}
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
              type='submit'
              className='flex w-full gap-2'
              disabled={form.formState.isSubmitting}
            >
              <Icons.key className='h-5 w-5' />
              Login with passkeys
            </Button>
          </form>
        </Form>
      </CardContent>
      <CardFooter className='text-sm'>
        Don&apos;t have an account?&nbsp;
        <Link href='/register' className='text-primary'>
          sign up
        </Link>
      </CardFooter>
    </Card>
  );
}
