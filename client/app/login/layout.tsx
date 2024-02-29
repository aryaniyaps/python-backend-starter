import { Divider } from '@nextui-org/react';

export default function LoginLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className='flex h-full w-full max-w-md flex-col items-center justify-between'>
      {children}
      <div className='flex w-full flex-col'>
        <Divider className='my-4' />
        <div className='flex h-5 items-center justify-around space-x-4 text-small'>
          <div>Blog</div>
          <Divider orientation='vertical' />
          <div>Docs</div>
          <Divider orientation='vertical' />
          <div>Source</div>
        </div>
      </div>
    </div>
  );
}
