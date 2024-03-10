import { useSuspenseQuery } from '@tanstack/react-query';
import { usersApi } from '../api';

export default function useCurrentUser() {
  return useSuspenseQuery({
    queryKey: ['/users/@me'],
    queryFn: async () => {
      return await usersApi.openAPITagUSERSGetCurrentUser();
    },
  });
}
