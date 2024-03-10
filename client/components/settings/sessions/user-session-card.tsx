'use client';
import { Button } from '@/components/ui/button';
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
} from '@/components/ui/card';
import { UserSessionSchema } from '@/generated/openapi/v1.0';
import useDeleteUserSession from '@/lib/hooks/useDeleteUserSession';

const dateTimeFormat = new Intl.DateTimeFormat('en', {
  day: '2-digit',
  month: 'long',
  year: 'numeric',
});

export default function UserSessionCard({
  userSession,
}: {
  userSession: UserSessionSchema;
}) {
  const deleteUserSession = useDeleteUserSession();

  async function revokeSession() {
    await deleteUserSession.mutateAsync({ sessionId: userSession.id });
  }

  console.log(userSession.loggedOutAt);
  console.log(userSession.createdAt);

  return (
    <Card>
      <CardHeader>
        <div className='flex w-full items-center justify-between gap-4'>
          <p>
            {userSession.location} {userSession.ipAddress}
          </p>
          <Button
            variant='destructive'
            disabled
            size='sm'
            onClick={revokeSession}
          >
            Revoke
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        <div className='flex flex-col gap-2'>
          <p>{userSession.userAgent}</p>
        </div>
      </CardContent>
      <CardFooter>
        {userSession.loggedOutAt !== null ? (
          <p className='text-xs text-muted-foreground'>
            logged out on {dateTimeFormat.format(userSession.createdAt)}
          </p>
        ) : (
          <p className='text-xs text-muted-foreground'>
            created on {dateTimeFormat.format(userSession.createdAt)}
          </p>
        )}
      </CardFooter>
    </Card>
  );
}
