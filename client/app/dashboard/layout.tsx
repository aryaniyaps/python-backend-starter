import UserNav from '@/components/dashboard/user-nav';
import { APP_NAME } from '@/lib/constants';
import { Link } from '@nextui-org/react';

export default function DashBoardLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <main className='flex h-full w-full flex-col'>
      <div className='bg-default-50 py-unit-4'>
        <div className='mx-auto flex max-w-7xl items-center justify-between px-unit-4'>
          <Link href='/'>
            <h1 className='font-semibold'>{APP_NAME}</h1>
          </Link>
          <UserNav />
        </div>
      </div>
      <div className='mx-auto flex max-w-7xl flex-grow overflow-hidden px-unit-4 py-unit-6'>
        {children}
      </div>
    </main>
  );
}
