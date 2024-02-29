import { APP_NAME } from '@/lib/constants';
import {
  Button,
  Card,
  CardBody,
  CardFooter,
  CardHeader,
  Input,
  Link,
} from '@nextui-org/react';
export default function RegisterPage() {
  return (
    <Card isFooterBlurred fullWidth className='px-unit-2'>
      <CardHeader>
        <h1 className='text-md font-semibold'>Create a {APP_NAME} account</h1>
      </CardHeader>
      <CardBody className='flex flex-col gap-4'>
        <Input type='email' label='Email address' />
        <Input type='text' label='Display name' />
        <Button color='primary'>Continue</Button>
      </CardBody>
      <CardFooter className='text-sm'>
        Have an account?&nbsp;<Link href='/login'>sign in</Link>
      </CardFooter>
    </Card>
  );
}
