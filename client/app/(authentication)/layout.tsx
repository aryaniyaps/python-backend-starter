import { Divider } from '@nextui-org/react';

export default function AuthenticationLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className='mx-auto flex h-full w-full max-w-md flex-col items-center justify-center'>
      {children}
      <div className='flex w-full flex-col'>
        <Divider className='my-4' />
        <div className='flex h-5 items-center justify-around space-x-4 text-xs'>
          <div>Terms</div>
          <Divider orientation='vertical' />
          <div>Privacy</div>
          <Divider orientation='vertical' />
          <div>Security</div>
          <Divider orientation='vertical' />
          <div>Contact us</div>
        </div>
      </div>
    </div>
  );
}
