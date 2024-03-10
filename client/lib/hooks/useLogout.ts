import { useMutation } from '@tanstack/react-query';
import { authenticationApi } from '../api';

export default function useLogout() {
  return useMutation({
    mutationFn: async ({ rememberSession }: { rememberSession: boolean }) => {
      return await authenticationApi.openAPITagAUTHENTICATIONDeleteCurrentUserSession(
        { logoutInput: { rememberSession } }
      );
    },
  });
}
