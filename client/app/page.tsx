'use client';
import { client } from '@/lib/client';
import { Button } from '@nextui-org/react';
import { useRouter } from 'next/navigation';

export default function Home() {
  const router = useRouter();

  async function logout() {
    await client.POST('/auth/logout', { body: { rememberSession: false } });
    router.refresh();
  }
  return (
    <main className='flex min-h-screen flex-col items-center justify-center gap-unit-6 p-24'>
      Hi, user! You are authenticated
      <Button color='danger' onClick={logout}>
        logout
      </Button>
    </main>
  );
}
