import { REGISTER_FLOW_ID_COOKIE } from '@/lib/constants';
import { cookies } from 'next/headers';

import { LocalRegisterFlowProvider } from '@/components/register/flow-provider';
import RegisterForm from '@/components/register/register-form';
import { client } from '@/lib/api';

export default async function RegisterPage() {
  const cookieStore = cookies();
  const flowId = cookieStore.get(REGISTER_FLOW_ID_COOKIE);

  let flow = null;

  if (flowId) {
    try {
      const { data } = await client.GET('/auth/register/flows/{flow_id}', {
        params: { path: { flow_id: flowId.value } },
      });
      if (data) {
        flow = data;
      }
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
