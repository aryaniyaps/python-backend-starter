'use client';
import { OTPSlot } from '@/components/otp-input';
import { useRegisterFlow } from '@/components/register-flow-provider';
import { client } from '@/lib/client';
import { EMAIL_VERIFICATION_CODE_LENGTH } from '@/lib/constants';
import { yupResolver } from '@hookform/resolvers/yup';
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
import * as yup from 'yup';

const registerVerificationSchema = yup
  .object({
    verificationCode: yup
      .string()
      .required()
      .length(EMAIL_VERIFICATION_CODE_LENGTH),
  })
  .required();

export default function RegisterOTPPage() {
  const router = useRouter();
  const { flowId, email, setCurrentStep, setFlowId, setEmail } =
    useRegisterFlow();
  if (!flowId || !email) {
    // redirect to register page
    return router.push('/register');
  }

  const { control, handleSubmit, formState, setError } = useForm({
    resolver: yupResolver(registerVerificationSchema),
    reValidateMode: 'onSubmit',
  });

  const onSubmit: SubmitHandler<
    yup.InferType<typeof registerVerificationSchema>
  > = async (input) => {
    try {
      // verify register flow
      const { data } = await client.POST(
        '/auth/register/flows/{flow_id}/verify',
        {
          body: { verificationCode: input.verificationCode },
          params: { path: { flow_id: flowId } },
        }
      );

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
    await client.POST('/auth/register/flows/{flow_id}/resend-verification', {
      params: {
        path: { flow_id: flowId },
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
            Enter the code we sent to {email}
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
            await client.POST('/auth/register/flows/{flow_id}/cancel', {
              params: { path: { flow_id: flowId } },
            });
            setFlowId(null);
            setCurrentStep(null);
            setEmail(null);
          }}
        >
          Cancel
        </Button>
      </CardFooter>
    </Card>
  );
}
