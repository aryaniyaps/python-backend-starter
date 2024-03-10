import { useMutation } from '@tanstack/react-query';
import { authenticationApi } from '../api';

export default function useDeleteUserSession() {
  return useMutation({
    mutationFn: async ({ sessionId }: { sessionId: string }) => {
      return await authenticationApi.deleteUserSession({
        sessionId,
      });
    },
  });
}
