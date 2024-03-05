'use client';
import RegisterEmailVerification from '@/components/register/email-verification';
import RegisterFlowStart from '@/components/register/flow-start';
import RegisterWebAuthnRegistration from '@/components/register/webauthn-registration';
import { useRegisterFlow } from './flow-provider';

export default function RegisterForm() {
  const { currentStep } = useRegisterFlow();

  if (!currentStep) {
    return <RegisterFlowStart />;
  }
  switch (currentStep) {
    case 'email_verification':
      return <RegisterEmailVerification />;
    case 'webauthn_registration':
      return <RegisterWebAuthnRegistration />;
  }
}
