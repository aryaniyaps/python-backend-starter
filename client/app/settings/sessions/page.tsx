'use client';
import UserSessionCard from '@/components/settings/sessions/user-session-card';
import { Button } from '@/components/ui/button';
import useUserSessions from '@/lib/hooks/useUserSessions';
import React from 'react';

export default function SessionsSettingsPage() {
  const userSessions = useUserSessions();

  return (
    <div className='space-y-6'>
      <div>
        <h3 className='text-lg font-medium'>Sessions</h3>
        <p className='text-sm text-muted-foreground'>
          Here are all the sessions that are currently active. Revoke any
          sessions that you do not recognize.
        </p>
      </div>
      <div className='flex flex-col gap-4'>
        {userSessions.data.pages.map((page, i) => (
          <React.Fragment key={i}>
            {page.entities.map((userSession) => (
              <UserSessionCard userSession={userSession} key={userSession.id} />
            ))}
          </React.Fragment>
        ))}
        {userSessions.hasNextPage ? (
          <Button
            className='w-full'
            variant='outline'
            onClick={() => userSessions.fetchNextPage()}
            disabled={userSessions.isFetchingNextPage}
          >
            {userSessions.isFetchingNextPage ? 'Loading more...' : 'Load More'}
          </Button>
        ) : null}
      </div>
    </div>
  );
}
