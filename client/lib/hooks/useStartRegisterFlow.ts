import { useMutation, useQueryClient } from '@tanstack/react-query';
import { authenticationApi } from '../api';

export default function useStartRegisterFlow() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ email }: { email: string }) => {
      return await authenticationApi.openAPITagAUTHENTICATIONStartRegisterFlow({
        registerFlowStartInput: { email },
        userAgent: navigator.userAgent,
      });
    },
    onSuccess(data) {
      // update query data
      queryClient.setQueryData(
        ['/auth/register/flows', data.registerFlow.id],
        data.registerFlow
      );
    },
  });
}
