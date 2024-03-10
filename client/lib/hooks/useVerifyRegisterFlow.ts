import { useMutation, useQueryClient } from '@tanstack/react-query';
import { authenticationApi } from '../api';

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
      return await authenticationApi.verifyRegisterFlow({
        registerFlowId: flowId,
        registerFlowVerifyInput: { verificationCode },
      });
    },
    onSuccess(data, variables) {
      // update query data
      queryClient.setQueryData(
        ['/auth/register/flows', variables.flowId],
        data.registerFlow
      );
    },
  });
}
