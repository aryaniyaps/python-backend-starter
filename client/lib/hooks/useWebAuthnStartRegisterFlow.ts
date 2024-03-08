import { useMutation } from '@tanstack/react-query';
import { client } from '../client';

export default function useWebAuthnStartRegisterFlow() {
  return useMutation({
    mutationFn: async ({ flowId }: { flowId: string }) => {
      const { data } = await client.POST(
        '/auth/register/flows/webauthn-start',
        {
          params: { cookie: { register_flow_id: flowId } },
        }
      );
      return data;
    },
    onSuccess(data, variables, context) {
      // update query data here
    },
  });
}
