'use client';

import { getQueryClient } from '@/lib/queryClient';
import { NextUIProvider } from '@nextui-org/react';
import { QueryClientProvider } from '@tanstack/react-query';
import { ThemeProvider as NextThemesProvider } from 'next-themes';

export function Providers({ children }: { children: React.ReactNode }) {
  const queryClient = getQueryClient();
  return (
    <NextUIProvider className='h-full'>
      <NextThemesProvider attribute='class' defaultTheme='dark'>
        <QueryClientProvider client={queryClient}>
          {children}
        </QueryClientProvider>
      </NextThemesProvider>
    </NextUIProvider>
  );
}
