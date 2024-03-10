import { useMutation } from '@tanstack/react-query';
import { authenticationApi } from '../api';

export default function useResendVerificationRegisterFlow() {
  return useMutation({
    mutationFn: async ({ flowId }: { flowId: string }) => {
      return await authenticationApi.resendVerificationRegisterFlow({
        registerFlowId: flowId,
        userAgent: navigator.userAgent,
      });
    },
  });
}
