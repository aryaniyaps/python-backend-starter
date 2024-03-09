'use client';
import { useLocalRegisterFlow } from '@/components/register/flow-provider';
import {
  InputOTP,
  InputOTPGroup,
  InputOTPSeparator,
  InputOTPSlot,
} from '@/components/ui/input-otp';
import { EMAIL_VERIFICATION_CODE_LENGTH } from '@/lib/constants';
import useCancelRegisterFlow from '@/lib/hooks/useCancelRegisterFlow';
import useResendVerificationRegisterFlow from '@/lib/hooks/useResendVerificationRegisterFlow';
import useVerifyRegisterFlow from '@/lib/hooks/useVerifyRegisterFlow';
import { zodResolver } from '@hookform/resolvers/zod';
import { useRouter } from 'next/navigation';
import { SubmitHandler, useForm } from 'react-hook-form';
import * as z from 'zod';
import { Button } from '../ui/button';
import { Card, CardContent, CardFooter, CardHeader } from '../ui/card';
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '../ui/form';

const verifyRegisterFlowSchema = z.object({
  verificationCode: z.string().length(EMAIL_VERIFICATION_CODE_LENGTH),
});

export default function RegisterEmailVerification() {
  const verifyRegisterFlow = useVerifyRegisterFlow();
  const resendVerificationRegisterFlow = useResendVerificationRegisterFlow();
  const cancelRegisterFlow = useCancelRegisterFlow();
  const { flow } = useLocalRegisterFlow();

  const router = useRouter();

  const form = useForm({
    resolver: zodResolver(verifyRegisterFlowSchema),
    defaultValues: { verificationCode: '' },
    reValidateMode: 'onSubmit',
  });

  const onSubmit: SubmitHandler<
    z.infer<typeof verifyRegisterFlowSchema>
  > = async (input) => {
    try {
      // verify register flow
      await verifyRegisterFlow.mutateAsync({
        verificationCode: input.verificationCode,
        flowId: flow!.id,
      });
    } catch (err) {
      // TODO: handle error properly
      form.setError('verificationCode', {
        message: `That code isn't valid. You can request a new one`,
        type: 'server',
      });
    }
  };

  const resendVerificationCode = async () => {
    await resendVerificationRegisterFlow.mutateAsync({ flowId: flow!.id });
  };

  return (
    <Card>
      <CardHeader>
        <div className='flex w-full items-center justify-between gap-2'>
          <div className='flex flex-col gap-2'>
            <h1 className='text-md font-semibold'>Enter Verification Code</h1>
            <h3 className='text-xs font-extralight'>
              Enter the code we sent to {flow?.email}
            </h3>
          </div>
          <Button variant='secondary' onClick={resendVerificationCode}>
            resend code
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        <Form {...form}>
          <form
            onSubmit={form.handleSubmit(onSubmit)}
            className='flex flex-col items-start gap-4'
          >
            <FormField
              control={form.control}
              name='verificationCode'
              render={({ field }) => (
                <FormItem>
                  <FormLabel />
                  <FormControl>
                    <InputOTP
                      {...field}
                      inputMode='numeric'
                      maxLength={EMAIL_VERIFICATION_CODE_LENGTH}
                      render={({ slots }) => (
                        <>
                          <InputOTPGroup>
                            {slots.slice(0, 2).map((slot, idx) => (
                              <InputOTPSlot key={idx} {...slot} />
                            ))}
                          </InputOTPGroup>
                          <InputOTPSeparator />
                          <InputOTPGroup>
                            {slots.slice(2, 4).map((slot, idx) => (
                              <InputOTPSlot key={idx} {...slot} />
                            ))}
                          </InputOTPGroup>
                          <InputOTPSeparator />
                          <InputOTPGroup>
                            {slots.slice(4, 6).map((slot, idx) => (
                              <InputOTPSlot key={idx} {...slot} />
                            ))}
                          </InputOTPGroup>
                          <InputOTPSeparator />
                          <InputOTPGroup>
                            {slots.slice(6).map((slot, idx) => (
                              <InputOTPSlot key={idx} {...slot} />
                            ))}
                          </InputOTPGroup>
                        </>
                      )}
                    />
                  </FormControl>
                  <FormDescription />
                  <FormMessage />
                </FormItem>
              )}
            />

            <Button
              type='submit'
              disabled={!form.formState.isValid || form.formState.isSubmitting}
              className='w-full'
            >
              Continue
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
