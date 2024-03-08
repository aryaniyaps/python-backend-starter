'use client';
import RegisterEmailVerification from '@/components/register/email-verification';
import RegisterFlowStart from '@/components/register/flow-start';
import RegisterWebAuthnRegistration from '@/components/register/webauthn-registration';
import { useLocalRegisterFlow } from './flow-provider';

export default function RegisterForm() {
  const { flow } = useLocalRegisterFlow();

  if (!flow) {
    return <RegisterFlowStart />;
  }

  switch (flow.currentStep) {
    case 'email_verification':
      return <RegisterEmailVerification />;
    case 'webauthn_registration':
      return <RegisterWebAuthnRegistration />;
  }
}
