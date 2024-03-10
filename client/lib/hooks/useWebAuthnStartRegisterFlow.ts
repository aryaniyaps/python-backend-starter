import { useMutation } from '@tanstack/react-query';
import { authenticationApi } from '../api';

export default function useWebAuthnStartRegisterFlow() {
  return useMutation({
    mutationFn: async ({ flowId }: { flowId: string }) => {
      return await authenticationApi.openAPITagAUTHENTICATIONStartWebauthnRegisterFlow(
        { registerFlowId: flowId }
      );
    },
  });
}
