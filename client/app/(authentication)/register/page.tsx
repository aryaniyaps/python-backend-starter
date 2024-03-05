import { REGISTER_FLOW_ID_COOKIE } from '@/lib/constants';
import { cookies } from 'next/headers';

import { RegisterFlowProvider } from '@/components/register/flow-provider';
import RegisterForm from '@/components/register/register-form';
import { client } from '@/lib/client';

export default async function RegisterPage() {
  const cookieStore = cookies();
  const flowId = cookieStore.get(REGISTER_FLOW_ID_COOKIE);

  let flow;

  if (flowId) {
    try {
      console.log('GETTING FLOW DATA: ', flowId.value);
      const { data } = await client.GET('/auth/register/flows', {
        params: { cookie: { register_flow_id: flowId.value } },
      });
      if (data) {
        console.log('GOT FLOW DATA');
        flow = data;
      }
    } catch (err) {
      console.log(typeof err);
      console.log(JSON.stringify(err, null, 4));
      // TODO: handle errs better
      // TODO: delete register flow ID cookie if it is invalid
      // cookieStore.delete(REGISTER_FLOW_ID_COOKIE);
    }
  }

  return (
    <RegisterFlowProvider flow={flow}>
      <RegisterForm />
    </RegisterFlowProvider>
  );
}
