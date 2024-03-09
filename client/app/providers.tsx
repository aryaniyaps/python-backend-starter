'use client';

import { getQueryClient } from '@/lib/queryClient';
import { QueryClientProvider } from '@tanstack/react-query';
import { ThemeProvider as NextThemesProvider } from 'next-themes';

export function Providers({ children }: { children: React.ReactNode }) {
  const queryClient = getQueryClient();
  return (
    <NextThemesProvider
      attribute='class'
      defaultTheme='dark'
      enableSystem
      disableTransitionOnChange
    >
      <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
    </NextThemesProvider>
  );
}
