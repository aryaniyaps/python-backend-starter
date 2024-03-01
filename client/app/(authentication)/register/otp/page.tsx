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
        <h1 className='text-md font-semibold'>Enter {APP_NAME} OTP</h1>
        <div className='flex w-full items-center justify-between'>
          <h3 className='text-xs font-extralight'>
            Enter the OTP we sent to ary*********06@gmail.com
          </h3>
          <Button variant='flat' size='sm'>
            resend OTP
          </Button>
        </div>
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
            Confirm
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
