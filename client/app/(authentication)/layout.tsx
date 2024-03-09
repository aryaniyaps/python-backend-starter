import { Separator } from '@/components/ui/separator';

export default function AuthenticationLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className='mx-auto flex h-full w-full max-w-md flex-col items-center justify-center'>
      {children}
      <div className='flex w-full flex-col'>
        <Separator className='my-2 mt-8' />
        <div className='flex h-6 items-center justify-around space-x-2 text-xs'>
          <div>Terms</div>
          <Separator orientation='vertical' />
          <div>Privacy</div>
          <Separator orientation='vertical' />
          <div>Security</div>
          <Separator orientation='vertical' />
          <div>Contact us</div>
        </div>
      </div>
    </div>
  );
}
