'use client';
import { OTPSlot } from '@/components/otp-input';
import { APP_NAME } from '@/lib/constants';
import {
  Button,
  Card,
  CardBody,
  CardFooter,
  CardHeader,
  Divider,
  Link,
} from '@nextui-org/react';
import { OTPInput } from 'input-otp';
import { Controller, SubmitHandler, useForm } from 'react-hook-form';

type RegisterOTPInput = {
  otp: string;
};

export default function RegisterOTPPage() {
  const { control, handleSubmit } = useForm<RegisterOTPInput>({});

  const onSubmit: SubmitHandler<RegisterOTPInput> = async (data) => {};

  return (
    <Card isFooterBlurred fullWidth className='px-unit-2'>
      <CardHeader className='flex flex-col items-start gap-unit-2'>
        <h1 className='text-md font-semibold'>Enter your {APP_NAME} OTP</h1>
        <h3 className='text-xs font-extralight'>
          We sent an OTP to ary*********06@gmail.com
        </h3>
      </CardHeader>
      <CardBody>
        <form onSubmit={handleSubmit(onSubmit)} className='flex flex-col gap-4'>
          <Controller
            render={({ field }) => (
              <OTPInput
                {...field}
                maxLength={8}
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
            control={control}
            name='otp'
          />

          <Button color='primary' type='submit'>
            Continue
          </Button>
        </form>
      </CardBody>
      <CardFooter className='flex justify-between text-sm'>
        <Link href='/register'>go back</Link>
        <p>resend OTP in 5s</p>
      </CardFooter>
    </Card>
  );
}
