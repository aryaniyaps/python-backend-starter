'use client';
import { OTPSlot } from '@/components/otp-input';
import { APP_NAME, EMAIL_VERIFICATION_CODE_LENGTH } from '@/lib/constants';
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
import { Controller, SubmitHandler, useForm } from 'react-hook-form';
import * as yup from 'yup';

const registerOTPSchema = yup
  .object({
    otp: yup.string().required().length(EMAIL_VERIFICATION_CODE_LENGTH),
  })
  .required();

export default function RegisterOTPPage() {
  const { control, handleSubmit, formState } = useForm({
    resolver: yupResolver(registerOTPSchema),
  });

  const onSubmit: SubmitHandler<
    yup.InferType<typeof registerOTPSchema>
  > = async (data) => {};

  return (
    <Card isFooterBlurred fullWidth className='px-unit-2'>
      <CardHeader className='flex flex-col items-start gap-unit-2'>
        <h1 className='text-md font-semibold'>Enter {APP_NAME} OTP</h1>
        <h3 className='text-xs font-extralight'>
          Enter the OTP we sent to ar*****06@gmail.com
        </h3>
      </CardHeader>
      <CardBody>
        <form onSubmit={handleSubmit(onSubmit)} className='flex flex-col gap-4'>
          <Controller
            name='otp'
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
          <p className='text-xs'>
            Didn&apos;t receive an OTP?&nbsp;
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
