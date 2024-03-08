import { useMutation, useQueryClient } from '@tanstack/react-query';
import { client } from '../client';

export default function useCancelRegisterFlow() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({ flowId }: { flowId: string }) => {
      const { data } = await client.POST('/auth/register/flows/cancel', {
        params: { cookie: { register_flow_id: flowId } },
      });
      return data;
    },
    onSuccess(_data, variables) {
      // update query data here
      queryClient.removeQueries({
        queryKey: ['/auth/register/flows', variables.flowId],
      });
    },
  });
}
