import { useMutation } from '@tanstack/react-query';
import { client } from '../client';

export default function useWebAuthnFinishRegisterFlow() {
  return useMutation({
    mutationFn: async ({
      credential,
      flowId,
    }: {
      credential: string;
      flowId: string;
    }) => {
      const { data } = await client.POST(
        '/auth/register/flows/webauthn-finish',
        {
          body: { credential },
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
