'use client';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import useCurrentUser from '@/lib/hooks/useCurrentUser';
import Link from 'next/link';

export default function UserNav() {
  const { data: user } = useCurrentUser();

  return (
    <DropdownMenu>
      <DropdownMenuTrigger>
        <Avatar className='h-8 w-8'>
          <AvatarImage src={user.avatarUrl} loading='eager' alt={user.email} />
          <AvatarFallback>{user.email.slice(0, 2)}</AvatarFallback>
        </Avatar>
      </DropdownMenuTrigger>
      <DropdownMenuContent align='end' sideOffset={15}>
        <DropdownMenuLabel>{user.email}</DropdownMenuLabel>
        <Link href='/settings'>
          <DropdownMenuItem>Settings</DropdownMenuItem>
        </Link>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
