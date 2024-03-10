import { useMutation } from '@tanstack/react-query';
import { authenticationApi } from '../api';

export default function useAuthenticateStart() {
  return useMutation({
    mutationFn: async ({ email }: { email: string }) => {
      return await authenticationApi.generateAuthenticationOptions({
        authenticateOptionsInput: { email },
      });
    },
  });
}
