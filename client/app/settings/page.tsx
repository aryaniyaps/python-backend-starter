'use client';
import ChangeEmailDialog from '@/components/settings/account/change-email-dialog';
import ProfileForm from '@/components/settings/account/profile-form';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Input } from '@/components/ui/input';
import { Separator } from '@/components/ui/separator';
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from '@/components/ui/tooltip';
import { APP_NAME } from '@/lib/constants';
import useCurrentUser from '@/lib/hooks/useCurrentUser';
import Link from 'next/link';

export default function AccountSettingsPage() {
  const { data: user } = useCurrentUser();

  return (
    <div className='space-y-6'>
      <div className='flex flex-col'>
        <h3 className='text-lg font-medium'>User profile</h3>
        <p className='text-sm text-muted-foreground'>
          This is how others will see you on {APP_NAME}.
        </p>
      </div>
      <div className='flex w-full justify-between gap-8'>
        <ProfileForm />
        <div className='flex flex-col items-center gap-4'>
          <Tooltip>
            <TooltipTrigger asChild>
              <Avatar className='h-32 w-32'>
                <AvatarImage
                  src={user?.avatarUrl}
                  loading='eager'
                  alt={user?.email}
                />
                <AvatarFallback>{user?.email.slice(0, 2)}</AvatarFallback>
              </Avatar>
            </TooltipTrigger>
            <TooltipContent>
              Avatars are powered by{' '}
              <Link
                className='text-primary'
                href='https://gravatar.com/'
                rel='noopener noreferrer'
                target='_blank'
              >
                Gravatar.
              </Link>
            </TooltipContent>
          </Tooltip>
          <p className='text-sm text-muted-foreground'>User avatar</p>
        </div>
      </div>
      <Separator />
      <div>
        <h3 className='text-lg font-medium'>User email</h3>
        <p className='text-sm text-muted-foreground'>
          Your email address is private.
        </p>
      </div>
      <div className='flex w-full gap-4'>
        <Input className='w-96' value={user.email} disabled />
        <ChangeEmailDialog />
      </div>
    </div>
  );
}
