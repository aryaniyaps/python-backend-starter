import { useSuspenseQuery } from '@tanstack/react-query';
import { client } from '../client';

export default function useCurrentUser() {
  return useSuspenseQuery({
    queryKey: ['/users/@me'],
    queryFn: async () => {
      const { data } = await client.GET('/users/@me');
      return data;
    },
  });
}
