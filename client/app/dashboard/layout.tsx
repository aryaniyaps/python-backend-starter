import UserNav from '@/components/dashboard/user-nav';
import { APP_NAME } from '@/lib/constants';
import Link from 'next/link';

export default function DashBoardLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <main className='flex h-full w-full flex-col'>
      <div className='border-b py-4'>
        <div className='mx-auto flex max-w-7xl items-center justify-between px-4'>
          <Link href='/dashboard'>
            <h1 className='font-semibold'>{APP_NAME}</h1>
          </Link>
          <UserNav />
        </div>
      </div>
      <div className='flex flex-grow overflow-hidden py-6'>
        <div className='mx-auto max-w-7xl px-4'>{children}</div>
      </div>
    </main>
  );
}
