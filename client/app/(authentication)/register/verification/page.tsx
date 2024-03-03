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
  const { flowId, email, setCurrentStep } = useRegisterFlow();
  if (!flowId || !email) {
    // redirect to register page
    return router.push('/register');
  }

  const { control, handleSubmit, formState, setError } = useForm({
    resolver: yupResolver(registerVerificationSchema),
  });

  const onSubmit: SubmitHandler<
    yup.InferType<typeof registerVerificationSchema>
  > = async (input) => {
    console.log(input);
    try {
      // verify register flow
      const { data } = await client.POST('/auth/register/flow/verify', {
        body: { flowId: flowId, verificationCode: input.verificationCode },
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

  return (
    <Card isFooterBlurred fullWidth className='px-unit-2'>
      <CardHeader className='flex flex-col items-start gap-unit-2'>
        <h1 className='text-md font-semibold'>Enter Verification Code</h1>
        <h3 className='text-xs font-extralight'>
          Enter the code we sent to {email}
        </h3>
      </CardHeader>
      <CardBody>
        <form onSubmit={handleSubmit(onSubmit)} className='flex flex-col gap-4'>
          <Controller
            name='verificationCode'
            control={control}
            render={({ field }) => (
              <OTPInput
                {...field}
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
          {formState.errors.verificationCode ? (
            <p className='text-xs text-danger'>
              {formState.errors.verificationCode.message}
            </p>
          ) : null}
          <p className='text-xs'>
            Didn&apos;t receive code?&nbsp;
            <strong className='text-primary'>resend</strong>
          </p>
          <Button
            color='primary'
            type='submit'
            isLoading={formState.isSubmitting}
            isDisabled={!formState.isValid}
          >
            Continue
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
