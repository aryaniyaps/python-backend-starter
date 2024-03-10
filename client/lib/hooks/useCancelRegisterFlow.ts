import { useMutation, useQueryClient } from '@tanstack/react-query';
import { authenticationApi } from '../api';

export default function useCancelRegisterFlow() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({ flowId }: { flowId: string }) => {
      return await authenticationApi.openAPITagAUTHENTICATIONCancelRegisterFlow(
        { registerFlowId: flowId }
      );
    },
    onSuccess(_data, variables) {
      // update query data here
      queryClient.removeQueries({
        queryKey: ['/auth/register/flows', variables.flowId],
      });
    },
  });
}
