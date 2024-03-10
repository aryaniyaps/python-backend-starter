import { useMutation, useQueryClient } from '@tanstack/react-query';
import { authenticationApi } from '../api';

export default function useAuthenticateFinish() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({ credential }: { credential: string }) => {
      return await authenticationApi.verifyAuthenticationResponse({
        authenticateVerificationInput: { credential },
        userAgent: navigator.userAgent,
      });
    },
    onSuccess(data) {
      // update user query data
      queryClient.setQueryData(['/users/@me'], data);
    },
  });
}
