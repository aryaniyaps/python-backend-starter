import { useQuery } from '@tanstack/react-query';
import { client } from '../client';

export default function useCurrentUser() {
  return useQuery({
    queryKey: ['users/@me'],
    queryFn: async () => {
      const { data } = await client.GET('/users/@me');
      return data;
    },
  });
}
