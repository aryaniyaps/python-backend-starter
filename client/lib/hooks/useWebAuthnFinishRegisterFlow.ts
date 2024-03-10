import { useMutation } from '@tanstack/react-query';
import { authenticationApi } from '../api';

export default function useWebAuthnFinishRegisterFlow() {
  return useMutation({
    mutationFn: async ({
      credential,
      flowId,
    }: {
      credential: string;
      flowId: string;
    }) => {
      return await authenticationApi.finishWebauthnRegisterFlow({
        registerFlowId: flowId,
        registerFlowWebAuthnFinishInput: { credential },
      });
    },
  });
}
