import { REGISTER_FLOW_ID_COOKIE } from '@/lib/constants';
import { cookies } from 'next/headers';

import { LocalRegisterFlowProvider } from '@/components/register/flow-provider';
import RegisterForm from '@/components/register/register-form';
import { authenticationApi } from '@/lib/api';

export default async function RegisterPage() {
  const cookieStore = cookies();
  const flowId = cookieStore.get(REGISTER_FLOW_ID_COOKIE);

  let flow = null;

  if (flowId) {
    try {
      flow = await authenticationApi.getRegisterFlow({ flowId: flowId.value });
    } catch (err) {
      // TODO: handle errs better
      // TODO: delete register flow ID cookie if it is invalid
      // cookieStore.delete(REGISTER_FLOW_ID_COOKIE);
    }
  }

  return (
    <LocalRegisterFlowProvider flow={flow}>
      <RegisterForm />
    </LocalRegisterFlowProvider>
  );
}
