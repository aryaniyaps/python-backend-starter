import { useMutation } from '@tanstack/react-query';
import { client } from '../client';

export default function useAuthenticateFinish() {
  return useMutation({
    mutationFn: async ({ credential }: { credential: string }) => {
      const { data } = await client.POST('/auth/authenticate/finish', {
        body: { credential },
        params: { header: { 'user-agent': navigator.userAgent } },
      });
      return data;
    },
    onSuccess(data, variables, context) {
      // update user query data here
    },
  });
}
