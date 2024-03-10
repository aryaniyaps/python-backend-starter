import { useSuspenseInfiniteQuery } from '@tanstack/react-query';
import { authenticationApi } from '../api';

export default function useUserSessions() {
  return useSuspenseInfiniteQuery({
    queryKey: ['/auth/user-sessions'],
    queryFn: async ({ pageParam }) => {
      return await authenticationApi.getUserSessions({ after: pageParam });
    },
    getNextPageParam: (lastPage, pages) => lastPage.pageInfo.nextCursor,
    initialPageParam: undefined,
  });
}
