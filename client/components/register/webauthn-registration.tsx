'use client';
import { useLocalRegisterFlow } from '@/components/register/flow-provider';
import { DEFAULT_REDIRECT_TO } from '@/lib/constants';
import useCancelRegisterFlow from '@/lib/hooks/useCancelRegisterFlow';
import useWebAuthnFinishRegisterFlow from '@/lib/hooks/useWebAuthnFinishRegisterFlow';
import useWebAuthnStartRegisterFlow from '@/lib/hooks/useWebAuthnStartRegisterFlow';
import { startRegistration } from '@simplewebauthn/browser';
import Link from 'next/link';
import { useRouter, useSearchParams } from 'next/navigation';
import { SubmitHandler, useForm } from 'react-hook-form';
import { Icons } from '../icons';
import { Alert, AlertDescription } from '../ui/alert';
import { Button } from '../ui/button';
import { Card, CardContent, CardFooter, CardHeader } from '../ui/card';
import { Form } from '../ui/form';

export default function RegisterWebAuthnRegistration() {
  const startWebAuthnRegisterFlow = useWebAuthnStartRegisterFlow();
  const finishWebAuthnRegisterFlow = useWebAuthnFinishRegisterFlow();
  const cancelRegisterFlow = useCancelRegisterFlow();

  const form = useForm({});

  const router = useRouter();
  const searchParams = useSearchParams();

  const { flow } = useLocalRegisterFlow();

  const returnTo = searchParams.get('returnTo') || DEFAULT_REDIRECT_TO;

  const onSubmit: SubmitHandler<{}> = async () => {
    // start webauthn registration
    const data = await startWebAuthnRegisterFlow.mutateAsync({
      flowId: flow!.id,
    });

    if (data) {
      let authenticatorResponse;
      try {
        authenticatorResponse = await startRegistration(data.options);
      } catch (err) {
        return form.setError('root', {
          message: `Couldn't create passkey. Please try again`,
        });
      }

      try {
        await finishWebAuthnRegisterFlow.mutateAsync({
          flowId: flow!.id,
          credential: JSON.stringify(authenticatorResponse),
        });
      } catch (err) {
        // TODO: perform better error handling
        return form.setError('root', {
          message: `Couldn't verify user. Please try again`,
        });
      }

      router.replace(returnTo);
    }
  };

  return (
    <Card className='w-full'>
      <CardHeader>
        <div className='flex flex-col items-start gap-2'>
          <h1 className='text-md font-semibold'>Create a passkey</h1>
          <h3 className='text-xs font-light'>
            Passkeys are a secure alternative to passwords.{' '}
            <Link
              href='https://developers.google.com/identity/passkeys'
              rel='noopener noreferrer'
              target='_blank'
            >
              learn more
            </Link>
          </h3>
        </div>
      </CardHeader>
      <CardContent className='flex flex-col gap-6'>
        {form.formState.errors.root ? (
          <Alert variant='destructive'>
            <AlertDescription>
              {form.formState.errors.root.message}
            </AlertDescription>
          </Alert>
        ) : null}
        <Form {...form}>
          <form
            onSubmit={form.handleSubmit(onSubmit)}
            className='flex flex-col gap-4'
          >
            <Button
              type='submit'
              disabled={form.formState.isSubmitting}
              className='flex w-full gap-2'
            >
              <Icons.key className='h-5 w-5' />
              Create passkey
            </Button>
          </form>
        </Form>
      </CardContent>
      <CardFooter>
        <Button
          variant='outline'
          className='w-full'
          onClick={async () => {
            await cancelRegisterFlow.mutateAsync({ flowId: flow!.id });
            router.refresh();
          }}
        >
          Cancel
        </Button>
      </CardFooter>
    </Card>
  );
}
