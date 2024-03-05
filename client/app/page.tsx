'use client';
import { client } from '@/lib/client';
import useCurrentUser from '@/lib/hooks/useCurrentUser';
import { Button, Spinner } from '@nextui-org/react';
import { useRouter } from 'next/navigation';

export default function Home() {
  const router = useRouter();

  const { data, isLoading } = useCurrentUser();

  async function logout() {
    await client.POST('/auth/logout', { body: { rememberSession: false } });
    router.refresh();
  }

  if (isLoading) {
    return (
      <main className='flex min-h-screen items-center justify-center p-24'>
        <Spinner />
      </main>
    );
  }
  return (
    <main className='flex min-h-screen flex-col items-center justify-center gap-unit-6 p-24'>
      Hi, {data?.email}! You are authenticated
      <pre>{data ? JSON.stringify(data) : null}</pre>
      <Button color='danger' onClick={logout}>
        logout
      </Button>
    </main>
  );
}
