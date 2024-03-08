import { useMutation } from '@tanstack/react-query';
import { client } from '../client';

export default function useAuthenticateStart() {
  return useMutation({
    mutationFn: async ({ email }: { email: string }) => {
      const { data } = await client.POST('/auth/authenticate/start', {
        body: { email },
      });
      return data;
    },
  });
}
