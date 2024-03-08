import { useMutation, useQueryClient } from '@tanstack/react-query';
import { client } from '../client';

export default function useVerifyRegisterFlow() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({
      verificationCode,
      flowId,
    }: {
      verificationCode: string;
      flowId: string;
    }) => {
      const { data } = await client.POST('/auth/register/flows/verify', {
        body: { verificationCode },
        params: {
          header: { 'user-agent': navigator.userAgent },
          cookie: { register_flow_id: flowId },
        },
      });
      return data;
    },
    onSuccess(data, variables) {
      // update query data
      queryClient.setQueryData(
        ['/auth/register/flows', variables.flowId],
        data?.registerFlow
      );
    },
  });
}
