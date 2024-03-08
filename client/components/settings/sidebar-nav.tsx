'use client';

import Link from 'next/link';

import { client } from '@/lib/client';
import { cn } from '@/utils/style';
import { Button } from '@nextui-org/react';
import { useRouter } from 'next/navigation';

interface SidebarNavProps extends React.HTMLAttributes<HTMLElement> {
  items: {
    href: string;
    title: string;
  }[];
}

export default function SidebarNav({
  className,
  items,
  ...props
}: SidebarNavProps) {
  const router = useRouter();

  async function logout() {
    await client.POST('/auth/logout', { body: { rememberSession: false } });
    router.replace('/login');
  }

  return (
    <nav
      className={cn(
        'flex h-full w-full items-start justify-between space-x-unit-4 lg:flex-col lg:space-x-unit-0 lg:space-y-unit-2',
        className
      )}
      {...props}
    >
      <div className='flex h-full w-full space-x-unit-4 lg:flex-col lg:space-x-unit-0 lg:space-y-unit-2'>
        {items.map((item) => (
          <Link key={item.href} href={item.href}>
            {item.title}
          </Link>
        ))}
      </div>
      <Button
        color='danger'
        className='text-destructive font-bold'
        onClick={logout}
      >
        Logout
      </Button>
    </nav>
  );
}
