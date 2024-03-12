import { useSuspenseQuery } from '@tanstack/react-query';
import { authenticationApi } from '../api';

export default function useWebAuthnCredentials() {
  return useSuspenseQuery({
    queryKey: ['/auth/webauthn-credentials'],
    queryFn: async () => {
      return await authenticationApi.getWebauthnCredentials();
    },
  });
}
