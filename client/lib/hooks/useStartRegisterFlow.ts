import { useMutation } from '@tanstack/react-query';
import { client } from '../client';

export default function useStartRegisterFlow() {
  return useMutation({
    mutationFn: async ({ email }: { email: string }) => {
      const { data } = await client.POST('/auth/register/flows/start', {
        body: { email },
        params: { header: { 'user-agent': navigator.userAgent } },
      });
      return data;
    },
    onSuccess(data, variables, context) {
      // update query data here
    },
  });
}
