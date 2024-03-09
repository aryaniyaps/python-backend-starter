import { useMutation } from '@tanstack/react-query';
import { client } from '../client';

export default function useLogout() {
  return useMutation({
    mutationFn: async ({ rememberSession }: { rememberSession: boolean }) => {
      await client.POST('/auth/logout', { body: { rememberSession } });
    },
  });
}
