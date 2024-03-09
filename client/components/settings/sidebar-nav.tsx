'use client';

import Link from 'next/link';

import { client } from '@/lib/client';
import { cn } from '@/utils/style';
import { usePathname, useRouter } from 'next/navigation';
import { Button, buttonVariants } from '../ui/button';

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

  const pathname = usePathname();

  async function logout() {
    await client.POST('/auth/logout', { body: { rememberSession: false } });
    router.replace('/login');
  }

  return (
    <nav
      className={cn(
        'flex h-full w-full items-start justify-between space-x-2 lg:flex-col lg:space-x-0 lg:space-y-1',
        className
      )}
      {...props}
    >
      <div className='flex h-full w-full space-x-2 lg:flex-col lg:space-x-0 lg:space-y-1'>
        {items.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className={cn(
              buttonVariants({ variant: 'ghost' }),
              pathname === item.href
                ? 'bg-muted hover:bg-muted'
                : 'hover:bg-transparent hover:underline',
              'justify-start'
            )}
          >
            {item.title}
          </Link>
        ))}
      </div>
      <Button
        variant='ghost'
        className='text-destructive font-bold'
        onClick={logout}
      >
        Logout
      </Button>
    </nav>
  );
}
