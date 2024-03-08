'use client';
import { useRegisterFlow } from '@/components/register/flow-provider';
import { OTPSlot } from '@/components/ui/otp-input';
import { client } from '@/lib/client';
import { EMAIL_VERIFICATION_CODE_LENGTH } from '@/lib/constants';
import { zodResolver } from '@hookform/resolvers/zod';
import {
  Button,
  Card,
  CardBody,
  CardFooter,
  CardHeader,
  Divider,
} from '@nextui-org/react';
import { OTPInput } from 'input-otp';
import { useRouter } from 'next/navigation';
import { Controller, SubmitHandler, useForm } from 'react-hook-form';
import * as z from 'zod';

const registerVerificationSchema = z.object({
  verificationCode: z.string().length(EMAIL_VERIFICATION_CODE_LENGTH),
});

export default function RegisterEmailVerification() {
  const { setCurrentStep, flow } = useRegisterFlow();

  const router = useRouter();

  const { control, handleSubmit, formState, setError } = useForm({
    resolver: zodResolver(registerVerificationSchema),
    reValidateMode: 'onSubmit',
  });

  const onSubmit: SubmitHandler<
    z.infer<typeof registerVerificationSchema>
  > = async (input) => {
    try {
      // verify register flow
      const { data } = await client.POST('/auth/register/flows/verify', {
        body: { verificationCode: input.verificationCode },
        params: { cookie: { register_flow_id: flow!.id } },
      });

      if (data) {
        setCurrentStep(data.registerFlow.currentStep);
      }
    } catch (err) {
      // TODO: handle error properly
      setError('verificationCode', {
        message: `That code isn't valid. You can request a new one.`,
        type: 'server',
      });
    }
  };

  const resendVerificationCode = async () => {
    await client.POST('/auth/register/flows/resend-verification', {
      params: {
        cookie: { register_flow_id: flow!.id },
        header: { 'user-agent': navigator.userAgent },
      },
    });
  };

  return (
    <Card isFooterBlurred fullWidth className='px-unit-2'>
      <CardHeader className='flex w-full items-center justify-between gap-unit-2'>
        <div className='flex flex-col gap-unit-2'>
          <h1 className='text-md font-semibold'>Enter Verification Code</h1>
          <h3 className='text-xs font-extralight'>
            Enter the code we sent to {flow?.email}
          </h3>
        </div>
        <Button size='sm' variant='ghost' onClick={resendVerificationCode}>
          resend code
        </Button>
      </CardHeader>
      <CardBody>
        <form
          onSubmit={handleSubmit(onSubmit)}
          className='flex flex-col items-start gap-4'
        >
          <Controller
            name='verificationCode'
            control={control}
            render={({ field }) => (
              <OTPInput
                {...field}
                inputMode='numeric'
                maxLength={EMAIL_VERIFICATION_CODE_LENGTH}
                containerClassName='group flex items-center has-[:disabled]:opacity-30'
                render={({ slots }) => (
                  <>
                    <div className='flex'>
                      {slots.slice(0, 2).map((slot, idx) => (
                        <OTPSlot key={idx} {...slot} />
                      ))}
                    </div>

                    <Divider
                      orientation='horizontal'
                      className='mx-unit-2 w-unit-2'
                    />

                    <div className='flex'>
                      {slots.slice(2, 4).map((slot, idx) => (
                        <OTPSlot key={idx} {...slot} />
                      ))}
                    </div>

                    <Divider
                      orientation='horizontal'
                      className='mx-unit-2 w-unit-2'
                    />

                    <div className='flex'>
                      {slots.slice(4, 6).map((slot, idx) => (
                        <OTPSlot key={idx} {...slot} />
                      ))}
                    </div>

                    <Divider
                      orientation='horizontal'
                      className='mx-unit-2 w-unit-2'
                    />

                    <div className='flex'>
                      {slots.slice(6).map((slot, idx) => (
                        <OTPSlot key={idx} {...slot} />
                      ))}
                    </div>
                  </>
                )}
              />
            )}
          />
          {formState.errors.verificationCode &&
          formState.errors.verificationCode.type == 'server' ? (
            <p className='text-xs text-danger'>
              {formState.errors.verificationCode.message}
            </p>
          ) : null}

          <Button
            color='primary'
            type='submit'
            isLoading={formState.isSubmitting}
            isDisabled={!formState.isValid}
            fullWidth
          >
            Continue
          </Button>
        </form>
      </CardBody>
      <CardFooter>
        <Button
          variant='ghost'
          fullWidth
          onClick={async () => {
            await client.POST('/auth/register/flows/cancel', {
              params: { cookie: { register_flow_id: flow!.id } },
            });
            router.refresh();
          }}
        >
          Cancel
        </Button>
      </CardFooter>
    </Card>
  );
}
