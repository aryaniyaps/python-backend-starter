import SidebarNav from '@/components/settings/sidebar-nav';
import { APP_NAME } from '@/lib/constants';
import Link from 'next/link';

const sidebarNavItems = [
  {
    title: 'Profile',
    href: '/settings',
  },
  {
    title: 'Appearance',
    href: '/settings/appearance',
  },
];

export default function SettingsLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <main className=' flex min-h-screen w-full flex-col'>
      <div className='bg-content1 p-unit-4'>
        <div className='mx-auto flex max-w-7xl items-center'>
          <Link href='/'>
            <h1 className='font-semibold'>{APP_NAME} Settings</h1>
          </Link>
        </div>
      </div>
      <div className='mb-unit-12 flex min-h-full flex-1'>
        <div className='mx-auto flex min-h-full max-w-7xl flex-1 flex-col space-y-unit-12 p-unit-4 lg:flex-row lg:space-x-unit-16 lg:space-y-unit-0'>
          <aside className='lg:w-1/6'>
            <SidebarNav items={sidebarNavItems} />
          </aside>
          <div className='min-h-full flex-1 lg:max-w-2xl'>{children}</div>
        </div>
      </div>
    </main>
  );
}
