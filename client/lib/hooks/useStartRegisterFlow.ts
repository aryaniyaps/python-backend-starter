import { useMutation, useQueryClient } from '@tanstack/react-query';
import { client } from '../client';

export default function useStartRegisterFlow() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ email }: { email: string }) => {
      const { data } = await client.POST('/auth/register/flows/start', {
        body: { email },
        params: { header: { 'user-agent': navigator.userAgent } },
      });
      return data;
    },
    onSuccess(data) {
      // update query data
      console.log('SUCCESS DATA: ', data);
      queryClient.setQueryData(
        ['/auth/register/flows', data?.registerFlow.id],
        data?.registerFlow
      );
    },
  });
}
