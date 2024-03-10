'use client';
import { Button } from '@/components/ui/button';
import useUserSessions from '@/lib/hooks/useUserSessions';
import React from 'react';
import UserSessionCard from './user-session-card';

export default function UserSessionList() {
  const userSessions = useUserSessions();

  return (
    <div className='flex h-full flex-1 flex-col gap-4'>
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
  );
}
