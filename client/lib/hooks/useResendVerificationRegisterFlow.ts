import { useMutation } from '@tanstack/react-query';
import { client } from '../client';

export default function useResendVerificationRegisterFlow() {
  return useMutation({
    mutationFn: async ({ flowId }: { flowId: string }) => {
      const { data } = await client.POST(
        '/auth/register/flows/resend-verification',
        {
          params: {
            header: { 'user-agent': navigator.userAgent },
            cookie: { register_flow_id: flowId },
          },
        }
      );
      return data;
    },
  });
}
