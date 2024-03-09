'use client';
import ProfileForm from '@/components/settings/account/profile-form';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Separator } from '@/components/ui/separator';
import { APP_NAME } from '@/lib/constants';
import useCurrentUser from '@/lib/hooks/useCurrentUser';

export default function AccountSettingsPage() {
  const { data: user } = useCurrentUser();

  return (
    <div className='space-y-6'>
      <div>
        <h3 className='text-lg font-medium'>User avatar</h3>
        <p className='text-muted-foreground text-sm'>
          {APP_NAME} uses Gravatar for avatars.
        </p>
      </div>
      <Avatar className='h-32 w-32'>
        <AvatarImage src={user?.avatarUrl} loading='eager' alt={user?.email} />
        <AvatarFallback>{user?.email.slice(0, 2)}</AvatarFallback>
      </Avatar>
      <Separator />
      <div>
        <h3 className='text-lg font-medium'>User profile</h3>
        <p className='text-muted-foreground text-sm'>
          This is how others will see you on {APP_NAME}.
        </p>
      </div>
      <ProfileForm />
    </div>
  );
}
