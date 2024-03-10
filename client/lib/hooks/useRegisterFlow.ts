import { useQuery } from '@tanstack/react-query';
import { authenticationApi } from '../api';

export default function useRegisterFlow(
  {
    flowId,
  }: {
    flowId: string;
  },
  initialData:
    | { id: string; email: string; currentStep: string }
    | undefined = undefined
) {
  return useQuery({
    queryKey: ['/auth/register/flows', flowId],
    queryFn: async () => {
      return await authenticationApi.openAPITagAUTHENTICATIONGetRegisterFlow({
        flowId,
      });
    },
    initialData,
    refetchOnMount: false,
  });
}
