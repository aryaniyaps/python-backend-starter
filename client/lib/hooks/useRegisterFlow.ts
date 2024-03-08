import { useQuery } from '@tanstack/react-query';
import { client } from '../client';

export default function useRegisterFlow({ flowId }: { flowId: string }) {
  return useQuery({
    queryKey: ['/auth/register/flows', flowId],
    queryFn: async () => {
      const { data } = await client.GET('/auth/register/flows/{flow_id}', {
        params: { path: { flow_id: flowId } },
      });
      return data;
    },
  });
}
