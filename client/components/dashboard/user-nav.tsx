'use client';
import useCurrentUser from '@/lib/hooks/useCurrentUser';
import { Avatar } from '@nextui-org/react';
import Link from 'next/link';

export default function UserNav() {
  const { data: user } = useCurrentUser();

  return (
    <Link href='/settings' className='flex items-center gap-unit-4'>
      <Avatar src={user?.avatarUrl} name={user?.email} />
      <p className='hidden text-sm font-semibold leading-none sm:block'>
        {user?.email}
      </p>
    </Link>
  );
}
