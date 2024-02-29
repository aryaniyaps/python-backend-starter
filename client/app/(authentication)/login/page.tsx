import { APP_NAME } from '@/lib/constants';
import {
  Card,
  CardBody,
  CardFooter,
  CardHeader,
  Input,
  Link,
} from '@nextui-org/react';

export default function LoginPage() {
  return (
    <Card isFooterBlurred fullWidth>
      <CardHeader>
        <h1 className='text-md font-semibold'>Sign in with {APP_NAME}</h1>
      </CardHeader>
      <CardBody>
        <Input type='email' label='Email address' />
      </CardBody>
      <CardFooter className='text-sm'>
        Don&apos;t have an account?&nbsp;<Link href='/register'>sign up</Link>
      </CardFooter>
    </Card>
  );
}
